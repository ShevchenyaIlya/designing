import logging
from typing import Dict, List, Optional, Tuple, Union

from enums import TransactionResult
from psycopg2 import Error

from .postgresql_handler import PostgreSQLHandler, convert_row_to_dictionary

LOG = logging.getLogger(__name__)


class RoleModel(PostgreSQLHandler):
    def select_roles(self) -> List[Dict]:
        self.cursor.execute(self.get_query("role", "select_roles"))
        roles = self.cursor.fetchall()

        return convert_row_to_dictionary(roles)

    def select_role_by_id(self, role_id: int) -> Optional[Dict]:
        self.cursor.execute(self.get_query("role", "select_role_by_id"), (role_id,))
        role = self.cursor.fetchone()

        if role is not None:
            return dict(role)

        return None

    def select_users_with_role(self, role_id: int) -> List[Dict]:
        self.cursor.execute(
            self.get_query("user_role", "select_users_with_role"), (role_id,)
        )
        users = self.cursor.fetchall()

        for index, user in enumerate(users):
            users[index] = dict(user)
            users[index]["register_date"] = str(users[index]["register_date"])

        return users

    def select_roles_with_policy(self, policy_id: int) -> List[Dict]:
        self.cursor.execute(
            self.get_query("role_policy", "select_roles_with_policy"), (policy_id,)
        )
        roles = self.cursor.fetchall()

        for index, role in enumerate(roles):
            roles[index] = dict(role)

        return roles

    def select_single_role(self, identifier: int) -> Optional[Dict]:
        self.cursor.execute(self.get_query("role", "select_single_role"), (identifier,))
        role = self.cursor.fetchone()

        if role is not None:
            return dict(role)

        return None

    def delete_role(self, identifier: int) -> bool:
        self.cursor.execute(self.get_query("role", "delete_role"), (identifier,))
        self.connection.commit()

        return bool(self.cursor.rowcount)

    def insert_role(self, role: Dict) -> Union[int, TransactionResult]:
        if not self.role_exists(role["name"]):
            try:
                self.cursor.execute(
                    self.get_query("role", "insert_role"),
                    (
                        role["name"],
                        role["description"],
                    ),
                )
            except Error as error:
                LOG.debug(error)

                self.connection.rollback()
                return TransactionResult.ERROR
            else:
                self.connection.commit()
                return self.cursor.fetchone()[0]

        return TransactionResult.SUCCESS

    def update_role(self, role_id: int, role: Dict) -> Optional[bool]:
        try:
            self.cursor.execute(
                self.get_query("role", "update_role"),
                (
                    role.get("name", None),
                    role.get("description", None),
                    role_id,
                ),
            )
        except Error as error:
            LOG.debug(error)
            self.connection.rollback()
        else:
            self.connection.commit()
            return bool(self.cursor.rowcount)

    def role_exists(self, name: str) -> bool:
        self.cursor.execute(self.get_query("role", "role_exists"), (name,))
        return self.cursor.fetchall()[0][0]

    def insert_role_policy(self, body: Dict) -> Optional[bool]:
        try:
            self.cursor.execute(
                self.get_query("role_policy", "insert_role_policy"),
                (body["role_id"], body["policy_id"], body["department_id"]),
            )
        except Error as error:
            LOG.debug(error)
            self.connection.rollback()
        else:
            self.connection.commit()
            return self.cursor.fetchone()[0]

    def delete_role_policy(self, body: Dict) -> Optional[bool]:
        try:
            self.cursor.execute(
                self.get_query("role_policy", "delete_user_group"),
                (body["role_id"], body["policy_id"], body["department_id"]),
            )
        except Error as error:
            LOG.debug(error)
            self.connection.rollback()
        else:
            self.connection.commit()
            return bool(self.cursor.rowcount)

    def select_role_policies(self, role_id: int) -> List[Dict]:
        self.cursor.execute(
            self.get_query("role_policy", "select_role_policies"), (role_id,)
        )
        policies = self.cursor.fetchall()

        for index, policy in enumerate(policies):
            policies[index] = dict(policy)

        return policies


roles = RoleModel()
