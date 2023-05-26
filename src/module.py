# todo: from googletrans import Translator

from github.Repository import Repository


def get_languages(repo: Repository) -> list[str]:
    get_langs = repo.get_languages()
    limit = sum(x for x in get_langs.values()) / 3
    return list(map(lambda x: x[0], filter(lambda x: x[1] > limit, get_langs.items())))


def get_commit_activity(repo_name: str) -> str:
    return f"https://img.shields.io/github/commit-activity/{repo_name}"


def get_stars(repo_name: str) -> str:
    return f"https://img.shields.io/github/stars/{repo_name}"
