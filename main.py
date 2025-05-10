import json
import sys
import typer

from pma.mcp_servers.linear.issues import search_issues

def main():
    linear_api_key = typer.prompt("Enter the Linear API key")
    for line in sys.stdin:
        try:
            req = json.loads(line)
            if req.get("tool") == "linear_search_issues":
                query = req.get("params", {}).get("query", "")
                result = search_issues(linear_api_key, query)
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
    typer.run(main)
