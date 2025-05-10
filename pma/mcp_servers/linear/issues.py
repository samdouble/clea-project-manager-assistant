import requests

def fct_search_issues(linear_api_key: str):
    url = "https://api.linear.app/graphql"
    headers = {
        "Authorization": linear_api_key,
        "Content-Type": "application/json"
    }
    graphql_query = {
        "query": """
            query SearchIssues($filter: IssueFilter, $term: String!) {
                searchIssues(filter: $filter, term: $term) {
                    nodes {
                        title
                        url
                        assignee {
                            email
                        }
                    }
                }
            }
        """,
        "variables": {
            "filter": {
                "assignee": {
                    "isMe": {
                        "eq": True
                    }
                }
            },
            "term": "a"
        }
    }
    resp = requests.post(url, headers=headers, json=graphql_query)
    return resp.json()
