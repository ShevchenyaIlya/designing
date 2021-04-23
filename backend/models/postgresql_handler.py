import json
from typing import Dict, List, Optional, Tuple

import psycopg2
from psycopg2.extras import DictCursor


def load_database_connection_settings():
    """
    Load connection setting from json file in this directory
    """

    with open("db_connection_setting.json") as json_file:
        return json.load(json_file)


def database_connection(connection_settings: Dict):
    """
    Get connection to database from 'connection_settings'
    """

    return psycopg2.connect(**connection_settings)


def load_query(filename: str):
    """
    Load SQL query from files as text
    """

    with open(filename, "r") as sql_query:
        return sql_query.read()


def convert_row_to_dictionary(rows: List):
    for index, row in enumerate(rows):
        rows[index] = dict(row)

    return rows


# TODO: Change architecture of postgresql handler, split different tables logic to separate classes


class PostgreSQLHandler:
    _connection = None

    def __init__(self):
        self.cursor = self.connection.cursor(cursor_factory=DictCursor)
        self.sql_queries = {}

    def __del__(self):
        self.close_connection()

    def get_query(self, folder: str, query: str):
        """
        Loading SQL query from directory 'sql/'
        """

        if not self.sql_queries.get(query, False):
            self.sql_queries[query] = load_query(
                "".join([f"sql/{folder}/", query, ".sql"])
            )

        return self.sql_queries[query]

    def close_connection(self):
        self.connection.close()

    @classmethod
    def init_connection(cls):
        cls._connection = database_connection(load_database_connection_settings())

    @property
    def connection(self):
        if self._connection is None:
            self.init_connection()

        return self._connection
