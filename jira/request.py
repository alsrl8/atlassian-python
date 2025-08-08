import json
from typing import Optional, Dict, Any, Union, Literal

import requests
from requests.auth import HTTPBasicAuth
from requests.models import Response

from env import get_domain, get_email, get_api_token


def jira_request(
        endpoint: str,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"] = "GET",
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], str]] = None,
        headers: Optional[Dict[str, str]] = None
) -> Optional[Dict[str, Any]]:
    """
    Jira API 공통 요청 함수

    Args:
        endpoint: API 엔드포인트 경로 (예: '/rest/api/3/search', '/rest/api/3/issue')
        method: HTTP 메서드 ('GET', 'POST', 'PUT', 'DELETE', 'PATCH')
        params: URL 파라미터 (GET 요청용)
        data: 요청 바디 데이터 (POST/PUT 요청용)
        headers: 추가 헤더

    Returns:
        응답 JSON 데이터 또는 None (실패시)
    """

    domain = get_domain()
    email = get_email()
    api_token = get_api_token()

    if not endpoint.startswith('http'):
        url = f"https://{domain}{endpoint}"
    else:
        url = endpoint

    default_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    if headers:
        default_headers.update(headers)

    auth = HTTPBasicAuth(email, api_token)

    if data and isinstance(data, dict):
        data = json.dumps(data)

    response: Response | None = None
    try:
        response = requests.request(
            method=method.upper(),
            url=url,
            params=params,
            data=data,
            headers=default_headers,
            auth=auth
        )

        response.raise_for_status()

        if response.content:
            return response.json()
        else:
            return {"success": True, "status_code": response.status_code}

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP 오류 ({response.status_code}): {e}")
        if response.content:
            try:
                error_data = response.json()
                print(f"   상세: {error_data}")
            except:
                print(f"   응답: {response.text}")
        return None

    except requests.exceptions.RequestException as e:
        print(f"❌ 요청 실패: {e}")
        return None


# 다른 Jira API 사용 예시들
def create_jira_issue(project_key: str, summary: str, description: str = "", issue_type: str = "Task"):
    """
    Jira 이슈 생성 (POST)
    """
    issue_data = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": description}]
                    }
                ]
            },
            "issuetype": {"name": issue_type}
        }
    }

    result = jira_request('/rest/api/3/issue', method='POST', data=issue_data)

    if result:
        print(f"✅ 이슈 생성 성공: {result['key']}")
        return result
    else:
        print("❌ 이슈 생성 실패")
        return None


def update_jira_issue(issue_key: str, fields: Dict[str, Any]):
    """
    Jira 이슈 수정 (PUT)
    """
    update_data = {"fields": fields}

    result = jira_request(f'/rest/api/3/issue/{issue_key}', method='PUT', data=update_data)

    if result:
        print(f"✅ 이슈 {issue_key} 수정 완료")
        return result
    else:
        print(f"❌ 이슈 {issue_key} 수정 실패")
        return None


def delete_jira_issue(issue_key: str):
    """
    Jira 이슈 삭제 (DELETE)
    """
    result = jira_request(f'/rest/api/3/issue/{issue_key}', method='DELETE')

    if result:
        print(f"✅ 이슈 {issue_key} 삭제 완료")
        return True
    else:
        print(f"❌ 이슈 {issue_key} 삭제 실패")
        return False


def get_jira_issue_detail(issue_key: str):
    """
    특정 이슈 상세 조회 (GET)
    """
    result = jira_request(f'/rest/api/3/issue/{issue_key}')

    if result:
        print(f"📄 이슈 {issue_key} 상세 정보:")
        print(f"   제목: {result['fields']['summary']}")
        print(f"   상태: {result['fields']['status']['name']}")
        print(f"   fields: {result['fields']}")
        return result
    else:
        print(f"❌ 이슈 {issue_key} 조회 실패")
        return None


def add_comment_to_issue(issue_key: str, comment_text: str):
    """
    이슈에 코멘트 추가 (POST)
    """
    comment_data = {
        "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": comment_text}]
                }
            ]
        }
    }

    result = jira_request(f'/rest/api/3/issue/{issue_key}/comment', method='POST', data=comment_data)

    if result:
        print(f"✅ 이슈 {issue_key}에 코멘트 추가 완료")
        return result
    else:
        print(f"❌ 이슈 {issue_key} 코멘트 추가 실패")
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
        print(f"📋 이슈 {issue_key}의 가능한 상태 전환:")
        for transition in result['transitions']:
            print(f"   ID: {transition['id']} - {transition['name']}")
        return result['transitions']
    else:
        print(f"❌ 이슈 {issue_key} 상태 전환 목록 조회 실패")
        return None
