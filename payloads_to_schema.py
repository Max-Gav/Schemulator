from schema_generator.schema_generator import SchemaGenerator


def generate_draft4_schema(grouped_results):
    schema = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "definitions": {},
        "properties": {}
    }

    for cluster_id, items in grouped_results.items():
        definition_name = f"Group_{cluster_id}"

        builder = SchemaGenerator()
        for item in items:
            builder.add_object(item)

        cluster_schema = builder.to_schema()
        cluster_schema.pop("$schema", None)

        schema["definitions"][definition_name] = cluster_schema
        schema["properties"][f"data_type_{cluster_id}"] = {
            "$ref": f"#/definitions/{definition_name}"
        }

    return schema