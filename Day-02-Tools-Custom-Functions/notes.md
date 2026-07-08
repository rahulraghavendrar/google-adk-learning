# 🛠️ Day 2 — Tools & Custom Functions

## 🎯 Day 2 Goal

Learn how to create useful Python functions and give them to a Google ADK agent as **tools**.

By the end of Day 2, the agent will be able to:

* **Choose the correct tool**
* **Send correct inputs to the tool**
* **Receive the tool result**
* **Give a clear response to the user**
* **Handle errors safely**
* **Use multiple custom tools**

---

# 🧭 Day 2 Topics

```text
1️⃣ Function tools
2️⃣ Type hints and docstrings
3️⃣ Built-in tools vs custom tools
4️⃣ Tool return types and structured outputs
5️⃣ Error handling and retries
6️⃣ Long-running tools and async patterns
7️⃣ Callbacks and guardrails
8️⃣ Lab 2 — Build an agent with 3–4 custom tools
```

---

# 🧩 Topic 1 — Function Tools

## 🤔 What is a function tool?

A **function tool** is a normal Python function that an ADK agent is allowed to call.

```text
🐍 Normal Python function
        +
🤖 Given to an ADK agent
        =
🛠️ Function tool
```

For example:

```python
def add_numbers(first_number: float, second_number: float) -> float:
    """Adds two numbers and returns the result."""
    return first_number + second_number
```

This is a normal Python function.

When we add it to an ADK agent like this:

```python
tools=[add_numbers]
```

the agent can use it as a tool.

---

## 🧮 Example: Calculator Tool Flow

Suppose the user asks:

> **Add 25 and 17.**

The flow is:

```text
👤 User: Add 25 and 17
        ↓
🤖 Agent understands this is an addition question
        ↓
🛠️ Agent chooses `add_numbers`
        ↓
⚙️ Python runs: add_numbers(25, 17)
        ↓
📤 Tool returns: 42
        ↓
💬 Agent replies: 25 + 17 = 42
```

```text
🤖 Agent = decides which tool to use

🛠️ Tool = performs the actual action
```

---

## 🧱 Basic Function Tool Structure

```python
def function_name(parameter_name: type) -> return_type:
    """Clear explanation of what this tool does."""
    return result
```

| Part             | Meaning                            |
| ---------------- | ---------------------------------- |
| `def`            | Creates a Python function          |
| `function_name`  | Name of the tool                   |
| `parameter_name` | Input needed by the tool           |
| `: type`         | Expected data type of the input    |
| `-> return_type` | Type of value returned by the tool |
| `"""..."""`      | Docstring that explains the tool   |
| `return`         | Sends the result back              |

---

## 🧪 Example: Discount Calculator Tool

```python
def calculate_discount(
    original_price: float,
    discount_percentage: float,
) -> float:
    """Calculates the final price after applying a percentage discount."""
    discount_amount = original_price * (discount_percentage / 100)
    return original_price - discount_amount
```

Example:

```python
final_price = calculate_discount(2000, 15)

print(final_price)
```

Output:

```text
1700.0
```

Explanation:

```text
💰 Original price = 2000
🏷️ Discount = 15%

15% of 2000 = 300

Final price = 2000 - 300 = 1700
```

---

## 🧠 How Does the LLM Understand a Tool?

ADK mainly uses these details:

```text
1️⃣ Function name
2️⃣ Parameter names
3️⃣ Type hints
4️⃣ Docstring
```

From this function:

```python
def calculate_discount(
    original_price: float,
    discount_percentage: float,
) -> float:
    """Calculates the final price after applying a percentage discount."""
```

the LLM can understand something like:

```text
🛠️ Tool name: calculate_discount

📋 Purpose:
Calculate the final price after a discount.

📥 Inputs:
- original_price → number
- discount_percentage → number

📤 Output:
- final price → number
```

If a user asks:

> **What is the final price of ₹2,000 after a 15% discount?**

the agent can call:

```python
calculate_discount(
    original_price=2000,
    discount_percentage=15,
)
```

---

## ❌ Bad Tool Design vs ✅ Good Tool Design

### ❌ Bad Tool

```python
def process(a, b):
    return a - (a * b / 100)
```

Problems:

```text
❌ `process` does not explain the action
❌ `a` and `b` are unclear
❌ No type hints
❌ No docstring
```

### ✅ Good Tool

```python
def calculate_discount(
    original_price: float,
    discount_percentage: float,
) -> float:
    """Calculates the final price after applying a percentage discount."""
    return original_price - (original_price * discount_percentage / 100)
```

Why it is better:

```text
✅ Clear function name
✅ Clear parameter names
✅ Type hints
✅ Clear docstring
```

---

## ⚠️ `function_name` vs `function_name()`

When giving a function to an ADK agent:

```python
tools=[calculate_discount]
```

Do **not** write:

```python
tools=[calculate_discount()]
```

Difference:

