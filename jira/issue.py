from env import get_domain
from jira.request import jira_request


def get_jira_issues(jql="", max_results=10):
    """
    Jira 이슈 목록 조회
    """

    if not jql:
        jql = "ORDER BY created DESC"

    # 요청 파라미터
    params = {
        'jql': jql,
        'maxResults': max_results,
        'fields': 'summary,status,assignee,created,priority'
    }

    # 공통 함수 사용
    data = jira_request('/rest/api/3/search', method='GET', params=params)

    if not data:
        return None

    issues = data['issues']
    domain = get_domain()

    print(f"📋 총 {data['total']}개 이슈 중 {len(issues)}개 조회")
    print("-" * 60)

    for i, issue in enumerate(issues, 1):
        key = issue['key']
        summary = issue['fields']['summary']
        status = issue['fields']['status']['name']
        assignee = issue['fields']['assignee']
        assignee_name = assignee['displayName'] if assignee else '미할당'
        print(f"issue : {issue}")
        print(f"key : {key}")

        print(f"{i:2d}. [{key}] {summary}")
        print(f"    상태: {status} | 담당자: {assignee_name}")
        print(f"    링크: https://{domain}/browse/{key}")
        print()
    return issues
