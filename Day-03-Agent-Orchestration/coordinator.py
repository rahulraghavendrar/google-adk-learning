import asyncio
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
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
def find_student(student_id: str) -> dict:
    """Finds and returns a student dictionary for the given student ID."""
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
        "message": f"Student ID {student_id} was not found.",
    }
def get_student_attendance(student_id: str) -> dict:
    """Returns attendance information for the given student ID."""
    result = find_student(student_id)
    if not result["success"]:
        return result
    student = result["data"]
    return {
        "success": True,
        "data": {
            "id": student["id"],
            "name": student["name"],
            "attendance": student["attendance"],
        },
        "message": "Attendance found.",
    }
def get_internal_marks(student_id: str) -> dict:
    """Returns internal marks information for the given student ID."""
    result = find_student(student_id)
    if not result["success"]:
        return result
    student = result["data"]
    return {
        "success": True,
        "data": {
            "id": student["id"],
            "name": student["name"],
            "internal_marks": student["internal_marks"],
        },
        "message": "Internal marks found.",
    }
def get_exam_eligibility(student_id: str) -> dict:
    """Returns exam eligibility based on attendance. Minimum attendance is 75 percent."""
    result = find_student(student_id)
    if not result["success"]:
        return result
    student = result["data"]
    attendance = student["attendance"]
    if attendance >= 75:
        exam_status = "Eligible to attend the exam."
    else:
        exam_status = "Not eligible to attend the exam."
    return {
        "success": True,
        "data": {
            "id": student["id"],
            "name": student["name"],
            "attendance": attendance,
            "exam_status": exam_status,
        },
        "message": "Eligibility checked.",
    }
attendance_agent = LlmAgent(
    name="attendance_agent",
    model="gemini-2.5-flash",
    instruction="""
You are the Attendance Agent.

Your only responsibility is to answer attendance questions.

When the user provides a student ID, you MUST call
the get_student_attendance tool.

After the tool returns:
- If success is true, state the student's name, ID, and attendance percentage.
- If success is false, state the tool's message.
Keep the response short.
""",
    tools=[get_student_attendance],
)
marks_agent = LlmAgent(
    name="marks_agent",
    model="gemini-2.5-flash",
    instruction="""
You are the Internal Marks Agent.

Your only responsibility is to answer internal-marks questions.

When the user provides a student ID, you MUST call
the get_internal_marks tool.

After the tool returns:
- If success is true, state the student's name, ID, and internal marks out of 50.
- If success is false, state the tool's message.
Keep the response short.
""",
    tools=[get_internal_marks],
)
eligibility_agent = LlmAgent(
    name="eligibility_agent",
    model="gemini-2.5-flash",
    instruction="""
You are the Exam Eligibility Agent.

Your only responsibility is to answer exam-eligibility questions.

When the user provides a student ID, you MUST call
the get_exam_eligibility tool.

After the tool returns:
- If success is true, state the student's name, ID, attendance percentage,
  and exam eligibility status.
- If success is false, state the tool's message.
Keep the response short.
""",
    tools=[get_exam_eligibility],
)
coordinator_agent = LlmAgent(
    name="student_coordinator",
    model="gemini-2.5-flash",
    instruction="""
You are a Student Information Coordinator.

Your job is to delegate the user's request to exactly one specialist agent.

Routing rules:
- For attendance questions, delegate to attendance_agent.
- For internal marks or marks questions, delegate to marks_agent.
- For exam eligibility, exam permission, or whether a student can attend an exam,
  delegate to eligibility_agent.

Do not answer student questions yourself.
Do not invent student data.
If the request does not contain a student ID, ask the user to provide one.
""",
    sub_agents=[
        attendance_agent,
        marks_agent,
        eligibility_agent,
    ],
)
async def main():
    session_service = InMemorySessionService()

    session = await session_service.create_session(
        app_name="student_coordinator_app",
        user_id="rahul",
        session_id="student_coordinator_session_1",
    )

    runner = Runner(
        agent=coordinator_agent,
        app_name="student_coordinator_app",
        session_service=session_service,
    )

    print("🎓 Student Coordinator Agent")
    print("Type 'exit' to stop.\n")
    print("Examples:")
    print("- What is the attendance for SNU101?")
    print("- Show internal marks for SNU112.")
    print("- Can SNU102 attend the exam?\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
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
                            print(f"\nAssistant: {part.text}\n")

        except Exception as error:
            print(f"\nUnable to process the request: {error}\n")
if __name__ == "__main__":
    asyncio.run(main())