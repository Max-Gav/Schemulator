from math import gcd
from genson.schema.strategies import Number


class SchemaInteger(Number):
    """
    Handles integer values only. Tracks multipleOf via GCD.
    Must be registered in EXTRA_STRATEGIES before SchemaNumber, so it
    gets priority for int values.
    """
    KEYWORDS = (*Number.KEYWORDS, "minimum", "maximum" "multipleOf")

    def __init__(self, node_class):
        super().__init__(node_class)
        self._min = None
        self._max = None
        self._multiple_of = None

    @classmethod
    def match_object(cls, obj):
        # booleans are a subclass of int in Python, exclude them
        return isinstance(obj, int) and not isinstance(obj, bool)

    @classmethod
    def match_schema(cls, schema):
        return schema.get("type") == "integer"

    def add_object(self, obj):
        super().add_object(obj)
        self._min = obj if self._min is None else min(self._min, obj)
        self._max = obj if self._max is None else max(self._max, obj)
        self._multiple_of = obj if self._multiple_of is None else gcd(self._multiple_of, obj)

    def add_schema(self, schema):
        super().add_schema(schema)
        if "minimum" in schema:
            val = schema["minimum"]
            self._min = val if self._min is None else min(self._min, val)
        if "maximum" in schema:
            val = schema["maximum"]
            self._max = val if self._max is None else max(self._max, val)
        if "multipleOf" in schema:
            val = int(schema["multipleOf"])
            self._multiple_of = val if self._multiple_of is None else gcd(self._multiple_of, val)

    def to_schema(self):
        schema = super().to_schema()
        if self._multiple_of is not None and self._multiple_of > 1:
            schema["multipleOf"] = self._multiple_of
        return schema
