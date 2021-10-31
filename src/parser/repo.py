from git import Repo

from src.parser.branch import Branch
from src.parser.commit import GitCommit
from src.settings.git_settings import EXCLUDE_BRANCHES


class Repository:
    """Репозиторий проекта."""
    def __init__(self, name: str, project_conf: dict):
        self.name = name
        self.path = project_conf['path']
        self.repo = Repo(self.path)
        self.branches: list[Branch] = []
        self.commits: list[GitCommit] = []
        self.init_branches()
        self.init_commits()

    def __str__(self):
        """Отображаемое имя."""
        return self.name

    def init_branches(self):
        """Инициализируем и фильтруем ветки."""
        branches = list(map(str, self.repo.branches))
        for branch_name in branches:
            if branch_name in EXCLUDE_BRANCHES:
                continue
            branch = Branch(branch_name)
            self.branches.append(branch)

    def init_commits(self):
        """Собираем уникальные коммиты."""
        hex_list = set()
        for branch in self.branches:
            commits = list(self.repo.iter_commits(branch.name))
            for commit in commits:
                commit = GitCommit(commit, branch.name)
                if commit.is_valid() and commit.hex not in hex_list:
                    self.commits.append(commit)
                    hex_list.add(commit.hex)

        self.commits.sort(key=lambda comm: comm.date)
