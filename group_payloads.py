from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from kneed import KneeLocator


def flatten_keys(d, parent_key='', sep='.'):
    """Recursively flattens nested JSON keys."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_keys(v, new_key, sep=sep).split())
        else:
            items.append(new_key)
    return " ".join(items)


def group_json_payloads(data):
    if not data: return {}

    # --- STEP 1: HASHING & FLATTENING ---
    # We turn 1,000 JSONs into only the UNIQUE structures found.
    structure_map = {}
    for obj in data:
        # Flatten nested keys so 'user': {'id': 1} becomes 'user.id'
        flat_key_string = flatten_keys(obj)
        # Sort so that order doesn't matter
        fingerprint = " ".join(sorted(flat_key_string.split()))

        if fingerprint not in structure_map:
            structure_map[fingerprint] = []
        structure_map[fingerprint].append(obj)

    unique_key_strings = list(structure_map.keys())
    unique_keys = len(unique_key_strings)

    # --- STEP 2: TF-IDF VECTORIZATION ---
    vectorizer = TfidfVectorizer(binary=True,
                                 token_pattern=r"(?u)\b\w[\w.]*\b",
                                 max_df=0.9,
                                 stop_words=["id", "_id", "uuid"])
    weighted_matrix = vectorizer.fit_transform(unique_key_strings)

    # --- STEP 3: THE SAFETY GATE & ELBOW METHOD ---
    # Logic: You can't find an "elbow" if you have fewer than 3 unique types.
    if unique_keys <= 2:
        optimal_k = unique_keys
    else:
        max_k = min(unique_keys, 10)
        inertia = []
        k_range = range(1, max_k + 1)

        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(weighted_matrix)
            inertia.append(kmeans.inertia_)

        try:
            # S=1.0 is the "Standard" sensitivity.
            # Convex/Decreasing matches the shape of an Inertia graph.
            kn = KneeLocator(list(k_range), inertia, curve='convex', direction='decreasing', S=0.5)
            optimal_k = kn.elbow if kn.elbow else 2
        except:
            optimal_k = 2

    # --- STEP 4: FINAL CLUSTERING ---
    model = KMeans(n_clusters=optimal_k, random_state=42)
    labels = model.fit_predict(weighted_matrix)

    # --- STEP 5: RE-ASSEMBLY ---
    grouped_results = {}
    for idx, label in enumerate(labels):
        if label not in grouped_results:
            grouped_results[label] = []
        fingerprint = unique_key_strings[idx]
        grouped_results[label].extend(structure_map[fingerprint])

    return grouped_results
