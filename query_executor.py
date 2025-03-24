import logging
from typing import Optional

import psycopg2

logger = logging
logger.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%y/%m/%d %H:%M:%S",
    level=logger.INFO,
)


class SqlQueryExecutor:
    """A class for executing SQL queries using psycopg2.

    Attributes
        connection (psycopg2.connect): The database connection.
        cursor (psycopg2.cursor): The database cursor.
    """

    def __init__(self, db_properties: dict):
        """Initialize the SqlQueryExecutor instance.

        Args:
            db_properties: properties for the database connection.
        """
        self.__db_properties = db_properties
        self.connection = None

    def __is_connection_valid(self) -> bool:
        """Check if the existing connection is open and to the correct database."""
        return (self.connection is not None and
                self.connection.closed == 0 and
                self.connection.info.dbname == self.__db_properties["database"])

    def __return_conn(self) -> psycopg2.extensions.connection:
        if self.__is_connection_valid():
            return self.connection
        if self.connection is not None and self.connection.closed == 0:
            self.connection.close()

        self.connection = psycopg2.connect(**self.__db_properties)
        return self.connection

    def execute_query(self, query: str, params: Optional[tuple] = None) -> list[tuple] | None:
        """Execute a query.

        Args:
            query: The query to be executed.
            params: The parameters to be passed to the query
        """
        with self.__return_conn() as conn, conn.cursor() as cur:
            try:
                cur.execute(query, params)
                conn.commit()
            except psycopg2.Error:
                conn.rollback()
                logger.exception(f"Error executing query: {query}")

            if cur.description:
                return cur.fetchall()

        return None

    def read_columns(self, table_name: str, schema: str) -> list | None:
        """Read columns from the target postgres table."""
        return self.execute_query(f"""SELECT column_name, data_type
                               FROM information_schema.columns
                               WHERE table_name = '{table_name}'
                               AND table_schema = '{schema}';""")

def create_table():
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS crypto_data (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                symbol TEXT NOT NULL,
                current_price NUMERIC NOT NULL,
                price_change_percentage_24h NUMERIC NOT NULL,
                last_updated TIMESTAMP DEFAULT NOW()
            )
            """)
            conn.commit()


def save_to_db(data):
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            for coin in data:
                cur.execute("""
                INSERT INTO crypto_data (name, symbol, current_price, price_change_percentage_24h)
                VALUES (%s, %s, %s, %s)
                """, (coin["name"], coin["symbol"], coin["current_price"], coin["price_change_percentage_24h"]))
            conn.commit()


def analyze_data():
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT name, price_change_percentage_24h
            FROM crypto_data
            ORDER BY price_change_percentage_24h DESC
            LIMIT 1
            """)
            biggest_gainer = cur.fetchone()

            cur.execute("""
            SELECT name, price_change_percentage_24h
            FROM crypto_data
            ORDER BY price_change_percentage_24h ASC
            LIMIT 1
            """)
            biggest_loser = cur.fetchone()

    return {
        "biggest_gainer": {
            "name": biggest_gainer[0],
            "price_change": biggest_gainer[1]
        },
        "biggest_loser": {
            "name": biggest_loser[0],
            "price_change": biggest_loser[1]
        }
    }
