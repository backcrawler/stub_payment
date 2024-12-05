from enum import Enum


class IsolationLevelEnum(str, Enum):
    serializable = "serializable"
    repeatable_read = "repeatable_read"
    read_committed = "read_committed"


class OperationResultEnum(str, Enum):
    success = "success"
    failed = "failed"
