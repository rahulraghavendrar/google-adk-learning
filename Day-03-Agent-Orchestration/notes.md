# 🤝 Day 3 — Agent Orchestration & Multi-Agent Systems

## 🎯 Day 3 Goal

The goal of Day 3 is to understand how multiple agents can work together in one application.

Instead of making one large agent handle every task, we can create smaller specialized agents and coordinate them.

```text
👤 User request
        ↓
🧭 Coordinator or workflow agent
        ↓
🤖 Specialized agents
        ↓
💬 Final response
```

---

# 🧩 Why Use Multiple Agents?

A single agent can handle many tasks, but it can become difficult to manage when it has too many responsibilities.

For example, one large agent may need to:

```text
🧮 Perform calculations
📚 Give study tips
📁 Search files
📧 Draft emails
🗃️ Query databases
🔐 Apply security rules
```

As the number of tasks increases, the agent may have:

* Long instructions
* Too many tools
* More confusion when choosing tools
* Harder debugging
* Harder testing

A multi-agent system divides work among smaller agents.

```text
❌ One overloaded agent
→ Many tools
→ Long instructions
→ More chances of confusion

✅ Multiple specialized agents
→ Smaller instructions
→ Fewer tools per agent
→ Clear responsibilities
```

---

## 🧩 Decomposition

**Decomposition** means splitting one large problem into smaller tasks.

Example request:

> Calculate the discounted price of ₹2,000 and give a Python study tip.

A multi-agent system can split this into two jobs:

```text
👤 User request
        ↓
🧭 Coordinator understands the request
        ↓
🧮 Calculator Agent
→ Calculates the discounted price

📚 Study Agent
→ Gives a Python study tip
        ↓
💬 Final combined answer
```

Each agent focuses on one part of the request.

---

## 🎯 Specialization

**Specialization** means each agent has one clear role.

```text
🧮 Calculator Agent
→ Handles arithmetic and discounts

📚 Study Agent
→ Handles study guidance

🎓 Attendance Agent
→ Finds attendance information

✅ Eligibility Agent
→ Decides exam eligibility
```

Specialized agents are useful because they have:

* Focused instructions
* Only relevant tools
* Less chance of selecting an unrelated tool
* Easier testing and debugging

For example, an attendance agent does not need a discount-calculation tool.

---

## 🛡️ Reliability

A multi-agent system can be more reliable because each agent is smaller and easier to test.

```text
Single large agent:
❓ Did it choose the correct tool?
❓ Did it follow all instructions?
❓ Which part caused an error?

Multi-agent system:
✅ Test the attendance agent separately
✅ Test the eligibility agent separately
✅ Test the workflow separately
```

If one agent has a problem, it can be fixed without changing every other agent.

---

## 🏪 Simple Analogy

A multi-agent system is similar to a store.

```text
👤 Customer
        ↓
🧭 Reception desk
        ↓
🧮 Billing counter
📦 Delivery counter
🛠️ Customer support counter
```

The reception desk does not perform every task. It understands the request and sends the customer to the right specialist.

```text
🧭 Coordinator agent
= Reception desk

🤖 Specialized agents
= Individual counters
```

---

## ⚖️ Single Agent vs Multi-Agent System

| Area             | Single Agent              | Multi-Agent System                |
| ---------------- | ------------------------- | --------------------------------- |
| Responsibilities | Many tasks in one agent   | Split across agents               |
| Instructions     | Can become long           | Short and focused                 |
| Tools            | Large tool list           | Relevant tools only               |
| Testing          | Harder as the app grows   | Agents can be tested separately   |
| Best for         | Small/simple applications | Larger or mixed-task applications |

---

## ⚠️ When Not to Use Multiple Agents

Multiple agents are not always necessary.

Use a single agent when:

* The task is small
* One set of tools is enough
* There is no clear reason to split responsibilities
* Extra routing would only add complexity

```text
🧠 Start simple.

Use multiple agents only when specialization
or coordination improves the application.
```

---

# ➡️ Sequential Agents

A **sequential agent workflow** means agents run in a fixed order.

One agent finishes its work first. Then the next agent uses the previous result.

```text
Agent 1
   ↓
Agent 2
   ↓
Agent 3
   ↓
Final result
```

Sequential workflows are also called:

```text
➡️ Pipelines
➡️ Step-by-step workflows
```

---

## 🧪 Student Exam Eligibility Example

We created a student eligibility workflow.

The user enters a student ID.

```text
👤 User enters: SNU101
        ↓
🎓 Attendance Agent
→ Finds the student's attendance
        ↓
✅ Eligibility Agent
→ Uses the attendance percentage
→ Decides exam eligibility
        ↓
💬 Final exam status
```

Example:

```text
SNU101
        ↓
Attendance Agent finds Rahul
        ↓
Attendance = 82.5%
        ↓
Eligibility Agent checks:
82.5 >= 75
        ↓
Eligible to attend the exam
```

This is sequential because the eligibility agent cannot decide anything until the attendance agent finds the attendance percentage.

---

## 📋 Student List

The student list is created in the main program.

Each student is stored as a dictionary.

```python
students = [
    {"id": "SNU101", "name": "Rahul", "attendance": 82.5},
    {"id": "SNU102", "name": "Arjun", "attendance": 68.0},
    {"id": "SNU103", "name": "Karthik", "attendance": 91.0},
]
```

Each dictionary has:

```text
"id"         → Student ID
"name"       → Student name
"attendance" → Attendance percentage
```

The full program contains students from `SNU101` to `SNU120`.

---

# 🛠️ Custom Tool: `get_student_details`