```text
calculate_discount
→ Gives the function itself to the agent.

calculate_discount()
→ Immediately tries to run the function.
```

The agent needs the function itself so it can decide:

* **When to use it**
* **What input values to send**
* **Whether another tool is more suitable**

---

## 🌍 Examples of Function Tools

| Tool                            | What it does                |
| ------------------------------- | --------------------------- |
| `calculate_discount()`          | Calculates discounted price |
| `get_weather(city)`             | Gets weather information    |
| `search_employee(employee_id)`  | Finds employee data         |
| `get_stock_price(symbol)`       | Fetches a stock price       |
| `create_task(title)`            | Adds a task                 |
| `send_email(to, subject, body)` | Sends an email              |

```text
🛠️ A tool gives an agent an ability.

Without tools:
🤖 “I can answer using my knowledge.”

With tools:
🤖 “I can take actions and get fresh results.”
```

---

# 🏷️ Topic 2 — Type Hints & Docstrings

## 🔤 What are Type Hints?

**Type hints** tell us what kind of data a function expects and returns.

Example:

```python
def add_numbers(first_number: float, second_number: float) -> float:
    """Adds two numbers and returns the result."""
    return first_number + second_number
```

Read it like this:

```text
first_number: float
→ first_number should be a number

second_number: float
→ second_number should be a number

-> float
→ the function returns a number
```

---

## 🧩 Common Type Hints

| Type hint   | Meaning                    | Example                 |
| ----------- | -------------------------- | ----------------------- |
| `str`       | Text                       | `"Rahul"`               |
| `int`       | Whole number               | `25`                    |
| `float`     | Number, including decimals | `99.5`                  |
| `bool`      | True or False              | `True`                  |
| `list[str]` | List of text values        | `["Python", "ADK"]`     |
| `dict`      | Key-value data             | `{"status": "success"}` |
| `None`      | No value returned          | `None`                  |

---

## 🧪 Example: Student Result Tool

```python
def get_student_result(student_name: str, subject: str) -> str:
    """Returns the result status for a student in a given subject."""
    return f"{student_name} has passed {subject}."
```

The agent can understand it as:

```text
🛠️ Tool name: get_student_result

📥 Inputs:
- student_name → text
- subject → text

📤 Output:
- text

📋 Purpose:
Return a student's result status for a subject.
```

Example tool call:

```python
get_student_result(
    student_name="Rahul",
    subject="Python",
)
```

---

## ❌ Function Without Type Hints

```python
def result(a, b):
    return f"{a} has passed {b}"
```

Problems:

```text
❌ What is `result`?
❌ What does `a` represent?
❌ What does `b` represent?
❌ Are the values text, numbers, or something else?
```

Python can run it, but it is not a good tool for an agent.

---

## 📋 What is a Docstring?

A **docstring** is a description written inside triple quotes directly below a function definition.

```python
def get_weather(city: str) -> str:
    """Returns the current weather summary for the given city."""
    return f"The weather in {city} is sunny."
```

The docstring is:

```python
"""Returns the current weather summary for the given city."""
```

It tells the agent the **purpose** of the tool.

---

## 🧠 Why Do Docstrings Matter?

The agent uses the docstring to decide:

```text
🤔 Should I use this tool?
🤔 What does this tool do?
🤔 When should I use it?
🤔 What kind of result will it return?
```

Example:

```python
def get_weather(city: str) -> str:
    """Returns the current weather summary for the given city."""
```

```python
def get_temperature(city: str) -> float:
    """Returns only the current temperature in Celsius for the given city."""
```

| User question                         | Best tool               |
| ------------------------------------- | ----------------------- |
| “How is the weather in Chennai?”      | `get_weather()` 🌦️     |
| “What is the temperature in Chennai?” | `get_temperature()` 🌡️ |

---

## ✍️ Good Docstring Style

Use this pattern:

```text
Verb + what the tool does + important condition
```

Examples:

```python
"""Adds two numbers and returns the result."""
```

```python
"""Calculates the final price after applying a percentage discount."""
```

```python
"""Searches the employee database by employee ID and returns profile details."""
```

```python
"""Divides two numbers and returns an error message if the divisor is zero."""
```

---

## ⚠️ Mention Important Restrictions

If a tool has a limitation, explain it in the docstring.

```python
def divide_numbers(first_number: float, second_number: float) -> float | str:
    """Divides two numbers. Returns an error message if the second number is zero."""
    if second_number == 0:
        return "Error: Division by zero is not allowed."
    return first_number / second_number
```

This makes the tool safer for requests such as:

```text
Divide 10 by 0
```

---

## 🧠 Type Hints + Docstrings Work Together

```python
def convert_celsius_to_fahrenheit(celsius: float) -> float:
    """Converts a temperature from Celsius to Fahrenheit."""
    return (celsius * 9 / 5) + 32
```

ADK can understand this approximately as:

