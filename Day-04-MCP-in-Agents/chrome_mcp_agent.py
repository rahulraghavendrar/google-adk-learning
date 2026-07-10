import asyncio

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.genai import types


load_dotenv()


chrome_toolset = MCPToolset(
    connection_params=StdioConnectionParams(
        command="npx",
        args=[
            "-y",
            "chrome-devtools-mcp@latest",
        ],
    )
)


chrome_search_agent = LlmAgent(
    name="chrome_search_agent",
    model="gemini-2.5-flash",
    instruction="""
You are a browser research assistant.

Use the available Chrome MCP tools to open web pages and inspect their content.

When the user asks to search for something:
1. Open a Google search URL using the user's query.
2. Inspect the visible search results.
3. Return a short answer with the most relevant findings.

Do not claim you searched or read a page unless you used a Chrome MCP tool.
Do not perform logins, purchases, form submissions, or other irreversible actions.
""",
    tools=[chrome_toolset],
)


async def main():
    session_service = InMemorySessionService()

    session = await session_service.create_session(
        app_name="chrome_mcp_agent_app",
        user_id="rahul",
        session_id="chrome_mcp_session_1",
    )

    runner = Runner(
        agent=chrome_search_agent,
        app_name="chrome_mcp_agent_app",
        session_service=session_service,
    )

    print("🌐 Chrome MCP Search Agent")
    print("Type 'exit' to stop.\n")
    print("Examples:")
    print("• Search for the official Google ADK documentation")
    print("• Search for latest MCP tutorials")
    print("• Open https://google.github.io/adk-docs/ and summarize it\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        if not user_input:
            continue

        user_message = types.Content(
            role="user",
            parts=[types.Part(text=user_input)],
        )

        try:
            async for event in runner.run_async(
                user_id=session.user_id,
                session_id=session.id,
                new_message=user_message,
            ):
                if event.is_final_response() and event.content:
                    for part in event.content.parts:
                        if part.text:
                            print(f"\nAssistant: {part.text}\n")

        except Exception as error:
            print(f"\nError: {error}\n")


if __name__ == "__main__":
    asyncio.run(main())