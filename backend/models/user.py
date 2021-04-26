from typing import Dict, List, Optional, Tuple

from .postgresql_handler import PostgreSQLHandler


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

    def insert_user_role(self, user_id: int, role_id: int):
        self.cursor.execute(
            self.get_query("user_role", "insert_user_role"),
            (user_id, role_id),
        )
        self.connection.commit()

        return self.cursor.fetchone()[0]

    def delete_user_role(self, user_id: int, role_id: int):
        self.cursor.execute(
            self.get_query("user_role", "delete_user_role"), (user_id, role_id)
        )
        self.connection.commit()

        return bool(self.cursor.rowcount)

    def select_user_roles(self, user_id: int):
        self.cursor.execute(
            self.get_query("user_role", "select_user_roles"), (user_id,)
        )
        roles = self.cursor.fetchall()

        for index, role in enumerate(roles):
            roles[index] = dict(role)

        return roles

    def insert_user_group(self, user_id: int, group_id: int):
        self.cursor.execute(
            self.get_query("user_group", "insert_user_group"),
            (group_id, user_id),
        )
        self.connection.commit()

        return self.cursor.fetchone()[0]

    def delete_user_group(self, user_id: int, group_id: int):
        self.cursor.execute(
            self.get_query("user_group", "delete_user_group"), (user_id, group_id)
        )
        self.connection.commit()

        return bool(self.cursor.rowcount)

    def select_user_groups(self, user_id: int):
        self.cursor.execute(
            self.get_query("user_group", "select_user_groups"), (user_id,)
        )
        roles = self.cursor.fetchall()

        for index, role in enumerate(roles):
            roles[index] = dict(role)

        return roles

    def select_user_policies(self, user_id: int):
        self.cursor.execute(self.get_query("user", "select_user_policies"), (user_id,))
        policies = self.cursor.fetchall()

        for index, policy in enumerate(policies):
            policies[index] = dict(policy)

        return policies


users = UserModel()
