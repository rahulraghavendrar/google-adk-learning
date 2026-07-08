import asyncio

from dotenv import load_dotenv
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
load_dotenv()
students = [
    {"id": "SNU101", "name": "Rahul", "attendance": 82.5},
    {"id": "SNU102", "name": "Arjun", "attendance": 68.0},
    {"id": "SNU103", "name": "Karthik", "attendance": 91.0},
    {"id": "SNU104", "name": "Vikram", "attendance": 74.5},
    {"id": "SNU105", "name": "Naveen", "attendance": 88.0},
    {"id": "SNU106", "name": "Rohan", "attendance": 76.0},
    {"id": "SNU107", "name": "Sanjay", "attendance": 72.0},
    {"id": "SNU108", "name": "Pranav", "attendance": 95.0},
    {"id": "SNU109", "name": "Aditya", "attendance": 80.0},
    {"id": "SNU110", "name": "Jaswanth", "attendance": 69.5},
]
def get_student_details(student_id: str) -> dict:
    """Finds a student and returns their attendance details."""
    student_id = student_id.upper().strip()
    for student in students:
        if student["id"] == student_id:
            return {
                "success": True,
                "data": student,
                "message": "Student found.",
            }
    return {
        "success": False,
        "data": None,
        "message": f"No student found with ID {student_id}.",
    }
attendance_agent = LlmAgent(
    name="attendance_agent",
    model="gemini-2.0-flash",
    instruction="""
You are an attendance specialist.
Use the get_student_details tool whenever the user provides a student ID.
Return only one clear result:
- If the student exists, write the student's name, ID, and attendance percentage.
- If the student does not exist, clearly say that the student ID was not found.
""",
    tools=[get_student_details],
    output_key="attendance_result",
)
eligibility_agent = LlmAgent(
    name="eligibility_agent",
    model="gemini-2.0-flash",
    instruction="""
You are an exam eligibility specialist.
Read the previous attendance-agent result below:
{attendance_result}
Rules:
- A student is eligible when attendance is 75% or above.
- A student is not eligible when attendance is below 75%.
- If the student ID was not found, clearly say eligibility cannot be checked.
- Give a short final answer with the exam status.
""",
)
student_eligibility_pipeline = SequentialAgent(
    name="student_eligibility_pipeline",
    sub_agents=[
        attendance_agent,
        eligibility_agent,
    ],
)
async def main():
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="student_eligibility_app",
        user_id="rahul",
        session_id="eligibility_session_1",
    )
    runner = Runner(
        agent=student_eligibility_pipeline,
        app_name="student_eligibility_app",
        session_service=session_service,
    )

    print("Student Exam Eligibility Checker")
    print("Type 'exit' to stop.\n")

    print("Available student IDs:")
    for student in students:
        print(f'{student["id"]} - {student["name"]}')
    print()
    while True:
        student_id = input("Enter a student ID: ").strip()

        if student_id.lower() == "exit":
            print("Goodbye!")
            break
        user_message = types.Content(
            role="user",
            parts=[
                types.Part(
                    text=f"Check exam eligibility for student ID {student_id}."
                )
            ],
        )
        async for event in runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=user_message,
        ):
            if event.is_final_response() and event.content:
                for part in event.content.parts:
                    if part.text:
                        print(f"\n Result: {part.text}\n")
if __name__ == "__main__":
    asyncio.run(main())