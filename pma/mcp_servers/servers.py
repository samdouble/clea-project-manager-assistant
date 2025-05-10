from fastmcp import FastMCP
from typing import Any

from pma.mcp_servers.linear.issues import fct_search_issues

linear_mcp = FastMCP(name="LinearMCPServer")

@linear_mcp.tool()
def search_issues(linear_api_key: str) -> list[Any]:
    """Search for my own issues in Linear"""
    return fct_search_issues(linear_api_key)
