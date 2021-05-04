from enum import Enum, auto


class TransactionResult(Enum):
    SUCCESS = "Success"
    ERROR = "Error"


class Permission(Enum):
    CREATE_USERS = "Create users"
    MANAGE_DEPARTMENTS = "Manage departments"
    MANAGE_UNITS = "Manage units"
    MANAGE_GROUPS = "Manage groups"
    MANAGE_ROLES = "Manage roles"
    MANAGE_POSITIONS = "Manage positions"
    MANAGE_USERS = "Manage users"
    MANAGE_POLICIES = "Manage policies"


class APIVersions(Enum):
    v1 = "v1"
    v2 = "v2"
