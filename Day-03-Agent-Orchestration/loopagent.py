import asyncio
from dotenv import load_dotenv
from google.adk.agents import LlmAgent, LoopAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.exit_loop_tool import exit_loop
from google.genai import types
load_dotenv()
plan_agent = LlmAgent(
    name="plan_agent",
    model="gemini-2.5-flash",
    instruction="""
You are a study-plan writer.

Create or improve a practical study plan for the topic requested by the user.

Your plan must contain:
1. A clear goal
2. Three numbered study steps
3. A daily time recommendation

Keep it short and easy to follow.
""",
    output_key="study_plan",
)
review_agent = LlmAgent(
    name="review_agent",
    model="gemini-2.5-flash",
    instruction="""
You are a study-plan reviewer.

Read the latest plan below:

{study_plan}

Check whether it has all of these:
1. A clear goal
2. Three numbered steps
3. A daily time recommendation

If every requirement is present:
- Return the final plan exactly as it is.
- Call the exit_loop tool immediately.

If any requirement is missing:
- Explain briefly what is missing.
- Do not call exit_loop.
""",
    tools=[exit_loop],
)
study_plan_loop = LoopAgent(
    name="study_plan_loop",
    sub_agents=[
        plan_agent,
        review_agent,
    ],
    max_iterations=3,
)
async def main():
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="loop_study_plan_app",
        user_id="rahul",
        session_id="loop_study_plan_session_1",
    )
    runner = Runner(
        agent=study_plan_loop,
        app_name="loop_study_plan_app",
        session_service=session_service,
    )
    print("📚 Loop Study Plan Agent")
    print("Type 'exit' to stop.\n")
    while True:
        topic = input("Enter a topic to study: ").strip()
        if topic.lower() == "exit":
            print("Goodbye!")
            break
        user_message = types.Content(
            role="user",
            parts=[
                types.Part(
                    text=f"Create a study plan for: {topic}"
                )
            ],
        )
        print("\nCreating and reviewing the plan...\n")
        try:
            async for event in runner.run_async(
                user_id=session.user_id,
                session_id=session.id,
                new_message=user_message,
            ):
                if event.is_final_response() and event.content:
                    for part in event.content.parts:
                        if part.text:
                            print(f"Final Plan:\n{part.text}\n")
        except Exception as error:
            print(f"Unable to create the plan: {error}\n")
if __name__ == "__main__":
    asyncio.run(main())