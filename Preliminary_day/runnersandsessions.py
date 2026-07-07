import asyncio

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


load_dotenv()


agent = Agent(
    name="StateAssistant",
    model="gemini-2.5-flash",
    instruction="""
    You are a helpful assistant.
    Use the user's name and learning topic from session state when answering.
    """
)


async def main():
    session_service = InMemorySessionService()

    app_name = "state_demo"
    user_id = "user_1"
    session_id = "session_1"

    await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
        state={
            "user_name": "Rahul",
            "topic": "Google ADK"
        }
    )

    runner = Runner(
        agent=agent,
        app_name=app_name,
        session_service=session_service
    )

    user_message = types.Content(
        role="user",
        parts=[
            types.Part(
                text="Hello. What topic am I learning?"
            )
        ]
    )

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=user_message
    ):
        if event.is_final_response():
            print(event.content.parts[0].text)


asyncio.run(main())
```
