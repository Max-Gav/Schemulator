from genson.schema.strategies import List


class SchemaList(List):
    """
    Extends Genson's built-in List strategy to track minItems / maxItems
    from observed payloads as the schema is being built.

    Add more array-level keywords here without touching anything else.
    """
    KEYWORDS = (*List.KEYWORDS, "minItems", "maxItems")

    def __init__(self, node_class):
        super().__init__(node_class)
        self._min = None
        self._max = None

    def add_object(self, obj):
        super().add_object(obj)
        length = len(obj)
        self._min = length if self._min is None else min(self._min, length)
        self._max = length if self._max is None else max(self._max, length)

    def add_schema(self, schema):
        super().add_schema(schema)
        if "minItems" in schema:
            val = schema["minItems"]
            self._min = val if self._min is None else min(self._min, val)
        if "maxItems" in schema:
            val = schema["maxItems"]
            self._max = val if self._max is None else max(self._max, val)

    def to_schema(self):
        schema = super().to_schema()
        if self._min is not None:
            schema["minItems"] = self._min
        if self._max is not None:
            schema["maxItems"] = self._max
        return schema
