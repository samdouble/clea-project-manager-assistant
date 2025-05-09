import sys
import json
import requests
import os

LINEAR_API_KEY = os.getenv("LINEAR_API_KEY")

def search_issues(query):
    url = "https://api.linear.app/graphql"
    headers = {
        "Authorization": LINEAR_API_KEY,
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

def main():
    for line in sys.stdin:
        try:
            req = json.loads(line)
            if req.get("tool") == "linear_search_issues":
                query = req.get("params", {}).get("query", "")
                result = search_issues(query)
                response = {
                    "id": req.get("id"),
                    "result": result
                }
                print(json.dumps(response), flush=True)
            else:
                print(json.dumps({"error": "Unknown tool"}), flush=True)
        except Exception as e:
            print(json.dumps({"error": str(e)}), flush=True)

if __name__ == "__main__":
    main()
