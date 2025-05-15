import requests
from typing import Any

from pma.integrations.linear import LinearClient
from pma.utils.constants import LINEAR_BASE_URL

ISSUE_NODE_FIELDS = """
    assignee {
        name
    }
    creator {
        name
    }
    cycle {
        name
        number
    }
    description
    dueDate
    estimate
    project {
        name
    }
    state {
        name
    }
    title
    url
"""

def fct_search_issues(
    # Fields
    is_description_empty: bool | None = None,
    # Assignee
    assignee: str | None = None,
    is_mine_only: bool = False,
    # Cycle
    is_current_cycle: bool | None = None,
    is_next_cycle: bool | None = None,
    is_previous_cycle: bool | None = None
) -> list[Any]:
    linear_api_key = LinearClient().api_key
    headers = {
        "Authorization": linear_api_key,
        "Content-Type": "application/json"
    }
    graphql_query = {
        "query": f"""
            query SearchIssues($issueFilter: IssueFilter, $cycleFilter: CycleFilter) {{
                issues(filter: $issueFilter) {{
                    nodes {{
                        {ISSUE_NODE_FIELDS}
                    }}
                }}
                cycles(filter: $cycleFilter) {{
                    nodes {{
                        name
                    }}
                }}
            }}
        """,
        "variables": {
            "issueFilter": {
                "assignee": {
                    **({"isMe": {"eq": True}} if is_mine_only else {}),
                    **({"name": {"contains": assignee}} if assignee else {}),
                },
                "cycle": {
                    **({"isActive": {"eq": is_current_cycle}} if is_current_cycle is not None else {}),
                    **({"isNext": {"eq": is_next_cycle}} if is_next_cycle is not None else {}),
                    **({"isPrevious": {"eq": is_previous_cycle}} if is_previous_cycle is not None else {}),
                },
                "description": {
                    **({"null": is_description_empty} if is_description_empty is not None else {}),
                }
            },
            "cycleFilter": {
                **({"isActive": {"eq": is_current_cycle}} if is_current_cycle is not None else {}),
            }
        }
    }
    resp = requests.post(LINEAR_BASE_URL, headers=headers, json=graphql_query)
    return resp.json()["data"]["issues"]["nodes"]


def fct_update_issue(
    issue_id: str,
    description: str | None = None,
    estimate: int | None = None,
) -> list[Any]:
    linear_api_key = LinearClient().api_key
    headers = {
        "Authorization": linear_api_key,
        "Content-Type": "application/json"
    }
    graphql_query = {
        "query": f"""
            mutation UpdateIssue($id: String!, $updateInput: IssueUpdateInput!) {{
                issueUpdate(id: $id, input: $updateInput) {{
                    issue {{
                        {ISSUE_NODE_FIELDS}
                    }}
                    success
                }}
            }}
        """,
        "variables": {
            "id": issue_id,
            "updateInput": {
                **({"description": description} if description else {}),
                **({"estimate": estimate} if estimate else {}),
            },
        }
    }
    resp = requests.post(LINEAR_BASE_URL, headers=headers, json=graphql_query)
    return resp.json()["data"]["issueUpdate"]["issue"]
