import asyncio

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


load_dotenv()


def add_numbers(first_number: float, second_number: float) -> dict:
    """Adds two numbers and returns the result."""
    return {
        "success": True,
        "data": {
            "result": first_number + second_number,
        },
        "message": "Addition completed successfully.",
    }


def calculate_discount(
    original_price: float,
    discount_percentage: float,
) -> dict:
    """Calculates the final price after a discount from 0 to 100 percent."""
    if original_price < 0:
        return {
            "success": False,
            "data": None,
            "message": "Original price cannot be negative.",
        }

    if discount_percentage < 0 or discount_percentage > 100:
        return {
            "success": False,
            "data": None,
            "message": "Discount percentage must be between 0 and 100.",
        }

    final_price = original_price - (
        original_price * discount_percentage / 100
    )

    return {
        "success": True,
        "data": {
            "final_price": final_price,
        },
        "message": "Discount calculated successfully.",
    }


def get_study_tip(subject: str) -> dict:
    """Returns a short study tip for Python, ADK, or general study."""
    tips = {
        "python": "Practice one small program daily and understand each line.",
        "adk": "Build small agents first, then add tools one by one.",
        "general": "Study for 25 minutes, then take a 5-minute break.",
    }

    subject = subject.lower().strip()

    tip = tips.get(
        subject,
        "Break the topic into small parts and practise with examples.",
    )

    return {
        "success": True,
        "data": {
            "subject": subject,
            "tip": tip,
        },
        "message": "Study tip found.",
    }


study_helper = LlmAgent(
    name="study_helper",
    model="gemini-2.0-flash",
    instruction="""
You are a friendly study helper.

Use the available tools whenever the user asks for:
- addition,
- a discount calculation,
- a study tip.

Do not calculate or invent tool results yourself.
Keep answers short and clear.
""",
    tools=[
        add_numbers,
        calculate_discount,
        get_study_tip,
    ],
)


async def main():
    session_service = InMemorySessionService()

    session = await session_service.create_session(
        app_name="study_helper_app",
        user_id="rahul",
        session_id="study_session_1",
    )

    runner = Runner(
        agent=study_helper,
        app_name="study_helper_app",
        session_service=session_service,
    )

    print("📚 Study Helper is ready!")
    print("Type 'exit' to stop.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("🤖 Study Helper: Goodbye!")
            break

        user_message = types.Content(
            role="user",
            parts=[types.Part(text=user_input)],
        )

        async for event in runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=user_message,
        ):
            if event.is_final_response():
                for part in event.content.parts:
                    if part.text:
                        print(f"🤖 Study Helper: {part.text}")


if __name__ == "__main__":
    asyncio.run(main())