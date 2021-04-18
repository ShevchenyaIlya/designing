import json

import psycopg2
from psycopg2.extensions import AsIs
from psycopg2.extras import DictCursor


def load_database_connection_settings():
    """
    Load connection setting from json file in this directory
    """

    with open("db_connection_setting.json") as json_file:
        return json.load(json_file)


def database_connection(connection_settings):
    """
    Get connection to database from 'connection_settings'
    """

    return psycopg2.connect(**connection_settings)


def load_query(filename):
    """
    Load SQL query from files as text
    """

    with open(filename, "r") as sql_query:
        return sql_query.read()


class PostgreSQLHandler:
    def __init__(self):
        self.connection = database_connection(load_database_connection_settings())
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

    def user_exist(self, email):
        self.cursor.execute(self.get_query("user", "user_exists"), (email,))
        return self.cursor.fetchall()[0][0]

    def insert_user(self, user):
        if not self.user_exist(user["email"]):
            self.cursor.execute(
                self.get_query("user", "insert_user"),
                (
                    user["first_name"],
                    user["last_name"],
                    user["middle_name"],
                    user["email"],
                    user["password"],
                ),
            )
            self.connection.commit()

            return self.cursor.fetchone()[0]

    def select_user(self, email):
        self.cursor.execute(self.get_query("user", "select_user"), (email,))
        user = dict(self.cursor.fetchone())
        user.pop("password", None)
        user.pop("user_id", None)

        return user

    def select_users(self):
        self.cursor.execute(self.get_query("user", "select_users"))
        users = self.cursor.fetchall()

        for index, user in enumerate(users):
            users[index] = dict(user)

        return users

    def delete_user(self, email):
        self.cursor.execute(self.get_query("user", "delete_user"), (email,))
        self.connection.commit()

        return bool(self.cursor.rowcount)

    def update_user(self, user):
        self.cursor.execute(
            self.get_query("user", "update_user"),
            (
                user.get("first_name", None),
                user.get("last_name", None),
                user.get("middle_name", None),
                user.get("department_id", None),
                user.get("unit_id", None),
                user.get("position_id", None),
                user["email"],
            ),
        )

        self.connection.commit()

        return bool(self.cursor.rowcount)

    def find_user_by_email(self, email):
        self.cursor.execute(self.get_query("user", "select_user"), (email,))
        response = self.cursor.fetchone()

        if response is None:
            return response

        return response["user_id"], response["password"]

    def close_connection(self):
        self.connection.close()


DATABASE = PostgreSQLHandler()