```text
🛠️ Tool: convert_celsius_to_fahrenheit

📋 Purpose:
Convert Celsius to Fahrenheit.

📥 Input:
- celsius → number

📤 Output:
- number
```

```text
✨ Better names + type hints + docstrings
   = better tool calls and fewer mistakes.
```

---

## 🧪 Example with Multiple Data Types

```python
def create_task(title: str, priority: int, completed: bool) -> dict:
    """Creates a task and returns its details."""
    return {
        "title": title,
        "priority": priority,
        "completed": completed,
    }
```

Example:

```python
task = create_task(
    title="Finish ADK Day 2",
    priority=1,
    completed=False,
)

print(task)
```

Output:

```text
{
    "title": "Finish ADK Day 2",
    "priority": 1,
    "completed": False
}
```

---

## 🚫 Avoid Vague Inputs

### ❌ Less Clear

```python
def create_user(data: dict) -> dict:
    """Creates a user."""
```

The agent does not know which keys are required inside `data`.

### ✅ Better

```python
def create_user(name: str, email: str, age: int) -> dict:
    """Creates a user profile using a name, email address, and age."""
```

Now the agent knows exactly what information it needs.

---

```

---
# 🧰 Built-in Tools vs Custom Tools

An ADK agent can use two main kinds of tools:

```text
1️⃣ Built-in tools
2️⃣ Custom tools
```

Both allow an agent to perform actions. The main difference is **who created the tool**.

---

## 🧰 Built-in Tools

**Built-in tools** are ready-made capabilities provided by ADK, a provider, or a connected service.

You do not write the main tool logic yourself. You import or configure the tool, then give it to the agent.

```text
🏢 Framework or provider creates the tool
        ↓
🤖 You connect it to your agent
        ↓
🛠️ Agent can use it
```

Examples of built-in or connected capabilities include:

* **🌐 Web search**
* **📁 File access**
* **🗃️ Database access**
* **💻 Code execution**
* **🔌 MCP tool connections**

Example idea using a built-in search tool:

```python
from google.adk.tools import google_search
```

```python
tools=[google_search]
```

```text
`google_search` is already created by ADK.

We only import it and give the agent permission to use it.
```

A search agent may work like this:

```text
👤 User: What are the latest Google ADK updates?
        ↓
🤖 Agent understands that current web information is needed
        ↓
🧰 Agent uses the Google Search tool
        ↓
🌐 Search tool returns information
        ↓
💬 Agent gives a clear answer
```

---

## 🛠️ Custom Tools

**Custom tools** are Python functions that we create for our own application.

```text
👨‍💻 We write the Python function
        ↓
🤖 Add it inside `tools=[...]`
        ↓
🛠️ Agent can call it
```

Example:

```python
def calculate_discount(
    original_price: float,
    discount_percentage: float,
) -> float:
    """Calculates the final price after applying a percentage discount."""
    return original_price - (original_price * discount_percentage / 100)
```

This is a custom tool because we wrote the function ourselves.

Example use case:

```text
👤 User: What is the final price of ₹2,000 after a 15% discount?
        ↓
🤖 Agent calls `calculate_discount`
        ↓
⚙️ Python calculates the result
        ↓
💬 Agent returns the final price
```

---

## ⚖️ Built-in Tools vs Custom Tools

| Feature               | Built-in Tool 🧰                    | Custom Tool 🛠️                         |
| --------------------- | ----------------------------------- | --------------------------------------- |
| Who creates it?       | Framework, provider, or service     | We create it                            |
| Main purpose          | Common tasks                        | Application-specific tasks              |
| Code required from us | Usually less                        | We write the function                   |
| Example               | Search, file access, MCP connection | Attendance calculation, employee lookup |
| Best for              | Existing reusable capability        | Unique business logic                   |

---

## 🍽️ Simple Analogy

Think of an agent application like a restaurant.

```text
🧰 Built-in tool
= A ready-made coffee machine

🛠️ Custom tool
= Your restaurant’s special recipe
```

The coffee machine is already built and ready to use.
Your special recipe is something you create for your own restaurant.

---

## 🧪 Example: Custom College Tool

A general search tool can find public information, but it cannot know internal college attendance records.

For that, we create a custom tool:

```python
def get_student_attendance(student_id: str) -> dict:
    """Returns attendance percentage and status for a student ID."""
    return {
        "student_id": student_id,
        "attendance_percentage": 82.5,
        "status": "Eligible",
    }
```

If the user asks:

> Show attendance for student SNU123.

The agent can call:

```python
get_student_attendance(student_id="SNU123")
```

The tool returns:

```python
{
    "student_id": "SNU123",
    "attendance_percentage": 82.5,
    "status": "Eligible",
}
```

---

## 🧠 When to Use Each Type

Use a **built-in tool** when:

* The capability already exists
* It is a common task
* It is well tested
* You do not need special business logic

Use a **custom tool** when:

* Your application has unique rules
* You need your own database logic
* You need a special calculation
* You need to validate your own data
* No ready-made tool matches your requirement

```text
🧰 Built-in tools give broad capabilities.

