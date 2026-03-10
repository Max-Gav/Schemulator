from genson import SchemaBuilder

from schema_generator.entity_builders import SchemaObject, SchemaInteger
from schema_generator.entity_builders.list import SchemaList
from schema_generator.entity_builders.number import SchemaNumber
from schema_generator.entity_builders.string import SchemaString


class SchemaGenerator(SchemaBuilder):
    EXTRA_STRATEGIES = (SchemaList, SchemaNumber, SchemaString, SchemaObject, SchemaInteger)
