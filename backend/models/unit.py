import json
from typing import Dict, List, Optional, Tuple

import psycopg2
from psycopg2.extensions import AsIs
from psycopg2.extras import DictCursor

from .postgresql_handler import PostgreSQLHandler, convert_row_to_dictionary


class UnitModel(PostgreSQLHandler):
    def select_units(self) -> List[Dict]:
        self.cursor.execute(self.get_query("unit", "select_units"))
        units = self.cursor.fetchall()

        return convert_row_to_dictionary(units)

    def select_department_units(self, department_id: int) -> List[Dict]:
        self.cursor.execute(
            self.get_query("unit", "select_department_units"), (department_id,)
        )
        units = self.cursor.fetchall()

        return convert_row_to_dictionary(units)

    def select_single_unit(self, name: str) -> Optional[Dict]:
        self.cursor.execute(self.get_query("unit", "select_single_unit"), (name,))
        unit = self.cursor.fetchone()

        if unit is not None:
            return dict(unit)

        return None

    def delete_unit(self, identifier: str) -> bool:
        self.cursor.execute(self.get_query("unit", "delete_unit"), (identifier,))
        self.connection.commit()

        return bool(self.cursor.rowcount)

    def insert_unit(self, unit: Dict) -> int:
        if not self.unit_exists(unit["name"]):
            self.cursor.execute(
                self.get_query("unit", "insert_unit"),
                (
                    unit["name"],
                    unit["description"],
                    unit["department_id"],
                    unit["head_id"],
                ),
            )
            self.connection.commit()

            return self.cursor.fetchone()[0]

    def update_unit(self, unit: Dict) -> bool:
        self.cursor.execute(
            self.get_query("unit", "update_unit"),
            (
                unit.get("name", None),
                unit.get("description", None),
                unit.get("department_id", None),
                unit.get("head_id", None),
                unit["id"],
            ),
        )

        self.connection.commit()

        return bool(self.cursor.rowcount)

    def unit_exists(self, name: str) -> bool:
        self.cursor.execute(self.get_query("unit", "unit_exists"), (name,))
        return self.cursor.fetchall()[0][0]


units = UnitModel()
