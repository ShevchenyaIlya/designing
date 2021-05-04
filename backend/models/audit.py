import logging
from datetime import datetime
from typing import Dict, List

from psycopg2 import Error

from .postgresql_handler import PostgreSQLHandler, convert_row_to_dictionary

LOG = logging.getLogger(__name__)


class AuditModel(PostgreSQLHandler):
    def rollback(self, date: datetime) -> bool:
        LOG.debug(f"Execute rollback to {date}")

        try:
            self.cursor.callproc("rollback_changes", (date,))
        except Error as error:
            LOG.debug(f"Rollback failed. Error: {error}")
            return False

        LOG.debug("Successfully rollback")
        return True

    def select_audit_information(self, date: datetime) -> List[Dict]:
        self.cursor.execute(self.get_query("user", "select_audit_entries"), (date,))
        audit_entries = self.cursor.fetchall()

        return convert_row_to_dictionary(audit_entries)


audit = AuditModel()
