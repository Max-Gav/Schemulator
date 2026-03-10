
test_payloads = [
    # --- GROUP A: AUTHENTICATED USERS (Heavy Nesting) ---
    {
        "id": "u_01",
        "auth": {"method": "oauth", "provider": "google"},
        "profile": {"name": "Alice", "settings": {"theme": "dark", "lang": "en"}}
    },
    {
        "id": "u_02",
        "auth": {"method": "password"},
    },

    # --- GROUP B: LOG EVENTS (Common Top-level keys, different nested ones) ---
    {
        "id": "log_101",
        "timestamp": 1715600000,
        "event": "login_success",
        "metadata": {"ip": "1.1.1.1", "device": "mobile"}
    },
    {
        "id": "log_102",
        "timestamp": 1715600001,
        "event": "error_404",
        "metadata": {"url": "/api/v1/user", "code": 404} # Different metadata keys
    },

    # --- GROUP C: HARDWARE SENSORS (Flat but technical) ---
    {"id": "sensor_01", "reading": 22.5, "unit": "celsius", "status": "active", "hw_version": "v2.1"},
    {"id": "sensor_02", "reading": 45.0, "unit": "percent", "status": "active", "hw_version": "v2.1"},    {"id": "sensor_01", "reading": 22.5, "unit": "celsius", "status": "active", "hw_version": "v2.1"},

    # --- GROUP D: PRODUCT CATALOG (Mixed types) ---
    {"id": "prod_55", "sku": "SKU-99", "price": {"amount": 29.99, "currency": "USD"}, "tags": ["sale", "new"]},
    {"id": "prod_56", "price": {"amount": 15.00, "currency": "EUR"}, "tags": ["sale", "new", "test"]} # Missing tags
]
