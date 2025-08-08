from jira.issue import get_jira_issues


def custom_query():
    # 2025-08-08
    # 모든 issue 목록 및 link
    issues = get_jira_issues(
        "assignee = currentUser() AND created >= '2025-08-06' ORDER BY summary ASC",
        exec_print=False,
    )

    pass
