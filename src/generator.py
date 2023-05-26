import json
import os
from markdownmaker.document import Document
from markdownmaker.markdownmaker import *


from github import Github

import pandas as pd


from module import get_languages, get_commit_activity, get_stars

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", None)
UPDATE_SKIP = os.environ.get("UPDATE_SKIP", True)
g = Github(GITHUB_TOKEN)


output_repos: dict[str : dict[str : str | list[str]]] = {}

if not UPDATE_SKIP:
    with open("data.json", encoding="utf-8") as f:
        data = json.load(f)

    for repo_name, repo_item in data["repos"].items():
        repo = g.get_repo(repo_name)

        output_repos[repo_name] = {
            "name": repo.name,
            "url": repo.html_url,
            "description": repo.description,
            "topics": repo.topics,
            "langs": get_languages(repo),
            "last_commit": get_commit_activity(repo_name),
            "stars": get_stars(repo_name),
        } | repo_item

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(output_repos, f, indent=4, ensure_ascii=False)

else:
    with open("output.json", encoding="utf-8") as f:
        output_repos = json.load(f)

row_data = {
    "name": lambda x: x,
    "url": lambda x: Link(x, x).write(),
    "description": lambda x: x,
    "topics": lambda x: ", ".join(x),
    "langs": lambda x: ", ".join(x),
    "last_commit": lambda x: Image(x, "last commit").write(Document()),
    "stars": lambda x: Image(x, "stars").write(Document()),
}


doc = Document()

data = [
    [row_writer(repo_item[row]) for row, row_writer in row_data.items()]
    for repo_item in output_repos.values()
]


df = pd.DataFrame(data, columns=row_data.keys())

pd.set_option("display.unicode.east_asian_width", True)


with open("output.md", "w", encoding="utf-8") as f:
    f.write(df.to_markdown(index=False))
