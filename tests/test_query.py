"""Unit tests for query_executor.py."""
from unittest.mock import MagicMock, PropertyMock, patch

import psycopg2
import pytest

from app.query_executor import SqlQueryExecutor


@pytest.fixture
def mock_sql_query_executor():
    """Create a MockPsychoUtils object."""

    class MockSqlQueryExecutor(SqlQueryExecutor):
        """Mock SqlQueryExecutor."""

        def __init__(self):
            self._SqlQueryExecutor__db_properties = {
                "dbname": "test_database",
                "host": "test_server",
                "port": 5432,
                "user": "test_user",
                "password": "test_password",
            }
            self.connection = MagicMock()

    return MockSqlQueryExecutor()


@pytest.mark.parametrize(("connection", "connection_closed", "connection_info_db", "expected_result"), [
    (MagicMock(), 0, "test_database", True),        # Connection exists and open, to the right database
    (MagicMock(), 1, "test_database", False),       # Connection exists but CLOSED, to the right database
    (MagicMock(), 0, "test", False),                # Connection exists and open, to the WRONG database
    (None, "", "", False),                          # Connection DOES NOT EXIST
])
def test_is_connection_valid(mock_sql_query_executor,
                     connection, connection_closed, connection_info_db, expected_result):
    """Test the return_conn function."""
    mock_sql_query_executor.connection = connection
    if connection is not None:
        type(mock_sql_query_executor.connection).closed = PropertyMock(return_value=connection_closed)
        type(mock_sql_query_executor.connection).info = MagicMock()
        type(mock_sql_query_executor.connection.info).dbname = PropertyMock(return_value=connection_info_db)

    result = mock_sql_query_executor._SqlQueryExecutor__is_connection_valid()
    assert result == expected_result


@patch("psycopg2.connect")
def test_execute_query(mock_connect, mock_sql_query_executor):
    """Test the execute_query function under normal conditions."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    # Simulate query execution with returned results
    query = "SELECT * FROM my_table"
    params = None
    mock_cursor.description = [("column1",)]
    mock_cursor.fetchall.return_value = [("value1",)]

    # Execute the method
    result = mock_sql_query_executor.execute_query(query, params)

    # Assertions
    mock_connect.assert_called_once_with(**mock_sql_query_executor._SqlQueryExecutor__db_properties)
    mock_cursor.execute.assert_called_once_with(query, params)
    mock_conn.commit.assert_called_once()
    assert result == [("value1",)]


def test_execute_query_failing(mock_sql_query_executor):
    """Test the execute_query function with an error."""
    query = "definitely not a valid query whatsoever"
    with patch("psycopg2.connect", side_effect=psycopg2.Error("Mocked psycopg2 error")), pytest.raises(psycopg2.Error):
        mock_sql_query_executor.execute_query(query)
