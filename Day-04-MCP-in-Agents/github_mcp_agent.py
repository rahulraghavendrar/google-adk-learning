import asyncio
import os

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.genai import types


load_dotenv()


github_token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")

if not github_token:
    raise ValueError(
        "GITHUB_PERSONAL_ACCESS_TOKEN is missing. "
        "Add it to the root .env file."
    )


github_toolset = MCPToolset(
    connection_params=StdioConnectionParams(
        command="docker",
        args=[
            "run",
            "-i",
            "--rm",
            "-e",
            "GITHUB_PERSONAL_ACCESS_TOKEN",
            "ghcr.io/github/github-mcp-server",
        ],
        env={
            "GITHUB_PERSONAL_ACCESS_TOKEN": github_token,
        },
    )
)


github_agent = LlmAgent(
    name="github_readonly_agent",
    model="gemini-2.5-flash",
    instruction="""
You are a read-only GitHub repository assistant.

Use the available GitHub MCP tools to inspect repositories, files,
issues, pull requests, and commits.

You may only perform read-only actions.

Never create, edit, delete, merge, close, comment on, or modify anything
on GitHub. If the user asks for a write action, explain that this agent
is configured for read-only access.

Do not claim you inspected GitHub unless you used a GitHub MCP tool.
Give concise answers and mention the repository you inspected.
""",
    tools=[github_toolset],
)


async def main():
    session_service = InMemorySessionService()

    session = await session_service.create_session(
        app_name="github_mcp_agent_app",
        user_id="rahul",
        session_id="github_mcp_session_1",
    )

    runner = Runner(
        agent=github_agent,
        app_name="github_mcp_agent_app",
        session_service=session_service,
    )

    print("🐙 GitHub MCP Read-Only Agent")
    print("Type 'exit' to stop.\n")

    print("Examples:")
    print("• List my repositories.")
    print("• Show the files in rahulraghavendrar/google-adk-learning.")
    print("• Read the README from rahulraghavendrar/google-adk-learning.")
    print("• Show open issues in rahulraghavendrar/google-adk-learning.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("👋 Goodbye!")
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
                            print(f"\n🤖 Assistant: {part.text}\n")

        except Exception as error:
            print(f"\n❌ Error: {error}\n")


if __name__ == "__main__":
    asyncio.run(main())