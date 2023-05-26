from github.Repository import Repository
from markdownmaker.markdownmaker import *


def get_languages(repo: Repository) -> list[str]:
    get_langs = repo.get_languages()
    limit = sum(x for x in get_langs.values()) / 3
    return list(map(lambda x: x[0], filter(lambda x: x[1] > limit, get_langs.items())))


def get_commit_activity(repo_name: str) -> str:
    return f"https://img.shields.io/github/commit-activity/m/{repo_name}"


def get_stars(repo_name: str) -> str:
    return f"https://img.shields.io/github/stars/{repo_name}"


def get_name_md(x):
    return Link(x["name"], x["url"]).write()


def get_description_md(x):
    return "".join(
        [
            x["description"] or "",
            Image(x["last_commit"], "last commit").write(0).replace("\n", " "),
            Image(x["stars"], "stars").write(0).replace("\n", " "),
        ]
    )


def get_topics_md(x):
    return ", ".join(x["topics"])


def get_langs_md(x):
    return ", ".join(x["langs"])
