

def generate_draft4_schema(grouped_results):
    """
    Takes grouped JSON objects and creates a Draft 4 Schema
    with a definition for each group.
    """
    schema = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "definitions": {},
        "properties": {}
    }

    for cluster_id, items in grouped_results.items():
        # Create a name for the definition (e.g., Group_0)
        definition_name = f"Group_{cluster_id}"

        # Analyze the structure of the first item in the group
        # (Assuming items in a cluster share the same keys)
        properties = {}
        required = []

        # We aggregate keys from ALL items in the cluster to find optional vs required
        all_keys = set().union(*(item.keys() for item in items))

        for key in all_keys:
            # Determine the type based on the first occurrence of the key
            sample_value = next(item[key] for item in items if key in item)

            # Map Python types to JSON Schema types
            python_to_json_type = {
                str: "string",
                int: "integer",
                float: "number",
                bool: "boolean",
                list: "array",
                dict: "object"
            }

            json_type = python_to_json_type.get(type(sample_value), "string")
            properties[key] = {"type": json_type}

            # If the key exists in EVERY item of the cluster, it is 'required'
            if all(key in item for item in items):
                required.append(key)

        # Build the definition for this cluster
        schema["definitions"][definition_name] = {
            "type": "object",
            "properties": properties,
            "required": required
        }

        # Add a reference to the main properties for visibility
        schema["properties"][f"data_type_{cluster_id}"] = {
            "$ref": f"#/definitions/{definition_name}"
        }

    return schema