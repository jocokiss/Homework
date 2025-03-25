# crypto_price_analyzer
from app.api_ingester import ApiIngest
from app.views import app


if __name__ == "__main__":
    ingest = ApiIngest()
    ingest.run()
    app.run(debug=True, host="0.0.0.0", port=5001)
