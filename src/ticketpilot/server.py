import os

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from pydantic import BaseModel


class Ticket(BaseModel):
    id: str
    title: str
    team: str
    status: str


mcp = MCPServer(
    "TicketPilot",
    version="1.0.0",
    instructions="Use ticket data to answer IT support questions.",
)

TICKETS: dict[str, Ticket] = {
    "INC-101": Ticket(
        id="INC-101",
        title="VPN connection failing",
        team="IT",
        status="open",
    ),
    "INC-102": Ticket(
        id="INC-102",
        title="Payroll dashboard unavailable",
        team="HR",
        status="open",
    ),
    "INC-103": Ticket(
        id="INC-103",
        title="WSL network access failing when connected to VPN",
        team="Networks",
        status="closed",
    ),
}


def find_allowed_ticket(ticket_id: str) -> Ticket:
    ticket = TICKETS.get(ticket_id)

    allowed_team = os.getenv("HELPDESK_TEAM", "IT")

    if not ticket or ticket.team != allowed_team:
        raise ToolError("Ticket not found or not accessible")

    return ticket


@mcp.tool()
def get_ticket(ticket_id: str) -> Ticket:
    """Get an IT Support Ticket by its exact incident ID."""
    return find_allowed_ticket(ticket_id).copy()


@mcp.tool()
def list_open_tickets():
    """List open tickets belonging to the permitted team."""
    allowed_team = os.getenv("HELPDESK_TEAM", "IT")
    return [
        t.copy()
        for t in TICKETS.values()
        if t.team == allowed_team and t.status == "open"
    ]


@mcp.resource("helpdesk://policy")
def helpdesk_policy():
    """IT support operating policy"""
    return (
        "Always verify tickets using actual records. "
        "Never invent incident details. "
        "Never resolve a ticket without explicit approval."
    )


@mcp.prompt()
def triage_ticket(ticket_id: str) -> str:
    """Prepare a structured incident triage request."""
    return (
        f"Investigate ticket {ticket_id}. "
        "Fetch its actual details, summarize the status, "
        "and suggest the next appropriate action. "
        "Do not modify the ticket."
    )


if __name__ == "__main__":
    mcp.run()
