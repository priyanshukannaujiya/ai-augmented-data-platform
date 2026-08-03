import asyncio
import sys
# Force UTF-8 encoding for Windows terminals
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

import boto3
import json
import botocore.exceptions
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from ai_agent.config import AWS_REGION, BEDROCK_MODEL_ID

def mcp_to_bedrock_tool(mcp_tool):
    """Convert an MCP Tool schema to a Bedrock Converse API tool schema."""
    return {
        "toolSpec": {
            "name": mcp_tool.name,
            "description": mcp_tool.description or "",
            "inputSchema": {
                "json": mcp_tool.input_schema
            }
        }
    }

async def run_agent():
    print("Initializing AWS Data Engineering AI Agent...")
    
    # 1. Initialize Bedrock Client
    try:
        bedrock = boto3.client("bedrock-runtime", region_name=AWS_REGION)
    except Exception as e:
        print(f"Error initializing Bedrock client: {e}")
        return

    # 2. Configure MCP Server parameters (local stdio)
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "ai_agent.mcp_server.server"]
    )
    
    print("Connecting to local MCP server...")
    try:
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                # 3. Discover MCP Tools
                tools_response = await session.list_tools()
                mcp_tools = tools_response.tools
                
                # 4. Convert MCP Tools to Bedrock Tool format
                bedrock_tools = [mcp_to_bedrock_tool(t) for t in mcp_tools]
                tool_config = {"tools": bedrock_tools}
                
                print("\n==================================================")
                print("AWS Data Engineering AI Agent")
                print("Type 'exit' or 'quit' to quit.")
                print("==================================================\n")
                
                messages = []
                
                while True:
                    try:
                        user_input = input("You: ")
                    except EOFError:
                        break
                        
                    if user_input.lower() in ['exit', 'quit']:
                        break
                        
                    if not user_input.strip():
                        continue
                        
                    messages.append({"role": "user", "content": [{"text": user_input}]})
                    
                    # 5. Converse Loop (handle tool calls until final response)
                    while True:
                        try:
                            response = bedrock.converse(
                                modelId=BEDROCK_MODEL_ID,
                                messages=messages,
                                toolConfig=tool_config
                            )
                        except botocore.exceptions.ClientError as e:
                            print(f"\n[AWS Error] {e.response['Error']['Message']}")
                            break
                        except Exception as e:
                            print(f"\n[Unexpected Error] {e}")
                            break
                            
                        out_msg = response['output']['message']
                        messages.append(out_msg)
                        
                        # 6. Check if Claude wants to use a tool
                        if response['stopReason'] == 'tool_use':
                            tool_results_content = []
                            for block in out_msg['content']:
                                if 'toolUse' in block:
                                    tool_use = block['toolUse']
                                    tool_name = tool_use['name']
                                    tool_input = tool_use['input']
                                    tool_id = tool_use['toolUseId']
                                    
                                    print(f"\n[DEBUG] Claude selected tool: {tool_name}")
                                    print(f"[DEBUG] MCP tool execution started with args: {tool_input}")
                                    
                                    try:
                                        # 7. Execute through MCP
                                        mcp_result = await session.call_tool(tool_name, arguments=tool_input)
                                        result_text = "\n".join([c.text for c in mcp_result.content])
                                        print(f"[DEBUG] MCP result received: {result_text}")
                                        
                                        # 8. Return result back to Claude
                                        tool_results_content.append({
                                            "toolResult": {
                                                "toolUseId": tool_id,
                                                "content": [{"text": result_text}],
                                                "status": "success"
                                            }
                                        })
                                    except Exception as e:
                                        print(f"[DEBUG] MCP tool execution failed: {e}")
                                        tool_results_content.append({
                                            "toolResult": {
                                                "toolUseId": tool_id,
                                                "content": [{"text": f"Error executing tool: {e}"}],
                                                "status": "error"
                                            }
                                        })
                            
                            # Append all tool results and loop to get Claude's final answer
                            messages.append({"role": "user", "content": tool_results_content})
                        else:
                            # Final text response
                            for block in out_msg['content']:
                                if 'text' in block:
                                    print(f"\nAgent: {block['text']}\n")
                            break
                            
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error during MCP communication: {e}")

if __name__ == "__main__":
    asyncio.run(run_agent())
