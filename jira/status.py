from jira.request import jira_request


def get_bulk_statuses():
    ret = jira_request("/rest/api/3/statuses", "GET", params={
        "id": "45622",
    })
    print(ret)
