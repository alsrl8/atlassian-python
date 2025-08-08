from env import get_domain
from jira.request import jira_request
from util.print_ import pretty_json


def print_jira_issues(issues, total: int):
    print(f"📋 총 {total}개 이슈 중 {len(issues)}개 조회")
    print("-" * 60)

    domain = get_domain()

    for i, issue in enumerate(issues, 1):
        key = issue['key']
        summary = issue['fields']['summary']
        status = issue['fields']['status']['name']
        assignee = issue['fields']['assignee']
        assignee_name = assignee['displayName'] if assignee else '미할당'

        print(f"{i:2d}. [{key}] {summary}")
        print(f"    상태: {status} | 담당자: {assignee_name}")
        print(f"    링크: https://{domain}/browse/{key}")
        print()


def get_jira_issues(jql="", max_results=100):
    """
    Jira 이슈 목록 조회
    """

    if not jql:
        jql = "ORDER BY created DESC"

    params = {
        'jql': jql,
        'maxResults': max_results,
        'fields': 'summary,status,assignee,created,priority'
    }

    data = jira_request('/rest/api/3/search', method='GET', params=params)

    pretty_json(data)

    if not data:
        return None

    print_jira_issues(data["issues"], data["total"])
    return data["issues"]


def get_my_jira_issue_not_done(max_result: int = 5):
    return get_jira_issues(
        jql='assignee = currentUser() AND status != "Done"',
        max_results=max_result,
    )


def get_my_jira_issue_in_progress(max_result: int = 5):
    return get_jira_issues(
        jql='assignee = currentUser() AND status = "In Progress"',
        max_results=max_result,
    )


def get_my_jira_issue_done(max_result: int = 5):
    return get_jira_issues(
        jql='assignee = currentUser() AND status = "Done"',
        max_results=max_result,
    )


def get_jira_issue_detail(issue_key: str):
    result = jira_request(f'/rest/api/3/issue/{issue_key}')

    if result:
        print(f"📄 이슈 {issue_key} 상세 정보:")
        print(f"   제목: {result['fields']['summary']}")
        print(f"   상태: {result['fields']['status']['name']}")

        pretty_json(result)

        return result
    else:
        print(f"❌ 이슈 {issue_key} 조회 실패")
        return None


def transition_issue(issue_key: str, transition_id: str):
    """
    이슈 상태 전환 (POST)
    """
    transition_data = {
        "transition": {"id": transition_id}
    }

    result = jira_request(f'/rest/api/3/issue/{issue_key}/transitions', method='POST', data=transition_data)

    if result:
        print(f"✅ 이슈 {issue_key} 상태 전환 완료")
        return result
    else:
        print(f"❌ 이슈 {issue_key} 상태 전환 실패")
        return None


def get_available_transitions(issue_key: str):
    """
    이슈의 가능한 상태 전환 목록 조회 (GET)
    """
    result = jira_request(f'/rest/api/3/issue/{issue_key}/transitions')

    if result:
        pretty_json(result)
        print(f"📋 이슈 {issue_key}의 가능한 상태 전환:")
        for transition in result['transitions']:
            _id = transition["id"]
            name = transition["to"]["name"]
            o_name = transition["name"]
            print(f"   ID: {_id} - {name}")
        return result['transitions']
    else:
        print(f"❌ 이슈 {issue_key} 상태 전환 목록 조회 실패")
        return None
