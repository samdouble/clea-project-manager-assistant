import anthropic
import json
import keyring
import os
import typer
from fastmcp import Client
from rich import print

from pma.mcp_servers.servers import linear_mcp
from pma.utils.constants import AGENT_NAME, ANTHROPIC_MODEL

app = typer.Typer()

@app.command()
async def run():
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

    print(f"You can start conversing with {AGENT_NAME}, your project manager assistant.")

    messages = []
    messages.append({
        "role": "user",
        "content": """
            You are a project manager that converts user requests about their Linear projects and issues into MCP JSON requests.
            For every question, simply respond with the MCP JSON object without explanation.
            If you need additional information to answer the question properly, answer in the JSON format like this:
            {"target": "user", "message": "<Your message here>"}

            Examples:
            User: "Show me all the issues in the current cycle"
            Assistant: {"target": "MCP", "tool": "linear_search_issues", "params": {"query": "123"}}
        """,
    })
    async with Client(linear_mcp) as linear_mcp_client:
        tools = await linear_mcp_client.list_tools()
        print(tools)
        while True:
            user_input = typer.prompt(">")
            messages.append({"role": "user", "content": user_input})

            message = client.messages.create(
                model=ANTHROPIC_MODEL,
                max_tokens=16384,
                messages=messages,
            )
            message_text = message.content[0].text
            messages.append({"role": "assistant", "content": message_text})
            try:
                message_json = json.loads(message_text)
                if message_json.get("target") == "MCP":
                    print(f"[blue]MCP:[/blue] {message_json.get('tool')}")
                elif message_json.get("target") == "user":
                    print(f"[blue]{AGENT_NAME}:[/blue] {message_json.get('message')}")
            except Exception as e:
                print(f"[red]Could not parse answer:[/red] {e}")
                continue
