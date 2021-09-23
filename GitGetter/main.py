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
    with open("Studio_2.txt", "w") as s:
        for name in repo_names:
            s.write("==================" + name + "==================\n")
            repo = g.get_repo(name)

            s.write("OPEN ISSUES\n")
            open_issues = repo.get_issues(state="open")
            for issue in open_issues:
                issues = str(issue.id) + " " + str(issue.state) + " " + str(issue.assignees)
                s.write(issues + "\n")

            s.write("COMMITS\n")
            try:
                commits = repo.get_commits()
                for commit in commits:
                    headerkeys = commit.raw_headers
                    # print(headerkeys)
                    comms = str(headerkeys['last-modified']) + " " + str(commit.html_url) + " " +  str(commit.author)
                    s.write(comms + "\n")
            except github.GithubException:
                print("Error: no commits")

            s.write("PULL REQUESTS\n")
            pulls = repo.get_pulls()
            for p in pulls:
                print(p.state)
                for c in p.get_review_comments():
                    s.write(c + "\n")

            s.write("GROUP MEMBERS\n")
            users = repo.get_contributors()
            for user in users:
                peeps = str(user) + " " +  str(user.last_modified) + " " +  str(user.name)
                s.write(peeps + "\n")

            s.write("==================" + "END" + "==================\n\n")
        s.close()
        sleep(2)





