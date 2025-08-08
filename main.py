from jira.issue import *


def main():
    get_jira_issues(
        "assignee = currentUser() ORDER BY summary ASC",
    )


if __name__ == "__main__":
    main()
