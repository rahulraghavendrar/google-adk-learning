import asyncio
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.adk.tools import google_search

search_agent=LlmAgent(
    name="SearchAgent",
    model="gemini-2.5-flash",
    instruction='''You are a helpful assistant,perform google searches using the specified given tool''',
    tools=[google_search]
)

async def main():
    session_service=InMemorySessionService()

    session=await session_service.create_session(
        app_name="SearchAgentApp",
        user_id="user1",
        session_id="session1"
    )
    runner=Runner(
        agent=search_agent,
        session_service=session_service,
        app_name="SearchAgentApp"
    )
    print("Chat started. Type 'exit' to stop.")
    while True:
        user_input=input("\nYou: ")
        if user_input.lower()=="exit":
            print("Chat ended.")
            break
        user_message=types.Content(
            role="user",
            parts=[types.Part(text=user_input)]
        )
        async for event in runner.run_async(
            user_id="user1",
            session_id="session1",
            new_message=user_message
        ):
            if event.is_final_response():
                for part in event.content.parts:
                    print("\nAssistant:", part.text)
    if __name__=="__main__":
        asyncio.run(main())