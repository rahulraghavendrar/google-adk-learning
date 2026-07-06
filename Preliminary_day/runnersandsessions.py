import asyncio

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

def square_number(number: int) -> int:
    return number * number

agent=Agent(
    name="MathAgent",
    model="gemini-2.5-flash",
    instruction='''You are a helpful math assistant
    Use the square tool whenever asked to square a number.''',
    tools=[square_number]
)
async def main():
    session_service = InMemorySessionService()

    app_name="MathAgentApp"
    user_id="user123"
    session_id="session456"

    await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    runner=Runner(
        agent=agent,
        session_service=session_service
        app_name=app_name
    )
    user_message=types.Message(
        role="user",
        content="Please square the number 7."
    )
    async for message in runner.stream_messages(
        user_message=user_message,
        session_id=session_id
    ):
        print(f"{message.role}: {message.content}") 
        