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
    Remember information the user shares during this conversation.
    Answer clearly and simply.
    """
)
async def send_message(runner, user_id, session_id, message_text):
    user_message = types.Content(
        role="user",
        parts=[types.Part(text=message_text)]
    )
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=user_message
    ):
        if event.is_final_response():
            print("\nAssistant:", event.content.parts[0].text)
async def main():
    session_service = InMemorySessionService()
    app_name = "state_demo"
    user_id = "user_1"
    session_id = "session_1"
    await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    runner = Runner(
        agent=agent,
        app_name=app_name,
        session_service=session_service
    )
    print("Chat started. Type 'exit' to stop.")
    while True:
        message_text = input("\nYou: ")
        if message_text.lower() == "exit":
            print("Chat ended.")
            break
        await send_message(
            runner,
            user_id,
            session_id,
            message_text
        )
asyncio.run(main())
