import requests
from typing import Any

from pma.integrations.linear import LinearClient
from pma.utils.constants import LINEAR_BASE_URL


def fct_search_issues(assignee: str = None, is_mine_only: bool = False, is_current_cycle: bool = False) -> list[Any]:
    linear_api_key = LinearClient().api_key
    headers = {
        "Authorization": linear_api_key,
        "Content-Type": "application/json"
    }
    graphql_query = {
        "query": """
            query SearchIssues($filter: IssueFilter) {
                issues(filter: $filter) {
                    nodes {
                        assignee {
                            email
                        }
                        cycle {
                            name
                        }
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
                    }
                }
            }
        """,
        "variables": {
            "filter": {
                "assignee": {
                    **({"isMe": {"eq": True}} if is_mine_only else {}),
                    **({"name": {"contains": assignee}} if assignee else {}),
                }
            },
        }
    }
    #             cycles(filter: $cycleFilter) {
    #                 nodes {
    #                     name
    #                 }
    #             }
    #         "cycleFilter": {
    #             **({"isActive": {"eq": True}} if is_current_cycle else {}),
    #         }
    resp = requests.post(LINEAR_BASE_URL, headers=headers, json=graphql_query)
    return resp.json()["data"]["issues"]["nodes"]
