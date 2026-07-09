import asyncio
from dotenv import load_dotenv
from google.adk.agents import LlmAgent, ParallelAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
load_dotenv()
students = [
    {"id": "SNU101", "name": "Rahul", "attendance": 82.5, "internal_marks": 42},
    {"id": "SNU102", "name": "Arjun", "attendance": 68.0, "internal_marks": 35},
    {"id": "SNU103", "name": "Karthik", "attendance": 91.0, "internal_marks": 46},
    {"id": "SNU104", "name": "Vikram", "attendance": 74.5, "internal_marks": 38},
    {"id": "SNU105", "name": "Naveen", "attendance": 88.0, "internal_marks": 44},
    {"id": "SNU106", "name": "Rohan", "attendance": 76.0, "internal_marks": 40},
    {"id": "SNU107", "name": "Sanjay", "attendance": 72.0, "internal_marks": 33},
    {"id": "SNU108", "name": "Pranav", "attendance": 95.0, "internal_marks": 48},
    {"id": "SNU109", "name": "Aditya", "attendance": 80.0, "internal_marks": 41},
    {"id": "SNU110", "name": "Jaswanth", "attendance": 69.5, "internal_marks": 36},
    {"id": "SNU111", "name": "Aarav", "attendance": 78.5, "internal_marks": 39},
    {"id": "SNU112", "name": "Bharath", "attendance": 64.0, "internal_marks": 31},
    {"id": "SNU113", "name": "Charan", "attendance": 86.5, "internal_marks": 45},
    {"id": "SNU114", "name": "Deepak", "attendance": 73.0, "internal_marks": 37},
    {"id": "SNU115", "name": "Eshwar", "attendance": 92.0, "internal_marks": 47},
    {"id": "SNU116", "name": "Farhan", "attendance": 75.0, "internal_marks": 40},
    {"id": "SNU117", "name": "Gokul", "attendance": 70.5, "internal_marks": 34},
    {"id": "SNU118", "name": "Harish", "attendance": 84.0, "internal_marks": 43},
    {"id": "SNU119", "name": "Irfan", "attendance": 67.5, "internal_marks": 32},
    {"id": "SNU120", "name": "Jeevan", "attendance": 89.5, "internal_marks": 46},
]
def get_student_attendance(student_id: str) -> dict:
    """Returns attendance details for a student ID."""
    student_id = student_id.upper().strip()
    for student in students:
        if student["id"] == student_id:
            return {
                "success": True,
                "data": {
                    "id": student["id"],
                    "name": student["name"],
                    "attendance": student["attendance"],
                },
                "message": "Attendance found.",
            }
    return {
        "success": False,
        "data": None,
        "message": f"Student ID {student_id} was not found.",
    }
def get_internal_marks(student_id: str) -> dict:
    """Returns internal marks for a student ID."""
    student_id = student_id.upper().strip()

    for student in students:
        if student["id"] == student_id:
            return {
                "success": True,
                "data": {
                    "id": student["id"],
                    "name": student["name"],
                    "internal_marks": student["internal_marks"],
                },
                "message": "Internal marks found.",
            }

    return {
        "success": False,
        "data": None,
        "message": f"Student ID {student_id} was not found.",
    }
attendance_agent = LlmAgent(
    name="attendance_agent",
    model="gemini-2.5-flash",
    instruction="""
You are the Attendance Agent.

Your only responsibility is attendance.

The user message contains a student ID.
You MUST call the get_student_attendance tool for that ID.

Do not discuss internal marks.
Do not say you cannot provide internal marks.
Do not ask follow-up questions.

After the tool returns:
- If success is true, respond only with the student's name, ID, and attendance percentage.
- If success is false, respond only with the tool's message.
""",
    tools=[get_student_attendance],
    output_key="attendance_result",
)
marks_agent = LlmAgent(
    name="marks_agent",
    model="gemini-2.5-flash",
    instruction="""
You are the Internal Marks Agent.

Your only responsibility is internal marks.

The user message contains a student ID.
You MUST call the get_internal_marks tool for that ID.

Do not discuss attendance.
Do not say you cannot provide attendance.
Do not ask follow-up questions.

After the tool returns:
- If success is true, respond only with the student's name, ID, and internal marks out of 50.
- If success is false, respond only with the tool's message.
""",
    tools=[get_internal_marks],
    output_key="marks_result",
)
student_information_parallel = ParallelAgent(
    name="student_information_parallel",
    sub_agents=[
        attendance_agent,
        marks_agent,
    ],
)
async def main():
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="parallel_student_information_app",
        user_id="rahul",
        session_id="parallel_student_session_1",
    )
    runner = Runner(
        agent=student_information_parallel,
        app_name="parallel_student_information_app",
        session_service=session_service,
    )
    print("🎓 Parallel Student Information Checker")
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
                    text=f"Student ID: {student_id}"
                )
            ],
        )
        print("\nChecking attendance and marks at the same time...\n")
        try:
            async for event in runner.run_async(
                user_id=session.user_id,
                session_id=session.id,
                new_message=user_message,
            ):
                if event.is_final_response() and event.content:
                    for part in event.content.parts:
                        if part.text:
                            print(f"Result: {part.text}\n")
        except Exception as error:
            print(f"Unable to get results: {error}\n")
if __name__ == "__main__":
    asyncio.run(main())