import json
import requests
from typing import Any

from pma.integrations.linear import LinearClient
from pma.mcp_servers.linear.issues import ISSUE_NODE_FIELDS
from pma.utils.constants import LINEAR_BASE_URL


def fct_search_projects(
    # Fields
    name: str | None = None,
    # Users
    i_am_part_of: bool = False,
    i_created: bool = False,
    user_part_of: str | None = None,
) -> list[Any]:
    linear_api_key = LinearClient().api_key
    headers = {
        "Authorization": linear_api_key,
        "Content-Type": "application/json"
    }
    graphql_query = {
        "query": f"""
            query SearchProjects($projectFilter: ProjectFilter) {{
                projects(filter: $projectFilter) {{
                    nodes {{
                        creator {{
                            name
                        }}
                        currentProgress
                        description
                        health
                        lead {{
                            name
                        }}
                        name
                        targetDate
                        url
                    }}
                }}
            }}
        """,
        "variables": {
            "projectFilter": {
                "creator": {
                    **({"isMe": {"eq": True}} if i_created else {}),
                },
                "members": {
                    "some": {
                        **({"isMe": {"eq": True}} if i_am_part_of else {}),
                        **({"name": {"contains": user_part_of}} if user_part_of else {}),
                    },
                },
                **({"name": {"contains": name}} if name else {}),
            },
        },
    }
    resp = requests.post(LINEAR_BASE_URL, headers=headers, json=graphql_query)
    return resp.json()["data"]["projects"]["nodes"]
