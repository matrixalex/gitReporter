import os

from networkdays.networkdays import Networkdays
from openpyxl import Workbook
from openpyxl.styles import Alignment

from src.parser.repo import Repository
from src.reports.enums import EXCLUDE_COLUMNS_MULTIPLIER, ExcelHeaders
from src.settings.git_settings import (ATLASSIAN_URL, COLUMN_WIDTH_MULTIPLIER,
                                       COMMITS_TOGETHER, DATE_FORMAT,
                                       DEFAULT_SAVE_FILE_PATH,
                                       EXCEL_DATE_CELL_STYLE,
                                       HYPERLINK_CELL_STYLE,
                                       TOO_LONG_EXCEL_WIDTH)


class ExcelReporter:
    """Класс производящий выгрузку данных в ексель."""
    def __init__(self, user, repos: list[Repository]):
        """Инициализация."""
        self.user = user
        self.repos = repos
        self.workbook = self.init_workbook()
        self.sheet = self.init_sheet()
        self.init_headers()
        self.columns_width = {}
        self.summary_hours = 0

    def init_workbook(self):
        """Инициализация таблицы."""
        workbook = Workbook()
        return workbook

    def init_sheet(self):
        """Инициализация листа."""
        sheet = self.workbook.worksheets[0]
        sheet.title = 'Отчет'
        return sheet

    def init_headers(self):
        """Создание хеадеров таблицы."""
        self.sheet[ExcelHeaders.PROJECT.value + '1'] = 'Проект'
        self.sheet[ExcelHeaders.USER.value + '1'] = 'Исполнитель'
        self.sheet[ExcelHeaders.TASK_LINK.value + '1'] = 'Ссылка на задачу'
        self.sheet[ExcelHeaders.TASK.value + '1'] = 'Задача'
        self.sheet[ExcelHeaders.HOURS.value + '1'] = 'Часы потраченные на задачу'
        self.sheet[ExcelHeaders.DATE_START.value + '1'] = 'Дата начала'
        self.sheet[ExcelHeaders.DATE_END.value + '1'] = 'Дата окончания'

    def group_commits_by_date(self, repo: Repository):
        """Группировка коммитов по дате."""
        result = {}
        for commit in repo.commits:
            date = commit.date
            if date not in result:
                result[date] = [commit]
            else:
                result[date].append(commit)

        return result

    def construct(self):
        """Запись данных в таблицу."""
        data = []
        for repo in self.repos:
            commits_by_date = self.group_commits_by_date(repo)
            dates = list(commits_by_date.keys())
            for date in dates:
                commits = commits_by_date[date]
                if COMMITS_TOGETHER:
                    task_links = set([ATLASSIAN_URL.format(commit.branch) for commit in commits])
                    commits_display = ' \n'.join([commit.message for commit in commits])
                    row_data = [
                        repo.name,
                        self.user,
                        ' \n'.join(task_links),
                        commits_display,
                        self.calculate_work_hours(date, date),
                        date.strftime(DATE_FORMAT),
                        date.strftime(DATE_FORMAT)
                    ]
                    data.append(row_data)
                else:
                    for commit in commits:
                        row_data = [
                            repo.name,
                            self.user,
                            ATLASSIAN_URL.format(commit.branch),
                            commit.message,
                            self.calculate_work_hours(commit.date, commit.date),
                            date.strftime(DATE_FORMAT),
                            date.strftime(DATE_FORMAT)
                        ]
                        data.append(row_data)

        self.render_rows(data)
        self.set_columns_width()

    def calculate_work_hours(self, date_start, date_end):
        days = Networkdays(date_start, date_end).networkdays()
        return len(days) * 8

    def render_rows(self, data: list):
        row_num = 2
        columns = [column.value for column in ExcelHeaders]
        for row in data:
            self.render_row(row_num, columns, row)
            row_num += 1
        self.render_footer(row_num)

    def render_row(self, row_num: int, columns: list[str], row: list):
        assert len(columns) == len(row)

        for i, column in enumerate(columns):
            cell = self.sheet[f'{column}{row_num}']
            cell.alignment = Alignment(wrapText=True)
            if column == ExcelHeaders.TASK_LINK.value:
                cell.style = HYPERLINK_CELL_STYLE
            elif column in [ExcelHeaders.DATE_START.value, ExcelHeaders.DATE_END.value]:
                cell.style = EXCEL_DATE_CELL_STYLE
            elif column == ExcelHeaders.HOURS.value:
                self.summary_hours += row[i]

            cell.value = row[i]
            cell_len = len(str(cell.value))
            col_width = self.columns_width.get(column, 0)
            self.columns_width[column] = max(col_width, cell_len)

    def set_columns_width(self):
        for col in self.columns_width:
            val = max(self.columns_width[col], len(str(self.sheet[col + str(1)].value)))
            if col not in EXCLUDE_COLUMNS_MULTIPLIER:
                val = int(val * COLUMN_WIDTH_MULTIPLIER)
            if col == ExcelHeaders.TASK_LINK.value:
                val = 50
            elif val > TOO_LONG_EXCEL_WIDTH:
                val //= 2.5
            self.sheet.column_dimensions[col].width = val

    def render_footer(self, row_num):
        cell = self.sheet[ExcelHeaders.TASK.value + str(row_num)]
        cell.value = 'Итого:'
        cell.alignment = Alignment(horizontal='right')
        cell_val = self.sheet[ExcelHeaders.HOURS.value + str(row_num)]
        cell_val.value = self.summary_hours

    def save(self):
        """Сохранение файла."""
        file_name = DEFAULT_SAVE_FILE_PATH
        if os.path.isfile(file_name):
            num = 1
            while os.path.isfile(file_name):
                name, ext = DEFAULT_SAVE_FILE_PATH.split('.')
                file_name = name + f'_{num}.' + ext
                num += 1

        self.workbook.save(file_name)
        return file_name
