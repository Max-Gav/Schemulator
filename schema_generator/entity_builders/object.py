from genson.schema.strategies import Object


class SchemaObject(Object):
    KEYWORDS = (*Object.KEYWORDS, "minProperties", "maxProperties")

    def __init__(self, node_class):
        super().__init__(node_class)
        self._min = None
        self._max = None

    def add_object(self, obj):
        super().add_object(obj)
        count = len(obj)
        self._min = count if self._min is None else min(self._min, count)
        self._max = count if self._max is None else max(self._max, count)

    def add_schema(self, schema):
        super().add_schema(schema)
        if "minProperties" in schema:
            val = schema["minProperties"]
            self._min = val if self._min is None else min(self._min, val)
        if "maxProperties" in schema:
            val = schema["maxProperties"]
            self._max = val if self._max is None else max(self._max, val)

    def to_schema(self):
        schema = super().to_schema()
        if self._min is not None:
            schema["minProperties"] = self._min
        if self._max is not None:
            schema["maxProperties"] = self._max
        return schema