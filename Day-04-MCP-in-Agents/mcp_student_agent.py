import asyncio
import os
import sys

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.genai import types


load_dotenv()


CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
SERVER_FILE = os.path.join(CURRENT_FOLDER, "student_mcp_server.py")


mcp_toolset = MCPToolset(
    connection_params=StdioConnectionParams(
        command=sys.executable,
        args=[SERVER_FILE],
    )
)


student_mcp_agent = LlmAgent(
    name="student_mcp_agent",
    model="gemini-2.5-flash",
    instruction="""
You are a student information assistant.

Use the available MCP tools whenever the user asks about:
- student attendance
- internal marks

Always call the correct MCP tool for student data.
Do not invent student information.

Give a short and clear answer.
""",
    tools=[mcp_toolset],
)


async def main():
    session_service = InMemorySessionService()

    session = await session_service.create_session(
        app_name="mcp_student_agent_app",
        user_id="rahul",
        session_id="mcp_student_session_1",
    )

    runner = Runner(
        agent=student_mcp_agent,
        app_name="mcp_student_agent_app",
        session_service=session_service,
    )

    print("🎓 MCP Student Information Agent")
    print("Type 'exit' to stop.\n")

    print("Examples:")
    print("• What is the attendance for SNU101?")
    print("• Show internal marks for SNU102.\n")

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
                            print(f"\n Assistant: {part.text}\n")

        except Exception as error:
            print(f"\n Error: {error}\n")


if __name__ == "__main__":
    asyncio.run(main())