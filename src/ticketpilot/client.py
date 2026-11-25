import asyncio
from mcp import Client


async def main():
    async with Client("http://127.0.0.1:8000/mcp") as client:

        # Discover available tools
        tools = await client.list_tools()

        for tool in tools.tools:
            print(tool.name, tool.input_schema)

        # Invoke a tool
        result = await client.call_tool("get_ticket", {"ticket_id": "INC-101"})

        print("Error:", result.is_error)
        print("Data:", result.structured_content)

        # Read a resource
        policy = await client.read_resource("helpdesk://policy")
        print(policy.contents[0].text)

        # Render a prompt
        prompt = await client.get_prompt("triage_ticket", {"ticket_id": "INC-101"})
        print(prompt.messages)


asyncio.run(main())
