from jira.issue import *


def main():
    issues = get_jira_issues(
        "assignee = currentUser() AND created >= '2025-08-06' ORDER BY summary ASC",
        exec_print=False,
    )
    pretty_json(issues[0])

    # for i in issues:
    #     print(i["key"], i["fields"]["summary"], i["fields"]["link"])


if __name__ == "__main__":
    main()
