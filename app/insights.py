from config import DB_CONFIG
from app.query_executor import SqlQueryExecutor
from logging_helper import LoggingHelper


class Insights(LoggingHelper):
    def __init__(self):
        self.query_executor = SqlQueryExecutor(DB_CONFIG)

    def get_biggest_gainer(self) -> dict:
        """Return the cryptocurrency with the largest 24h price increase."""
        query = """
            SELECT name, price_change_percentage_24h
            FROM crypto_data
            ORDER BY price_change_percentage_24h DESC
            LIMIT 1;
        """

        if result := self.query_executor.execute_query(query):
            return {"name": result[0][0], "price_change_percentage": result[0][1]}
        return {}

    def get_biggest_loser(self) -> dict:
        """Return the cryptocurrency with the largest 24h price decrease."""
        query = """
            SELECT name, price_change_percentage_24h
            FROM crypto_data
            ORDER BY price_change_percentage_24h ASC
            LIMIT 1;
        """

        if result := self.query_executor.execute_query(query):
            return {"name": result[0][0], "price_change_percentage": result[0][1]}
        return {}

    def get_most_volatile(self) -> dict:
        """Return the most volatile cryptocurrency based on the 24h price range."""
        query = """
            SELECT name, high_24h, low_24h
            FROM crypto_data
            ORDER BY (high_24h - low_24h) DESC
            LIMIT 1;
        """

        if result := self.query_executor.execute_query(query):
            name = result[0][0]
            high_24h = result[0][1]
            low_24h = result[0][2]
            absolute_volatility = high_24h - low_24h
            percentage_volatility = (absolute_volatility / high_24h) * 100
            return {
                "name": name,
                "high_24h": high_24h,
                "low_24h": low_24h,
                "absolute_volatility": absolute_volatility,
                "percentage_volatility": f"{percentage_volatility:.2f}%",
            }
        return {}

    def get_volatility_to_market_cap_ratio(self) -> dict:
        query = """
                    SELECT 
                        name, 
                        (high_24h - low_24h) / market_cap AS get_volatility_to_market_cap_ratio
                    FROM 
                        crypto_data
                    WHERE 
                        market_cap > 0
                    ORDER BY 
                        get_volatility_to_market_cap_ratio DESC
                    LIMIT 1;
                """

        if result := self.query_executor.execute_query(query):
            return {"name": result[0][0], "volatility_to_market_cap_ratio": result[0][1]}
        return {}

    def get_biggest_market_cap_growth(self) -> dict:
        """Return the cryptocurrency with the largest market cap growth."""
        query = """
            SELECT name, market_cap_change_percentage_24h
            FROM crypto_data
            ORDER BY market_cap_change_percentage_24h DESC
            LIMIT 1;
        """

        if result := self.query_executor.execute_query(query):
            return {
                "name": result[0][0],
                "market_cap_change_percentage": result[0][1]
            }
        return {}


