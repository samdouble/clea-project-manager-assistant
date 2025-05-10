import anthropic
import json
import keyring
import os
import sys
import typer
from rich import print

from pma.mcp_servers.linear.issues import search_issues

def main():
    # Anthropic API key
    anthropic_api_key = os.getenv(
        "ANTHROPIC_API_KEY",
        keyring.get_password('samdouble_project_manager_assistant', 'anthropic_api_key'),
    )
    if anthropic_api_key:
        print("[green]\u2713 Anthropic API key found in environment variables[/green]")
    else:
        anthropic_api_key = typer.prompt("Enter the Anthropic API key")
        keyring.set_password('samdouble_project_manager_assistant', 'anthropic_api_key', anthropic_api_key)
        print("Anthropic API key saved")

    # Linear API key
    linear_api_key = os.getenv(
        "LINEAR_API_KEY",
        keyring.get_password('samdouble_project_manager_assistant', 'linear_api_key'),
    )
    if linear_api_key:
        print("[green]\u2713 Linear API key found in environment variables[/green]")
    else:
        linear_api_key = typer.prompt("Enter the Linear API key")
        keyring.set_password('samdouble_project_manager_assistant', 'linear_api_key', linear_api_key)
        print("Linear API key saved")

    client = anthropic.Anthropic(
        api_key=anthropic_api_key,
    )
    while True:
        user_input = typer.prompt("Enter a message")
        message = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": user_input}
            ]
        )
        print(message.content[0].text)

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
