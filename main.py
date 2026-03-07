import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from kneed import KneeLocator  # Optional: helps pick the "Elbow" point automatically

from payloads_to_schema import generate_draft4_schema

#
# from create_schema import generate_definitions_from_clusters
# from test_payloads import test_payloads

test_payloads = [
    # Cluster A: User Profiles
    {"id": 1, "username": "alpha_user", "email": "a@test.com", "active": True},
    {"id": 2, "username": "beta_tester", "email": "b@test.com", "bio": "Hello world"},

    # Cluster B: E-commerce Orders
    {"order_id": 101, "total_price": 50.00, "currency": "USD", "items": ["book", "pen"]},
    {"order_id": 102, "total_price": 25.50, "currency": "EUR", "discount_code": "SAVE10"},

    # Cluster C: Product Inventory
    {"sku": "SKU-99", "weight_kg": 1.2},
    {"sku": "SKU-100", "stock_level": 12, "warehouse_loc": "B4", "restock_date": "2024-12-01"}
]
def group_json_payloads(data):
    # STEP 1: Pre-processing
    # Extract keys and turn them into "sentences" for the Vectorizer
    # Result: "id order_id total", "id username email", etc.
    key_strings = [" ".join(obj.keys()) for obj in data]

    # STEP 2: Weighting with TF-IDF
    # This automatically gives high weight to unique keys (emp_id)
    # and low weight to common ones (id)
    vectorizer = TfidfVectorizer()
    weighted_matrix = vectorizer.fit_transform(key_strings)

    # STEP 3: The Elbow Method (Find the best number of clusters)
    # We try a range from 1 to the total number of items
    max_k = min(len(data), 15)
    inertia = []
    for k in range(1, max_k + 1):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(weighted_matrix)
        inertia.append(kmeans.inertia_)

    # Automatically find the "Elbow" point
    # If you don't have 'kneed' installed, you can just set k=3 based on logic
    try:
        kn = KneeLocator(range(1, max_k + 1), inertia, curve='convex', direction='decreasing', S=0.5)
        optimal_k = kn.elbow if kn.elbow else 3
    except:
        optimal_k = 3  # Fallback if library is missing

    print(f"--- Detected {optimal_k} unique JSON types ---\n")

    # STEP 4: Final Clustering
    model = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
    clusters = model.fit_predict(weighted_matrix)

    # STEP 5: Organize Results
    grouped_results = {}
    for idx, cluster_id in enumerate(clusters):
        if cluster_id not in grouped_results:
            grouped_results[cluster_id] = []
        grouped_results[cluster_id].append(data[idx])

    return grouped_results


# EXECUTION
results = group_json_payloads(test_payloads)
# Assuming 'results' is the output from your group_json_payloads(test_payloads)
final_draft4_schema = generate_draft4_schema(results)
print(json.dumps(final_draft4_schema, indent=2))

# Output the result
# print(json.dumps(final_draft4_schema, indent=2))
for cluster_id, items in results.items():
    print(f"Group {cluster_id}:")
    for item in items:
        print(f"  {item}")
    print("-" * 30)
