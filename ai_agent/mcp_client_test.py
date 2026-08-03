import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_mcp_client():
    print("="*60)
    print("MCP CLIENT TEST STARTING")
    print("="*60)
    
    # Configure the MCP server to run as a subprocess
    # We invoke the module we just created.
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "ai_agent.mcp_server.server"]
    )
    
    print("1. Starting/connecting to the MCP Server...")
    # Initialize the stdio client
    async with stdio_client(server_params) as (read_stream, write_stream):
        print("2. Initializing MCP session...")
        # Create a session with the server
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the session
            await session.initialize()
            
            print("3. Discovering registered tools...")
            # List available tools
            tools_response = await session.list_tools()
            
            print("\nDiscovered Tools:")
            for tool in tools_response.tools:
                print(f"  - {tool.name}: {tool.description}")
            
            print("\n4. Invoking MCP tools...")
            
            # Invoke bronze_to_silver_status
            print("\n--> Invoking tool: bronze_to_silver_status")
            bronze_result = await session.call_tool("bronze_to_silver_status")
            print("Response:")
            for content in bronze_result.content:
                print(content.text)
                
            # Invoke silver_to_gold_status
            print("\n--> Invoking tool: silver_to_gold_status")
            silver_result = await session.call_tool("silver_to_gold_status")
            print("Response:")
            for content in silver_result.content:
                print(content.text)
                
    print("\n" + "="*60)
    print("MCP CLIENT TEST COMPLETED")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(test_mcp_client())
