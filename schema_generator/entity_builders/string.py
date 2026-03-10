import re
from genson.schema.strategies import String

ENUM_CARDINALITY_THRESHOLD = 3


def detect_pattern(values):
    """
    Tries to find a common regex pattern across all observed string values.
    Tests candidate patterns in order of specificity — first match wins.
    Returns None if no pattern fits all values.
    """
    candidates = [
        (r"^\d+$", r"^\d+$"),  # pure integers
        (r"^\d+\.\d+$", r"^\d+\.\d+$"),  # decimals
        (r"^-?\d+(\.\d+)?$", r"^-?\d+(\.\d+)?$"),  # numeric (signed)
        (r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$",
         r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$"),  # UUID
        (r"^\S+@\S+\.\S+$", r"^\S+@\S+\.\S+$"),  # email
        (r"^https?://", r"^https?://"),  # URL
        (r"^\d{4}-\d{2}-\d{2}$", r"^\d{4}-\d{2}-\d{2}$"),  # ISO date
        (r"^[A-Z]{2,3}$", r"^[A-Z]{2,3}$"),  # short uppercase codes
        (r"^[a-z_]+$", r"^[a-z_]+$"),  # snake_case identifiers
    ]

    for test_pattern, emit_pattern in candidates:
        if all(re.match(test_pattern, v) for v in values):
            return emit_pattern

    return None


class SchemaString(String):
    KEYWORDS = (*String.KEYWORDS, "minLength", "maxLength", "const", "enum", "pattern")

    def __init__(self, node_class):
        super().__init__(node_class)
        self._min_length = None
        self._max_length = None
        self._values = set()

    def add_object(self, obj):
        super().add_object(obj)
        length = len(obj)
        self._min_length = length if self._min_length is None else min(self._min_length, length)
        self._max_length = length if self._max_length is None else max(self._max_length, length)
        self._values.add(obj)

    def add_schema(self, schema):
        super().add_schema(schema)
        if "minLength" in schema:
            val = schema["minLength"]
            self._min_length = val if self._min_length is None else min(self._min_length, val)
        if "maxLength" in schema:
            val = schema["maxLength"]
            self._max_length = val if self._max_length is None else max(self._max_length, val)
        if "const" in schema:
            self._values.add(schema["const"])
        elif "enum" in schema:
            self._values.update(schema["enum"])

    def to_schema(self):
        schema = super().to_schema()

        if self._min_length is not None:
            schema["minLength"] = self._min_length
        if self._max_length is not None:
            schema["maxLength"] = self._max_length

        if len(self._values) == 1:
            schema["const"] = next(iter(self._values))
        elif len(self._values) <= ENUM_CARDINALITY_THRESHOLD:
            schema["enum"] = sorted(self._values)
        else:
            pattern = detect_pattern(self._values)
            if pattern:
                schema["pattern"] = pattern

        return schema
