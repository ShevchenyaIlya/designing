from typing import Dict, List, Optional, Union

from enums import TransactionResult
from psycopg2 import Error

from .postgresql_handler import PostgreSQLHandler, convert_row_to_dictionary


class PolicyModel(PostgreSQLHandler):
    def select_policies(self) -> List[Dict]:
        self.cursor.execute(self.get_query("policy", "select_policies"))
        policies = self.cursor.fetchall()

        return convert_row_to_dictionary(policies)

    def select_policy_by_id(self, policy_id: int) -> Optional[Dict]:
        self.cursor.execute(
            self.get_query("policy", "select_policy_by_id"), (policy_id,)
        )
        policy = self.cursor.fetchone()

        if policy is not None:
            return dict(policy)

        return None

    def delete_policy(self, identifier: int) -> bool:
        self.cursor.execute(self.get_query("policy", "delete_policy"), (identifier,))
        self.connection.commit()

        return bool(self.cursor.rowcount)

    def insert_policy(self, policy: Dict) -> Union[int, TransactionResult]:
        if not self.policy_exists(policy["title"]):
            try:
                self.cursor.execute(
                    self.get_query("policy", "insert_policy"),
                    (
                        policy["title"],
                        policy["description"],
                        policy["is_administrative"],
                    ),
                )
            except Error:
                self.connection.rollback()
                return TransactionResult.ERROR
            else:
                self.connection.commit()
                return self.cursor.fetchone()[0]

        return TransactionResult.SUCCESS

    def update_policy(self, policy_id: int, policy: Dict) -> Optional[bool]:
        try:
            self.cursor.execute(
                self.get_query("policy", "update_policy"),
                (
                    policy.get("title", None),
                    policy.get("description", None),
                    policy.get("is_administrative", None),
                    policy_id,
                ),
            )
        except Error:
            self.connection.rollback()
        else:
            self.connection.commit()
            return bool(self.cursor.rowcount)

    def policy_exists(self, name: str) -> bool:
        self.cursor.execute(self.get_query("policy", "policy_exists"), (name,))
        return self.cursor.fetchall()[0][0]


policies = PolicyModel()
