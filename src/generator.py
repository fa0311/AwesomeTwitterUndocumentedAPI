import json
import os
from markdownmaker.document import Document


from github import Github

import pandas as pd


from module import *

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
    "Name": get_name_md,
    "Description": get_description_md,
    "Topic": get_topics_md,
    "Language": get_langs_md,
}


doc = Document()

data = [
    [writer(repo_item) for writer in row_data.values()]
    for repo_item in output_repos.values()
]


df = pd.DataFrame(data, columns=row_data.keys())

pd.set_option("display.unicode.east_asian_width", True)


with open("README.md", "w", encoding="utf-8") as f:
    f.write(df.to_markdown(index=False))
