import locale
import os.path
from datetime import date

# Настройка гита
from openpyxl.styles import Alignment, NamedStyle

USER = 'alexandr.stepanov'
USER_DISPLAY = 'Степанов Александр'
EXCLUDE_BRANCHES = ['dev', 'master']
BRANCH_NAME_REPLACE_LIST = ['bugfix/', 'hotfix/', 'feature/']
EXCLUDE_MERGE = True  # Убрать коммиты мерджа
ATLASSIAN_URL = 'https://fogstream.atlassian.net/browse/{}'

# Настройка дат
locale.setlocale(locale.LC_TIME, 'ru_RU')
DATE_MONTH_DISPLAY_FORMAT = '%B'
REPORT_DAY = 28
END_DATE = date.today()
if END_DATE.month == 1:
    START_DATE = date(END_DATE.year - 1, 12, REPORT_DAY)  # Костыль
else:
    START_DATE = date(END_DATE.year, END_DATE.month - 1, REPORT_DAY)

# Ексель
DATE_FORMAT = '%d.%m.%Y'
DEFAULT_FILE_NAME = f'Отчет {USER_DISPLAY} {END_DATE.strftime(DATE_MONTH_DISPLAY_FORMAT)}.xlsx'

DEFAULT_FILE_PATH = os.path.abspath('out')
DEFAULT_SAVE_FILE_PATH = DEFAULT_FILE_PATH + '/' + DEFAULT_FILE_NAME
EXCEL_DATE_CELL_STYLE = NamedStyle(name='date', number_format='DD.MM.YYYY')
HYPERLINK_CELL_STYLE = NamedStyle(name='Hyperlink', alignment=Alignment(wrapText=True))
TOO_LONG_EXCEL_WIDTH = 200
COLUMN_WIDTH_MULTIPLIER = 1.5
COMMITS_TOGETHER = True
