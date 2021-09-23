# This script is designed to use the Github api to extract information about a series of repos, their contributors
# and their work
# Data will be displayed graphically.

from github import Github
import requests
from pprint import pprint

git_token = "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"
g = Github(git_token)


repos = [
    "BIT-Studio-2/project-21s2-buddy-on-the-beach",
    "BIT-Studio-2/project-21s2-ark-tech",
    "BIT-Studio-2/project-21s2-beach-boys",
    "BIT-Studio-2/project-21s2-beach-buddy",
    "BIT-Studio-2/project-21s2-jackal",
    "BIT-Studio-2/project-21s2-paw-patrol",
    "BIT-Studio-2/project-21s2-sea-dogs",
    "BIT-Studio-2/project-21s2-walkeez"
    ]

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    for item in repos:
        r = g.get_repo(item)
        pprint(r.get_contributors().get_page(0))



