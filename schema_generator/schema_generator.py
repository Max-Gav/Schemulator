from genson import SchemaBuilder

from schema_generator.entity_builders.list import SchemaList
from schema_generator.entity_builders.number import SchemaNumber


class SchemaGenerator(SchemaBuilder):
    EXTRA_STRATEGIES = (SchemaList, SchemaNumber)
