"""Module containing constants used throughout the project."""

COINGECKO_API_URL = "https://api.coingecko.com/api/v3/coins/markets"

FETCH_PARAMS = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
        "sparkline": False
    }

DB_CONFIG = {
    "dbname": "crypto_db",
    "user": "crypto_user",
    "password": "crypto_pass",
    "host": "db",
    "port": 5432
}
