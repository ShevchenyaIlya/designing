from typing import Dict, List, Optional, Tuple

from .postgresql_handler import PostgreSQLHandler, convert_row_to_dictionary


class GroupModel(PostgreSQLHandler):
    def select_groups(self) -> List[Dict]:
        self.cursor.execute(self.get_query("group", "select_groups"))
        groups = self.cursor.fetchall()

        return convert_row_to_dictionary(groups)

    def select_group_by_id(self, group_id: int) -> Optional[Dict]:
        self.cursor.execute(self.get_query("group", "select_group_by_id"), (group_id,))
        group = self.cursor.fetchone()

        if group is not None:
            return dict(group)

        return None

    def delete_group(self, identifier: int) -> bool:
        self.cursor.execute(self.get_query("group", "delete_group"), (identifier,))
        self.connection.commit()

        return bool(self.cursor.rowcount)

    def insert_group(self, group: Dict) -> int:
        if not self.group_exists(group["name"]):
            self.cursor.execute(
                self.get_query("group", "insert_group"),
                (
                    group["name"],
                    group["description"],
                ),
            )
            self.connection.commit()

            return self.cursor.fetchone()[0]

    def update_group(self, group_id: int, group: Dict) -> bool:
        self.cursor.execute(
            self.get_query("group", "update_group"),
            (
                group.get("name", None),
                group.get("description", None),
                group_id,
            ),
        )

        self.connection.commit()

        return bool(self.cursor.rowcount)

    def group_exists(self, name: str) -> bool:
        self.cursor.execute(self.get_query("group", "group_exists"), (name,))
        return self.cursor.fetchall()[0][0]

    def insert_group_role(self, group_id: int, role_id: int):
        self.cursor.execute(
            self.get_query("group_role", "insert_group_role"),
            (group_id, role_id),
        )
        self.connection.commit()

        return self.cursor.fetchone()[0]

    def delete_group_role(self, group_id: int, role_id: int):
        self.cursor.execute(
            self.get_query("group_role", "delete_group_role"), (group_id, role_id)
        )
        self.connection.commit()

        return bool(self.cursor.rowcount)

    def select_group_roles(self, group_id: int):
        self.cursor.execute(
            self.get_query("group_role", "select_group_roles"), (group_id,)
        )
        roles = self.cursor.fetchall()

        for index, role in enumerate(roles):
            roles[index] = dict(role)

        return roles

    def select_users_in_group(self, group_id: int):
        self.cursor.execute(
            self.get_query("user_group", "select_users_in_group"), (group_id,)
        )
        users = self.cursor.fetchall()

        for index, user in enumerate(users):
            users[index] = dict(user)

        return users


groups = GroupModel()
