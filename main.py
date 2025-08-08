from jira.issue import *
from jira.status import get_bulk_statuses


def main():
    key = "CWPP-206"
    get_jira_issue_detail(key)
    get_bulk_statuses()

if __name__ == "__main__":
    main()
