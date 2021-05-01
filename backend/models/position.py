import logging
from typing import Dict, List, Optional, Union

from enums import TransactionResult
from psycopg2 import Error

from .postgresql_handler import PostgreSQLHandler, convert_row_to_dictionary

LOG = logging.getLogger(__name__)


class PositionModel(PostgreSQLHandler):
    def select_positions(self) -> List[Dict]:
        self.cursor.execute(self.get_query("position", "select_positions"))
        positions = self.cursor.fetchall()

        return convert_row_to_dictionary(positions)

    def select_position_by_id(self, position_id: int) -> Optional[Dict]:
        self.cursor.execute(
            self.get_query("position", "select_position_by_id"), (position_id,)
        )
        position = self.cursor.fetchone()

        if position is not None:
            return dict(position)

        return None

    def delete_position(self, identifier: int) -> bool:
        self.cursor.execute(
            self.get_query("position", "delete_position"), (identifier,)
        )
        self.connection.commit()

        return bool(self.cursor.rowcount)

    def insert_position(self, position: Dict) -> Union[int, TransactionResult]:
        if not self.position_exists(position["title"]):
            try:
                self.cursor.execute(
                    self.get_query("position", "insert_position"),
                    (
                        position["title"],
                        position["level"],
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

    def update_position(self, position_id: int, position: Dict) -> Optional[bool]:
        try:
            self.cursor.execute(
                self.get_query("position", "update_position"),
                (
                    position.get("name", None),
                    position.get("description", None),
                    position_id,
                ),
            )
        except Error as error:
            LOG.debug(error)
            self.connection.rollback()
        else:
            self.connection.commit()
            return bool(self.cursor.rowcount)

    def position_exists(self, name: str) -> bool:
        self.cursor.execute(self.get_query("position", "position_exists"), (name,))
        return self.cursor.fetchall()[0][0]


positions = PositionModel()