🛠️ Custom tools give an application its unique abilities.
```

---

## 🔐 Tool Safety: Least Privilege

Only give an agent the tools it truly needs.

```text
❌ Bad:
Give a calculator agent permission to delete files.

✅ Better:
Give a calculator agent only calculator tools.
```

This is called the **principle of least privilege**.

```text
🔐 Give the agent the smallest set of permissions needed
to complete its job.
```

---

# 📤 Tool Return Types & Structured Outputs

After a tool performs an action, it sends the result back to the agent.

```text
👤 User asks a question
        ↓
🤖 Agent calls a tool
        ↓
🛠️ Tool performs work
        ↓
📤 Tool returns data
        ↓
🤖 Agent reads the result
        ↓
💬 Agent gives the final answer
```

The value sent back by a tool is called its **return value**.

---

## 🔤 What is a Return Type?

A **return type** tells us what kind of value a function sends back.

```python
def add_numbers(first_number: float, second_number: float) -> float:
    """Adds two numbers and returns the result."""
    return first_number + second_number
```

```text
-> float
→ This tool returns a number.
```

Example:

```python
answer = add_numbers(10, 20)
print(answer)
```

Output:

```text
30
```

---

## 🧩 Common Return Types

| Return type | Example             | Use case                 |
| ----------- | ------------------- | ------------------------ |
| `str`       | `"Student found"`   | Text message             |
| `int`       | `25`                | Whole number             |
| `float`     | `82.5`              | Decimal number           |
| `bool`      | `True`              | Yes/no result            |
| `None`      | `None`              | No useful value returned |
| `dict`      | `{"name": "Rahul"}` | Structured information   |
| `list`      | `["Python", "ADK"]` | Multiple values          |

---

## 🧪 Tool Returning Text

```python
def get_greeting(name: str) -> str:
    """Creates a greeting message for the given name."""
    return f"Hello, {name}!"
```

Example result:

```text
Hello, Rahul!
```

---

## 🧪 Tool Returning a Number

```python
def calculate_total_price(price: float, quantity: int) -> float:
    """Calculates the total price for a product quantity."""
    return price * quantity
```

Example:

```python
calculate_total_price(price=499.5, quantity=2)
```

Output:

```text
999.0
```

---

## 📦 What is a Structured Output?

A **structured output** returns information in an organized format instead of one long sentence.

The most common structured output in Python is a **dictionary**.

```python
student = {
    "name": "Rahul",
    "attendance": 82.5,
    "eligible": True,
}
```

```text
"name"       → Rahul
"attendance" → 82.5
"eligible"   → True
```

This is easier for an agent to understand and use than one unstructured sentence.

---

## 🧪 Example: Student Attendance Tool

```python
def get_student_attendance(student_id: str) -> dict:
    """Returns attendance details for a student ID."""
    return {
        "student_id": student_id,
        "attendance_percentage": 82.5,
        "status": "Eligible",
    }
```

Example call:

```python
get_student_attendance(student_id="SNU123")
```

Output:

```python
{
    "student_id": "SNU123",
    "attendance_percentage": 82.5,
    "status": "Eligible",
}
```

The agent can then respond:

> Student SNU123 has 82.5% attendance and is eligible.

---

## 🧠 Why Structured Outputs Are Useful

```text
📦 Structured output
   → Uses clear labels
   → Is easier for the agent to read
   → Is easier to validate
   → Can be passed to another tool
```

For example, this is less useful:

```text
Rahul has 82.5 attendance and is eligible.
```

This is more useful:

```python
{
    "student_name": "Rahul",
    "attendance_percentage": 82.5,
    "eligible": True,
}
```

---

## `dict` vs `str`

### Returning only a sentence

```python
def get_student_result(student_id: str) -> str:
    """Returns the result for a student."""
    return "Rahul scored 88 and passed."
```

This is acceptable for a simple response, but it is harder to reuse the score later.

### Returning structured data

```python
def get_student_result(student_id: str) -> dict:
    """Returns the score and pass status for a student."""
    return {
        "student_id": student_id,
        "score": 88,
        "passed": True,
    }
```

Now the agent can clearly read:

```text
score  → 88
passed → True
```

---

## 📋 Returning a List

Use a list when a tool needs to return multiple items.

```python
def get_available_courses() -> list[str]:
    """Returns a list of available ADK learning courses."""
    return [
        "Google ADK Foundations",
        "Tools and Custom Functions",
        "Multi-Agent Systems",
    ]
```

---

## ✅ Returning Success or Failure Clearly

A useful tool should make it clear whether it succeeded.

```python
def create_task(title: str) -> dict:
    """Creates a task and returns whether the operation succeeded."""
    if not title.strip():
        return {
            "success": False,
            "message": "Task title cannot be empty.",
        }

    return {
        "success": True,
        "task": {
            "title": title,
            "completed": False,
        },
    }
