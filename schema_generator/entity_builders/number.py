from genson.schema.strategies import Number


class SchemaNumber(Number):
    KEYWORDS = (*Number.KEYWORDS, "minimum", "maximum")

    def __init__(self, node_class):
        super().__init__(node_class)
        self._min = None
        self._max = None

    def add_object(self, obj):
        super().add_object(obj)
        self._min = obj if self._min is None else min(self._min, obj)
        self._max = obj if self._max is None else max(self._max, obj)

    def add_schema(self, schema):
        super().add_schema(schema)
        if "minimum" in schema:
            val = schema["minimum"]
            self._min = val if self._min is None else min(self._min, val)
        if "maximum" in schema:
            val = schema["maximum"]
            self._max = val if self._max is None else max(self._max, val)

    def to_schema(self):
        schema = super().to_schema()
        if self._min is not None:
            schema["minimum"] = self._min
        if self._max is not None:
            schema["maximum"] = self._max
        return schema
