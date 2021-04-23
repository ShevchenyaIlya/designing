import json
from typing import Dict, List, Optional, Tuple

import psycopg2
from psycopg2.extensions import AsIs
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


class UserModel(PostgreSQLHandler):
    def user_exist(self, email: str) -> bool:
        self.cursor.execute(self.get_query("user", "user_exists"), (email,))
        return self.cursor.fetchall()[0][0]

    def insert_user(self, user: Dict) -> int:
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

    def select_user(self, email: str) -> Dict:
        self.cursor.execute(self.get_query("user", "select_user"), (email,))
        user = dict(self.cursor.fetchone())
        user.pop("password", None)
        user.pop("id", None)

        return user

    def select_users(self) -> List[Dict]:
        self.cursor.execute(self.get_query("user", "select_users"))
        users = self.cursor.fetchall()

        for index, user in enumerate(users):
            users[index] = dict(user)

        return users

    def delete_user(self, email: str) -> bool:
        self.cursor.execute(self.get_query("user", "delete_user"), (email,))
        self.connection.commit()

        return bool(self.cursor.rowcount)

    def update_user(self, user: Dict) -> bool:
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

    def find_user_by_email(self, email: str) -> Optional[Tuple[int, str]]:
        self.cursor.execute(self.get_query("user", "select_user"), (email,))
        response = self.cursor.fetchone()

        if response is None:
            return response

        return response[0], response["password"]


class DepartmentModel(PostgreSQLHandler):
    def select_departments(self) -> List[Dict]:
        self.cursor.execute(self.get_query("department", "select_departments"))
        departments = self.cursor.fetchall()

        return convert_row_to_dictionary(departments)

    def select_department_by_name(self, name: str):
        self.cursor.execute(
            self.get_query("department", "select_department_by_name"), (name,)
        )
        department = dict(self.cursor.fetchone())

        return department

    def select_department_by_id(self, department_id: int) -> Optional[Dict]:
        self.cursor.execute(
            self.get_query("department", "select_department_by_id"), (department_id,)
        )
        department = self.cursor.fetchone()

        if department is not None:
            return dict(department)

        return None

    def delete_department(self, identifier: str) -> bool:
        self.cursor.execute(
            self.get_query("department", "delete_department"), (identifier,)
        )
        self.connection.commit()

        return bool(self.cursor.rowcount)

    def insert_department(self, department: Dict) -> int:
        if not self.department_exists(department["name"]):
            self.cursor.execute(
                self.get_query("department", "insert_department"),
                (
                    department["name"],
                    department["description"],
                    department["head_id"],
                ),
            )
            self.connection.commit()

            return self.cursor.fetchone()[0]

    def update_department(self, department_id, department) -> bool:
        self.cursor.execute(
            self.get_query("department", "update_department"),
            (
                department.get("name", None),
                department.get("description", None),
                department.get("head_id", None),
                department_id,
            ),
        )

        self.connection.commit()

        return bool(self.cursor.rowcount)

    def department_exists(self, name: str) -> bool:
        self.cursor.execute(self.get_query("department", "department_exists"), (name,))
        return self.cursor.fetchall()[0][0]


users = UserModel()
departments = DepartmentModel()
