from jira.issue import get_jira_issues
from jira.request import update_jira_issue, get_jira_issue_detail


def main():
    # print("🚀 Jira 이슈 목록 조회")
    # print("=" * 60)
    #
    # # 1. 최근 이슈 10개
    # print("\n1️⃣ 최근 생성된 이슈 10개:")
    # get_jira_issues()
    #
    # # 2. 진행 중인 이슈들
    # print("\n2️⃣ 진행 중인 이슈들:")
    # get_jira_issues(
    #     jql='status = "In Progress"',
    #     max_results=5
    # )
    #
    # # 3. 내가 담당한 미완료 이슈들
    # print("\n3️⃣ 내가 담당한 미완료 이슈들:")
    # get_jira_issues(
    #     jql='assignee = currentUser() AND status != "Done"',
    #     max_results=5
    # )

    get_jira_issue_detail(
        "CWPP-206"
    )

    update_jira_issue(
        "CWPP-206",
        {
            "something": "something!"
        }
    )


if __name__ == "__main__":
    main()
