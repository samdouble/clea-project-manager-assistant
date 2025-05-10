# project-manager-assistant

Optionally, create a `.env` file like this:
```
ANTHROPIC_API_KEY=
LINEAR_API_KEY=
```
If you don't, you are going to be asked the informations through the CLI.

Run:
```
poetry run python main.py
```

Example of what to send it:
```
{"id": 1, "tool": "linear_search_issues", "params": {"query": "test"}}
```