```

Valid input:

```python
create_task(title="Finish Day 2 notes")
```

Output:

```python
{
    "success": True,
    "task": {
        "title": "Finish Day 2 notes",
        "completed": False,
    },
}
```

Invalid input:

```python
create_task(title="")
```

Output:

```python
{
    "success": False,
    "message": "Task title cannot be empty.",
}
```

---

## 🧱 A Clean Return Pattern

For many tools, this structure is useful:

```python
{
    "success": True,
    "data": {
        "key": "value",
    },
    "message": "Optional explanation",
}
```

Example:

```python
def get_employee_details(employee_id: str) -> dict:
    """Returns employee details for an employee ID."""
    return {
        "success": True,
        "data": {
            "employee_id": employee_id,
            "name": "Rahul",
            "department": "AI and Data Science",
        },
        "message": "Employee details found.",
    }
```

When an error happens, keep the same structure:

```python
{
    "success": False,
    "data": None,
    "message": "Employee not found.",
}
```

---

## ⚠️ Important Rule

A tool should return **clean and predictable data**.

```text
❌ Bad:
Sometimes return a number, sometimes a sentence,
and sometimes nothing.

✅ Better:
Always return the same structure.
```

For example:

```python
{
    "success": True,
    "data": {...},
    "message": "..."
}
```
# ⚠️ Error Handling & Tool Retries

Tools can fail because of invalid input, unavailable APIs, missing database records, or network problems.

A well-designed tool should not crash the whole agent program. It should return a clear result that helps the agent explain what happened.

```text
👤 User request
        ↓
🤖 Agent calls a tool
        ↓
🛠️ Tool succeeds OR fails
        ↓
📤 Tool returns a clear result
        ↓
💬 Agent explains the outcome
```

---

## 🧩 What is Error Handling?

**Error handling** means detecting a problem and returning a useful response instead of letting the program stop unexpectedly.

### ❌ Without Error Handling

```python
def divide_numbers(first_number: float, second_number: float) -> float:
    """Divides the first number by the second number."""
    return first_number / second_number
```

If the user asks to divide `10` by `0`, Python raises:

```text
ZeroDivisionError: float division by zero
```

The tool fails and the user may see a technical error.

---

## ✅ With Error Handling

```python
def divide_numbers(first_number: float, second_number: float) -> dict:
    """Divides two numbers and returns a clear error if the divisor is zero."""
    if second_number == 0:
        return {
            "success": False,
            "data": None,
            "message": "Division by zero is not allowed.",
        }

    return {
        "success": True,
        "data": {
            "result": first_number / second_number,
        },
        "message": "Division completed successfully.",
    }
```

If the user asks to divide `10` by `0`, the tool returns:

```python
{
    "success": False,
    "data": None,
    "message": "Division by zero is not allowed.",
}
```

The agent can then give a clear response such as:

> I cannot divide by zero. Please provide a non-zero divisor.

---

## 🛡️ Validate Input Before Doing the Work

Use input validation when you already know which values are invalid.

```python
def calculate_discount(
    original_price: float,
    discount_percentage: float,
) -> dict:
    """Calculates a discounted price and validates the input values."""
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
```

Examples of invalid input:

```text
❌ Original price = -500
❌ Discount percentage = 150
```

Instead of failing, the tool returns a useful message.

---

## 🧪 `try` and `except`

Use `try` and `except` when something may fail unexpectedly while the tool is running.

```python
def get_student_name(student_id: str) -> dict:
    """Returns a student's name for a valid student ID."""
    try:
        students = {
            "SNU101": "Rahul",
            "SNU102": "Raghavendra",
            "SNU103": "Raghav",
            "SNU104": "Raghu",
            "SNU105": "Raghavan",
        }

        student_name = students[student_id]

        return {
            "success": True,
            "data": {
                "student_id": student_id,
                "student_name": student_name,
            },
            "message": "Student found.",
        }

    except KeyError:
        return {
            "success": False,
            "data": None,
            "message": f"No student found with ID {student_id}.",
        }
```

### How `try` and `except` work

```python
try:
    student_name = students[student_id]
```

Python tries to find the given student ID in the dictionary.

```python
except KeyError:
```

If the student ID does not exist, Python catches the `KeyError` and returns a clean error response instead of crashing.

```text
🧪 `try`
→ Attempt code that may fail.

🛡️ `except`
→ Handle the error safely if it fails.
```

---

## 🔁 What is a Tool Retry?

A **retry** means trying an operation again after a temporary failure.

Retries are useful for:

* 🌐 Temporary network problems
* ⏳ API timeouts
* 🔌 External services that are temporarily unavailable
* 🗄️ Short database connection failures

```text
🛠️ Tool tries an API call
        ↓
❌ Temporary failure
        ↓
🔁 Wait briefly
        ↓
🛠️ Try again
        ↓
