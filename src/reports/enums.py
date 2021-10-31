from enum import Enum


class ExcelHeaders(Enum):
    """Перечисление хеадера таблицы."""
    PROJECT = 'A'
    USER = 'B'
    TASK_LINK = 'C'
    TASK = 'D'
    HOURS = 'E'
    DATE_START = 'F'
    DATE_END = 'G'


EXCLUDE_COLUMNS_MULTIPLIER = [ExcelHeaders.TASK.value, ExcelHeaders.TASK_LINK.value]
