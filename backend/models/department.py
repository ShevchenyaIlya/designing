from typing import Dict, List, Optional, Tuple, Union

from enums import TransactionResult
from psycopg2 import Error

from .postgresql_handler import PostgreSQLHandler, convert_row_to_dictionary


class DepartmentModel(PostgreSQLHandler):
    def select_departments(self) -> List[Dict]:
        self.cursor.execute(self.get_query("department", "select_departments"))
        departments = self.cursor.fetchall()

        return convert_row_to_dictionary(departments)

    def select_department_by_name(self, name: str) -> Dict:
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

    def insert_department(self, department: Dict) -> Union[int, TransactionResult]:
        if not self.department_exists(department["name"]):
            try:
                self.cursor.execute(
                    self.get_query("department", "insert_department"),
                    (
                        department["name"],
                        department["description"],
                        department["head_id"],
                    ),
                )
            except Error:
                self.connection.rollback()
                return TransactionResult.ERROR
            else:
                self.connection.commit()
                return self.cursor.fetchone()[0]

        return TransactionResult.SUCCESS

    def update_department(self, department_id, department) -> Optional[bool]:
        try:
            self.cursor.execute(
                self.get_query("department", "update_department"),
                (
                    department.get("name", None),
                    department.get("description", None),
                    department.get("head_id", None),
                    department_id,
                ),
            )
        except Error:
            self.connection.rollback()
        else:
            self.connection.commit()
            return bool(self.cursor.rowcount)

    def department_exists(self, name: str) -> bool:
        self.cursor.execute(self.get_query("department", "department_exists"), (name,))
        return self.cursor.fetchall()[0][0]


departments = DepartmentModel()
