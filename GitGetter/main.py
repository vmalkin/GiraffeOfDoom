# This script is designed to use the Github api to extract information about a series of repos,
# their contributors and their work. Data will be displayed graphically.
import github.GithubException
from github import Github
from pprint import pprint
from time import sleep

git_token = "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"
g = Github(git_token)

repo_names = [
    "BIT-Studio-2/project-21s2-buddy-on-the-beach",
    "BIT-Studio-2/project-21s2-ark-tech",
    "BIT-Studio-2/project-21s2-beach-boys",
    "BIT-Studio-2/project-21s2-beach-buddy",
    "BIT-Studio-2/project-21s2-jackal",
    "BIT-Studio-2/project-21s2-paw-patrol",
    "BIT-Studio-2/project-21s2-sea-dogs",
    "BIT-Studio-2/project-21s2-walkeez"
    ]


if __name__ == '__main__':
    for name in repo_names:
        print("==================" + name + "==================")
        repo = g.get_repo(name)

        print("\nOPEN ISSUES")
        open_issues = repo.get_issues(state="open")
        for issue in open_issues:
            print(issue.id, issue.state, issue.assignees)

        print("\nCOMMITS")
        try:
            commits = repo.get_commits()
            for commit in commits:
                print(commit.last_modified, commit.committer)

        except github.GithubException:
            print("Error: no commits")

        print("\nGROUP MEMBERS")
        users = repo.get_contributors()
        for user in users:
            print(user)

        print("==================" + "END" + "==================")
        print(" ")
        sleep(2)





