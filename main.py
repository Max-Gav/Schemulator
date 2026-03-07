import json

from group_payloads import group_json_payloads
from payloads_to_schema import generate_draft4_schema
from test import test_payloads

results = group_json_payloads(test_payloads)
final_draft4_schema = generate_draft4_schema(results)
print(json.dumps(final_draft4_schema, indent=2))

for cluster_id, items in results.items():
    print(f"Group {cluster_id}:")
    for item in items:
        print(f"  {item}")
    print("-" * 30)
