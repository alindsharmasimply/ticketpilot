import os

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

mcp = MCPServer(
    "TicketPilot",
    version="1.0.0",
    instructions="Use ticket data to answer IT support questions.",
)

TICKETS = {
    "INC-101": {
        "id": "INC-101",
        "title": "VPN connection failing",
        "team": "IT",
        "status": "open",
    },
    "INC-102": {
        "id": "INC-102",
        "title": "Payroll dashboard unavailable",
        "team": "HR",
        "status": "open",
    },
    "INC-103": {
        "id": "INC-103",
        "title": "WSL network access failing when connected to VPN",
        "team": "Networks",
        "status": "closed",
    },
}


def find_allowed_ticket(ticket_id: str):
    ticket = TICKETS.get(ticket_id)

    allowed_team = os.getenv("HELPDESK_TEAM", "IT")

    if not ticket or ticket["team"] != allowed_team:
        raise ToolError("Ticket not found or not accessible")

    return ticket


@mcp.tool()
def get_ticket(ticket_id: str):
    """Get an IT Support Ticket by its exact incident ID."""
    return find_allowed_ticket(ticket_id).copy()


@mcp.tool()
def list_open_tickets():
    """List open tickets belonging to the permitted team."""
    allowed_team = os.getenv("HELPDESK_TEAM", "IT")
    return [
        t.copy()
        for t in TICKETS.values()
        if t["team"] == allowed_team and t["status"] == "open"
    ]


if __name__ == "__main__":
    mcp.run()
