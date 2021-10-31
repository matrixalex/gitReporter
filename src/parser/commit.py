import re
from datetime import datetime

from git import Commit

from src.settings.git_settings import (BRANCH_NAME_REPLACE_LIST, END_DATE,
                                       EXCLUDE_MERGE, START_DATE, USER)


class GitCommit:
    def __init__(self, commit: Commit, branch_name: str):
        self.author = commit.author
        self.hex = commit.hexsha
        self.branch = self.convert_branch_name(branch_name)
        self.message = self.convert_message(commit.message)
        self.date = datetime.fromtimestamp(commit.committed_date).date()

    def __str__(self):
        return self.message

    def __repr__(self):
        return f'Commit("{self.__str__()}")'

    def convert_branch_name(self, branch_name):
        for raplace_value in BRANCH_NAME_REPLACE_LIST:
            branch_name = branch_name.replace(raplace_value, '')
        return branch_name

    def convert_message(self, message: str):
        message = message.replace('\n', ' ')
        message = re.sub(' +', ' ', message).strip()
        message = re.sub(f'^\(.+\)', '', message)
        return message.strip()

    def is_valid(self):
        if USER not in str(self.author):
            return False
        if not (START_DATE < self.date < END_DATE):
            return False
        if EXCLUDE_MERGE:
            if 'merge' in self.message and 'into' in self.message:
                return False
        return True