✅ Success OR return a final error
```

---

## ⚠️ When Should a Tool Retry?

| Problem                  |      Retry? | Reason                                      |
| ------------------------ | ----------: | ------------------------------------------- |
| Division by zero         |        ❌ No | The user input is invalid                   |
| Invalid student ID       |        ❌ No | Retrying gives the same result              |
| Temporary API timeout    |       ✅ Yes | The service may recover                     |
| Network connection error | ✅ Sometimes | The problem may be temporary                |
| Missing required input   |        ❌ No | The agent should ask the user for the input |

```text
🔁 Retry temporary system failures.

🛑 Do not retry invalid user input.
```

---

## 🧪 Simple Retry Example

```python
import time


def fetch_weather(city: str) -> dict:
    """Fetches weather data and retries up to three times for temporary failures."""
    for attempt in range(1, 4):
        try:
            if attempt < 3:
                raise ConnectionError("Temporary connection problem.")

            return {
                "success": True,
                "data": {
                    "city": city,
                    "temperature_celsius": 31,
                    "condition": "Partly cloudy",
                },
                "message": "Weather data fetched successfully.",
            }

        except ConnectionError:
            if attempt == 3:
                return {
                    "success": False,
                    "data": None,
                    "message": "Could not fetch weather data after 3 attempts.",
                }

            time.sleep(1)

    return {
        "success": False,
        "data": None,
        "message": "Unexpected error while fetching weather data.",
    }
```

This example simulates a temporary connection problem on the first two attempts and succeeds on the third attempt.

---

## 🔍 Important Retry Syntax

```python
for attempt in range(1, 4):
```

This creates three attempts:

```text
Attempt 1
Attempt 2
Attempt 3
```

```python
time.sleep(1)
```

This pauses the program for one second before trying again.

```python
raise ConnectionError("Temporary connection problem.")
```

This creates an example connection error for testing. In a real application, an API request or database call may naturally raise this kind of error.

---

## 📦 Keep Error Responses Predictable

Use the same response structure whether the tool succeeds or fails.

### Success

```python
{
    "success": True,
    "data": {
        "result": 42,
    },
    "message": "Calculation completed.",
}
```

### Failure

```python
{
    "success": False,
    "data": None,
    "message": "Division by zero is not allowed.",
}
```

```text
success = True
→ The agent can use the value in `data`.

success = False
→ The agent should explain the value in `message`.
```
# ⚡ Long-Running Tools & Async Patterns

Some tools finish immediately, such as addition or discount calculation.

```text
➕ 10 + 20
→ Result comes instantly
```

Other tools can take time because they depend on external systems.

```text
🌐 Calling a weather API
🗃️ Querying a database
📁 Reading a large file
📤 Uploading a document
🔎 Searching the web
```

These are called **long-running tools**.

---

## 🐢 What is a Long-Running Tool?

A **long-running tool** is a tool that may take noticeable time to complete.

Example flow:

```text
👤 User: Get the weather in Chennai.
        ↓
🤖 Agent calls the weather tool
        ↓
🌐 Tool sends a request to a weather API
        ↓
⏳ Tool waits for the API response
        ↓
📤 Tool returns weather data
```

The waiting time is why asynchronous programming is useful.

---

## 🚫 Problem with Normal Synchronous Code

```python
import time


def download_report() -> str:
    """Downloads a report and returns a completion message."""
    time.sleep(5)
    return "Report downloaded."
```

```python
time.sleep(5)
```

means:

```text
⏳ Stop the whole program for five seconds.
```

While this function is running, Python cannot do other work in the same thread.

```text
🚫 Program waits
🚫 Chatbot may feel frozen
🚫 Other requests cannot be handled in that thread
```

---

## ⚡ What is Asynchronous Programming?

**Asynchronous programming** lets Python wait for slow work without blocking the whole application.

```text
⏳ Waiting for an API response
        ↓
⚡ Python can handle other async work while waiting
```

The main keywords are:

```text
async def
→ Creates an asynchronous function.

await
→ Waits for an async task without blocking the whole application.
```

---

## 🧪 Basic Async Example

```python
import asyncio


async def download_report() -> str:
    """Simulates downloading a report."""
    await asyncio.sleep(5)
    return "Report downloaded."


async def main():
    result = await download_report()
    print(result)


asyncio.run(main())
```

After about five seconds, the output is:

```text
Report downloaded.
```

---

## 🔍 `time.sleep()` vs `asyncio.sleep()`

| Code                     | What happens                                               |
| ------------------------ | ---------------------------------------------------------- |
| `time.sleep(5)`          | Blocks the program for five seconds                        |
| `await asyncio.sleep(5)` | Lets the event loop handle other async tasks while waiting |

```text
🚫 `time.sleep()`
→ Everyone waits.

⚡ `await asyncio.sleep()`
→ This task waits, but Python can work on other async tasks.
```

---

## 🛠️ Async Function Tool Example

A tool itself can be asynchronous.

```python
import asyncio


