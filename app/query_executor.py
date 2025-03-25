from typing import Optional, Union

import psycopg2

from logging_helper import LoggingHelper


class SqlQueryExecutor(LoggingHelper):
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
                self.connection.info.dbname == self.__db_properties["dbname"])

    def __return_conn(self) -> psycopg2.extensions.connection:
        if self.__is_connection_valid():
            return self.connection

        self.connection = psycopg2.connect(**self.__db_properties)
        return self.connection

    def execute_query(self, query: str, params: Optional[tuple] = None) -> Union[list[tuple], None]:
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
                self.logger.exception(f"Error executing query: {query}")

            if cur.description:
                return cur.fetchall()

        return None
