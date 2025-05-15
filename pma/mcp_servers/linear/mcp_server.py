from fastmcp import FastMCP
from typing import Any

from pma.mcp_servers.linear.issues import fct_search_issues, fct_update_issue
from pma.mcp_servers.linear.projects import fct_search_projects
from pma.mcp_servers.linear.users import fct_search_users

linear_mcp = FastMCP(name="LinearMCPServer")

@linear_mcp.tool()
def search_issues(
    assignee: str | None = None,
    is_current_cycle: bool = False,
    is_description_empty: bool | None = None,
    is_mine_only: bool = False,
    is_next_cycle: bool = False,
    is_previous_cycle: bool = False,
) -> list[Any]:
    """Search for my own issues in Linear"""
    return fct_search_issues(
        assignee=assignee,
        is_current_cycle=is_current_cycle,
        is_description_empty=is_description_empty,
        is_mine_only=is_mine_only,
        is_next_cycle=is_next_cycle,
        is_previous_cycle=is_previous_cycle,
    )


@linear_mcp.tool()
def update_issue(
    issue_id: str,
    description: str | None = None,
    estimate: int | None = None,
) -> list[Any]:
    """Update an issue in Linear"""
    return fct_update_issue(
        issue_id=issue_id,
        description=description,
        estimate=estimate,
    )


@linear_mcp.tool()
def search_projects(
    i_am_part_of: bool = False,
    i_created: bool = False,
    name: str | None = None,
    user_part_of: str | None = None,
) -> list[Any]:
    """Search for projects in Linear"""
    return fct_search_projects(
        i_am_part_of=i_am_part_of,
        i_created=i_created,
        name=name,
        user_part_of=user_part_of,
    )


@linear_mcp.tool()
def search_users(
    name: str = None,
) -> list[Any]:
    """Search for team members and users in Linear"""
    return fct_search_users(name=name)
