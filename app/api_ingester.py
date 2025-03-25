from typing import Union

import requests

from app.query_executor import SqlQueryExecutor
from config import FETCH_PARAMS, DB_CONFIG, COINGECKO_API_URL
from logging_helper import LoggingHelper


class ApiIngest(LoggingHelper):
    def __init__(self):
        # Initialize the query executor with DB configuration
        self.query_executor = SqlQueryExecutor()
        self.__create_db()

    def __create_db(self) -> None:
        """Create the crypto_data table if it doesn't already exist."""
        self.query_executor.execute_query("""
            DROP TABLE IF EXISTS crypto_data;
            
            CREATE TABLE crypto_data (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                symbol TEXT NOT NULL,
                current_price NUMERIC NOT NULL,
                price_change_percentage_24h NUMERIC NOT NULL,
                market_cap NUMERIC NOT NULL,
                market_cap_rank INTEGER NOT NULL,
                market_cap_change_percentage_24h INTEGER NOT NULL,
                ath NUMERIC NOT NULL,
                atl NUMERIC NOT NULL,
                high_24h NUMERIC NOT NULL,
                low_24h NUMERIC NOT NULL,
                last_updated TIMESTAMP DEFAULT NOW()
            );
        """)

    @staticmethod
    def __fetch_data(api_url: str, params: dict = None) -> Union[dict, list]:
        """Fetch data from the CoinGecko API."""
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return []

    def __save_to_db(self, data: dict) -> None:
        """Save the fetched data into the database."""
        for entry in data:
            self.query_executor.execute_query(
                """
                INSERT INTO crypto_data (
                    name, 
                    symbol, 
                    current_price, 
                    price_change_percentage_24h,
                    market_cap,
                    market_cap_rank,
                    market_cap_change_percentage_24h,
                    ath,
                    atl,
                    high_24h,
                    low_24h
                ) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    entry["name"],
                    entry["symbol"],
                    entry["current_price"],
                    entry["price_change_percentage_24h"],
                    entry["market_cap"],
                    entry["market_cap_rank"],
                    entry["market_cap_change_percentage_24h"],
                    entry["ath"],
                    entry["atl"],
                    entry["high_24h"],
                    entry["low_24h"]
                )
            )

    def run(self):
        """Fetch data from the API and save it to the database."""
        self.logger.info("Starting API Ingestion")
        if data := self.__fetch_data(COINGECKO_API_URL, FETCH_PARAMS):
            self.__save_to_db(data)
            self.logger.info("Ingestion completed.")

        else:
            self.logger.info("No data was fetched from the API.")
