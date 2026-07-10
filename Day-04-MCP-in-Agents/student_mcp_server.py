from mcp.server.fastmcp import FastMCP
mcp=FastMCP("Student Information server")

students = [
{"id": "SNU101", "name": "Rahul", "attendance": 82.5, "internal_marks": 42},
{"id": "SNU102", "name": "Arjun", "attendance": 68.0, "internal_marks": 35},
{"id": "SNU103", "name": "Karthik", "attendance": 91.0, "internal_marks": 46},
]

@mcp.tool()
def get_student_attendance(student_id:str)->dict:
    '''Get student attendance percentage for the given Student ID,
    return flase if the Student ID is not present'''
    student_id=student_id.lower().strip()

    for student in students:
        if student["id"]==student_id:
            return {
                "success":True,
                "student_id":student["id"],
                "name":student["name"],
                "attendance":student["attendance"]
            }
    return {
        "success":False,
        "message":f"Student ID {student_id} was not found!"
    }
    if __name__=="main":
        mcp.run(transport="stdio")