async def fetch_weather(city: str) -> dict:
    """Fetches weather information for a city."""
    await asyncio.sleep(2)

    return {
        "success": True,
        "data": {
            "city": city,
            "temperature_celsius": 31,
            "condition": "Partly cloudy",
        },
        "message": "Weather fetched successfully.",
    }
```

```text
👤 User: What is the weather in Chennai?
        ↓
🤖 Agent chooses `fetch_weather`
        ↓
🌐 Tool waits for an external service
        ↓
📤 Tool returns structured weather data
        ↓
💬 Agent explains the weather
```

In this example, `await asyncio.sleep(2)` only simulates a slow API request. A real tool would use an async HTTP client or async database library.

---

## 🧠 `async def`

```python
async def fetch_weather(city: str) -> dict:
```

This creates an asynchronous function.

```text
def
→ Normal function

async def
→ Function that can use `await`
```

An async function is normally called using `await`.

```python
weather = await fetch_weather("Chennai")
```

---

## 🧠 `await`

```python
await asyncio.sleep(2)
```

Read it as:

```text
“Wait for this async task to finish,
but do not block the entire application while waiting.”
```

`await` can only be used inside an `async def` function.

### ❌ Invalid

```python
def main():
    result = await fetch_weather("Chennai")
```

### ✅ Valid

```python
async def main():
    result = await fetch_weather("Chennai")
```

---

## 🔄 Multiple Slow Tasks at the Same Time

Async is especially useful when multiple independent tasks are slow.

```python
import asyncio


async def fetch_weather(city: str) -> str:
    """Simulates fetching weather information."""
    await asyncio.sleep(2)
    return f"Weather data for {city} is ready."


async def fetch_news(topic: str) -> str:
    """Simulates fetching news information."""
    await asyncio.sleep(2)
    return f"News about {topic} is ready."


async def main():
    weather_result, news_result = await asyncio.gather(
        fetch_weather("Chennai"),
        fetch_news("Google ADK"),
    )

    print(weather_result)
    print(news_result)


asyncio.run(main())
```

Without async, two two-second tasks may take about four seconds when run one after another.

With `asyncio.gather(...)`, both tasks wait at the same time, so they take about two seconds total.

```text
Sequential:
Weather ⏳⏳
Then news ⏳⏳
Total ≈ 4 seconds

Concurrent async:
Weather ⏳⏳
News    ⏳⏳
Total ≈ 2 seconds
```

---

## ⚠️ Async Does Not Make CPU-Heavy Work Faster

Async is best for **I/O-bound tasks**, where the program spends time waiting.

```text
✅ API calls
✅ Database queries
✅ File uploads and downloads
✅ Network requests
```

It is not the main solution for CPU-heavy work.

```text
❌ Training an ML model
❌ Processing a huge video
❌ Large mathematical computations
```

CPU-heavy tasks may need separate processes, worker queues, or cloud jobs.

---

## 🧪 Async in ADK

In the Day 1 agent, this code was asynchronous:

```python
async for event in runner.run_async(
    user_id=session.user_id,
    session_id=session.id,
    new_message=user_message,
):
```

The agent may need time to:

```text
🧠 Call Gemini
🛠️ Call tools
💾 Read or update session data
📤 Receive events
```

`async for` receives events one by one as they become available.

---

# 🔍 Callbacks for Observability & Guardrails

Callbacks run custom code at important points in an agent workflow.

```text
👤 User sends a message
        ↓
🔔 Before-agent callback
        ↓
🤖 Agent thinks and decides
        ↓
🔔 Before-tool callback
        ↓
🛠️ Tool runs
        ↓
🔔 After-tool callback
        ↓
🤖 Agent prepares final response
        ↓
🔔 After-agent callback
        ↓
💬 Response sent to user
```

Callbacks act like checkpoints around the agent and its tools.

They are useful for:

```text
👀 Observability
→ See what the agent and tools are doing.

🛡️ Guardrails
→ Check, restrict, or block unsafe actions.
```

---

## 👀 Observability

**Observability** means being able to inspect what happens inside an application.

For an agent, this can include:

* Which tool the agent selected
* Input sent to a tool
* Whether the tool succeeded or failed
* How long a tool took
* The final response produced by the agent

```text
Without observability:
🤖 Agent works internally
❓ We do not know what happened

With observability:
🤖 Agent works internally
👀 We can inspect important steps
```

---

## 🧪 Logging a Tool Call

```python
def log_tool_call(tool_name: str, tool_input: dict) -> None:
    """Prints information about a tool call."""
    print(f"🔍 Tool selected: {tool_name}")
    print(f"📥 Tool input: {tool_input}")
```

Example:

```python
log_tool_call(
    tool_name="calculate_discount",
    tool_input={
        "original_price": 2000,
        "discount_percentage": 15,
    },
)
```

Output:

```text
🔍 Tool selected: calculate_discount
📥 Tool input: {'original_price': 2000, 'discount_percentage': 15}
```

This kind of logging helps debug an agent.

---

## 🛡️ Guardrails

**Guardrails** are rules that prevent an agent from doing something unsafe, invalid, or unwanted.

```text
🛡️ Guardrail
= A safety check before an action is allowed
```

Example:

```text
👤 User: Transfer ₹5,00,000
        ↓
