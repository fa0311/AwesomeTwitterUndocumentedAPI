import json
import os
from markdownmaker.document import Document

from github import Github
import pandas as pd
from module import *

pd.set_option("display.unicode.east_asian_width", True)

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", None)
UPDATE_SKIP = os.environ.get("UPDATE_SKIP", True)
g = Github(GITHUB_TOKEN)


output_repos: dict[str:dict] = {}

if not UPDATE_SKIP:
    with open("data.json", encoding="utf-8") as f:
        data: dict[str:dict] = json.load(f)

    for repo_type in data:
        output_repos[repo_type] = {}
        for repo_name, repo_item in data[repo_type].items():
            repo = g.get_repo(repo_name)

            output_repos[repo_type][repo_name] = {
                "name": repo_name,
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

doc = Document()

row_data = {
    "Name": get_name_md,
    "Description": get_description_md,
}

doc.add(Header("AwesomeTwitterUndocumentedAPI"))
doc.add("A curated list of awesome Twitter Undocumented API")
with HeaderSubLevel(doc):
    for repo_type in output_repos:
        doc.add(Header(repo_type))
        table = [
            [writer(repo_item) for writer in row_data.values()]
            for repo_item in output_repos[repo_type].values()
        ]

        df = pd.DataFrame(table, columns=row_data.keys())
        doc.add(df.to_markdown(index=False))


with open("README.md", "w", encoding="utf-8") as f:
    f.write(doc.write())