```python
def get_student_details(student_id: str) -> dict:
```

This is a custom tool used by the attendance agent.

Its job is to search the student list and return the correct student details.

Example input:

```text
SNU101
```

Example output:

```python
{
    "success": True,
    "data": {
        "id": "SNU101",
        "name": "Rahul",
        "attendance": 82.5,
    },
    "message": "Student found.",
}
```

If the student ID does not exist:

```python
{
    "success": False,
    "data": None,
    "message": "No student found with ID SNU999.",
}
```

---

## 🧹 `upper()` and `strip()`

```python
student_id = student_id.upper().strip()
```

This cleans the user input.

```text
User types: " snu101 "
        ↓
.strip()
        ↓
"snu101"
        ↓
.upper()
        ↓
"SNU101"
```

This means all of these work:

```text
SNU101
snu101
Snu101
 snu101
```

---

## 🔁 `for student in students`

```python
for student in students:
```

This loops through every student dictionary in the list.

```text
Student 1 → SNU101
Student 2 → SNU102
Student 3 → SNU103
...
```

The program checks each student:

```python
if student["id"] == student_id:
```

If the ID matches, it returns the student details.

---

## 📤 `return`

```python
return {
    "success": True,
    "data": student,
    "message": "Student found.",
}
```

`return` sends a value back from the function and stops that function.

```text
Function searches student list
        ↓
Finds matching student
        ↓
Returns student details
        ↓
Function ends
```

---

# 🤖 `LlmAgent`

An `LlmAgent` is an AI agent powered by an LLM such as Gemini.

```python
attendance_agent = LlmAgent(
    name="attendance_agent",
    model="gemini-2.0-flash",
    instruction="...",
    tools=[get_student_details],
    output_key="attendance_result",
)
```

The attendance agent has one job:

```text
🎓 Find student details and attendance information.
```

It has access to this tool:

```python
tools=[get_student_details]
```

This gives the attendance agent permission to call only the student-details tool.

---

# 🧩 `SequentialAgent`

```python
student_eligibility_pipeline = SequentialAgent(
    name="student_eligibility_pipeline",
    sub_agents=[
        attendance_agent,
        eligibility_agent,
    ],
)
```

`SequentialAgent` is a parent workflow agent.

It runs child agents one by one in the order written inside `sub_agents`.

```text
SequentialAgent
= Parent workflow agent that runs sub-agents in sequence.
```

In this workflow:

```text
attendance_agent
        ↓ runs first
eligibility_agent
        ↓ runs second
final response
```

The order matters.

```python
sub_agents=[
    attendance_agent,
    eligibility_agent,
]
```

* First item runs first.
* Second item runs after the first agent finishes.

If the eligibility agent ran first, it would not have attendance information yet.

---

# 📦 `output_key`

```python
output_key="attendance_result"
```

`output_key` tells ADK to save the final response of an agent in session state.

```text
Attendance Agent finishes
        ↓
ADK saves the result using:
attendance_result
```

Conceptually, session state can be imagined as a shared dictionary:

```python
state = {
    "attendance_result": "Rahul, ID SNU101, has 82.5% attendance."
}
```

The next agent can read this saved value.

---

# 🗒️ Shared Session State

**Session state** is shared information that agents in the same workflow can use.

```text
🎓 Attendance Agent
→ Writes attendance result

📦 Shared session state
→ Stores the result

✅ Eligibility Agent
→ Reads the result
```

This allows agents to pass information without directly calling each other like normal Python functions.

---

# 🔄 `{attendance_result}`

Inside the eligibility agent instruction:

```python
instruction="""
You are an exam eligibility specialist.

Read the previous attendance-agent result below:

{attendance_result}
"""
```

The curly braces tell ADK to insert the saved value from session state.

For example, ADK can turn this:

```text
{attendance_result}
```

into:

```text
Rahul, ID SNU101, has 82.5% attendance.
```

Then the eligibility agent can decide:

```text
82.5 >= 75
        ↓
Eligible to attend the exam
```

---

# 🎓 Attendance Agent

The attendance agent is responsible for finding student details.

```text
Input:
SNU101

Task:
Use `get_student_details`

Output:
Rahul has 82.5% attendance
```

It stores its response using:

```python
output_key="attendance_result"
```

---

# ✅ Eligibility Agent

The eligibility agent is responsible only for deciding exam eligibility.

It reads the attendance result from session state.

Rules:

```text
Attendance >= 75%
→ Eligible to attend the exam

Attendance < 75%
→ Not eligible to attend the exam
```

If the student ID is not found:

```text
Student ID not found
→ Eligibility cannot be checked
```

---

# 🔄 Complete Workflow

```text
👤 User enters: SNU101
        ↓
🧭 SequentialAgent starts

1️⃣ Attendance Agent runs
   ↓
Calls `get_student_details("SNU101")`
   ↓
Tool finds Rahul with 82.5% attendance
   ↓
Attendance Agent creates a clear response
   ↓
ADK saves it as:
`attendance_result`

2️⃣ Eligibility Agent runs
   ↓
Reads `{attendance_result}`
   ↓
Checks whether attendance is at least 75%
   ↓
💬 Rahul is eligible to attend the exam.
```

---

# ✅ Day 3 Progress So Far

```text
✅ Why multi-agent systems are useful
✅ Decomposition
✅ Specialization
✅ Reliability
✅ Single agent vs multi-agent systems
✅ Sequential workflows
✅ `SequentialAgent`
✅ `sub_agents`
✅ Custom tools inside a workflow
✅ `output_key`
✅ Shared session state
✅ Passing one agent's output to another agent
✅ Student eligibility sequential pipeline
```