🛡️ Guardrail checks the amount
        ↓
❌ Amount exceeds the allowed limit
        ↓
🚫 Tool call is blocked
```

Guardrails become especially important for agents that access files, databases, payments, or emails.

---

## 🧩 Callback Positions

| Callback     | Runs when                            | Useful for                                               |
| ------------ | ------------------------------------ | -------------------------------------------------------- |
| Before agent | Before the agent processes a request | Validate user input, load context, block unsafe requests |
| After agent  | After the agent finishes             | Log final response, measure execution time               |
| Before tool  | Before a tool runs                   | Validate inputs, check permissions, block risky actions  |
| After tool   | After a tool runs                    | Log results, detect failures, format data                |

```text
🤖 Before agent
→ “Should the agent process this request?”

🛠️ Before tool
→ “Is this tool call allowed?”

🛠️ After tool
→ “Did the tool succeed?”

🤖 After agent
→ “What final response was produced?”
```

---

## 🧪 Example Guardrail: Transfer Amount

```python
def validate_transfer_amount(amount: float) -> dict:
    """Checks whether a transfer amount is within the allowed limit."""
    maximum_allowed_amount = 10000

    if amount <= 0:
        return {
            "allowed": False,
            "message": "Transfer amount must be greater than zero.",
        }

    if amount > maximum_allowed_amount:
        return {
            "allowed": False,
            "message": "Transfer amount exceeds the allowed limit.",
        }

    return {
        "allowed": True,
        "message": "Transfer amount is allowed.",
    }
```

Example:

```python
result = validate_transfer_amount(25000)
print(result)
```

Output:

```text
{
    'allowed': False,
    'message': 'Transfer amount exceeds the allowed limit.'
}
```

A real before-tool callback can run this check before a money-transfer tool is allowed to execute.

---

## 🧪 Example Guardrail: Protected Files

```python
def check_file_deletion(file_name: str) -> dict:
    """Checks whether a file is allowed to be deleted."""
    protected_files = [
        ".env",
        "important_data.csv",
        "production_database.db",
    ]

    if file_name in protected_files:
        return {
            "allowed": False,
            "message": f"Deletion blocked: {file_name} is protected.",
        }

    return {
        "allowed": True,
        "message": "Deletion is allowed.",
    }
```

```text
👤 User: Delete .env
        ↓
🛡️ Before-tool check runs
        ↓
❌ `.env` is protected
        ↓
🚫 The delete tool is not allowed to run
```

---

## 🧪 Example: Before-Agent Validation

```python
def validate_user_message(user_message: str) -> dict:
    """Checks whether a user message is within the allowed length."""
    maximum_length = 500

    if len(user_message) > maximum_length:
        return {
            "allowed": False,
            "message": "Your message is too long. Please keep it under 500 characters.",
        }

    return {
        "allowed": True,
        "message": "User message is allowed.",
    }
```

```text
👤 User sends a message
        ↓
🛡️ Check message length
        ↓
✅ Continue to agent
or
❌ Stop before the agent runs
```

---

## 🧪 Example: After-Tool Logging

```python
def log_tool_result(tool_name: str, tool_result: dict) -> None:
    """Prints a tool result for debugging."""
    print(f"🛠️ Tool completed: {tool_name}")
    print(f"📤 Tool result: {tool_result}")
```

Example:

```python
log_tool_result(
    tool_name="get_student_attendance",
    tool_result={
        "success": True,
        "data": {
            "student_id": "SNU101",
            "attendance_percentage": 82.5,
        },
        "message": "Attendance found.",
    },
)
```

Output:

```text
🛠️ Tool completed: get_student_attendance
📤 Tool result: {'success': True, 'data': {'student_id': 'SNU101', 'attendance_percentage': 82.5}, 'message': 'Attendance found.'}
```

---

## 🔄 Callback Flow Example

```text
👤 User: Delete important_data.csv
        ↓
🔔 Before-agent callback
   → Validate the request
        ↓
🤖 Agent decides to use delete_file
        ↓
🔔 Before-tool callback
   → Check whether the file is protected
        ↓
🚫 Block the action
        ↓
🔔 After-agent callback
   → Log that the request was blocked
        ↓
💬 Agent: I cannot delete that protected file.
```

---

## ⚠️ Callback Logic vs ADK Callback Syntax

The examples above teach the logic of callbacks.

The exact callback parameters and return values depend on the ADK callback type and installed ADK version. When implementing a real callback, use the signatures in the official documentation for that version.

```text
🧠 Callback logic
→ What should be checked or logged?

⚙️ ADK callback syntax
→ How ADK passes context into that logic.
```
