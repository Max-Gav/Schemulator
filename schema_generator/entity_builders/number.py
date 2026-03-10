from math import gcd
from decimal import Decimal
from genson.schema.strategies import Number


def float_gcd(a, b):
    """
    Finds the GCD of two floats by scaling them to integers using
    their maximum decimal precision, computing integer GCD, then scaling back.

    e.g. float_gcd(0.3, 0.2) -> gcd(3, 2) / 10 -> 0.1
    """

    def decimal_places(x):
        return abs(Decimal(str(x)).as_tuple().exponent)

    precision = max(decimal_places(a), decimal_places(b))
    scale = 10 ** precision
    return gcd(round(a * scale), round(b * scale)) / scale


class SchemaNumber(Number):
    KEYWORDS = (*Number.KEYWORDS, "minimum", "maximum", "multipleOf")

    def __init__(self, node_class):
        super().__init__(node_class)
        self._min = None
        self._max = None
        self._multiple_of = None

    @classmethod
    def match_object(cls, obj):
        return isinstance(obj, float)

    @classmethod
    def match_schema(cls, schema):
        return schema.get("type") == "number"

    def add_object(self, obj):
        super().add_object(obj)
        self._min = obj if self._min is None else min(self._min, obj)
        self._max = obj if self._max is None else max(self._max, obj)
        self._multiple_of = obj if self._multiple_of is None else float_gcd(self._multiple_of, obj)

    def add_schema(self, schema):
        super().add_schema(schema)
        if "minimum" in schema:
            val = schema["minimum"]
            self._min = val if self._min is None else min(self._min, val)
        if "maximum" in schema:
            val = schema["maximum"]
            self._max = val if self._max is None else max(self._max, val)
        if "multipleOf" in schema:
            val = schema["multipleOf"]
            if isinstance(val, float):
                self._multiple_of = val if self._multiple_of is None else float_gcd(self._multiple_of, val)

    def to_schema(self):
        schema = super().to_schema()
        if self._min is not None:
            schema["minimum"] = self._min
        if self._max is not None:
            schema["maximum"] = self._max
        if (self._multiple_of is not None
                and not isinstance(self._multiple_of, int)
                and self._multiple_of > 1e-10):
            schema["multipleOf"] = self._multiple_of
        return schema
