# 📘 Day 1 — Google ADK Foundations & Single Agent

## 🎯 Goal

Understand the main concepts of **Google Agent Development Kit (ADK)** and build a basic **tool-using AI agent**.

---

# 🤖 What is Google ADK?

**Google ADK** stands for **Agent Development Kit**.

It is a framework from Google used to build **AI agents**.

An AI agent can:

* **Understand user requests**
* **Use an LLM such as Gemini**
* **Call Python functions or external tools**
* **Remember conversation information**
* **Complete multi-step tasks**

```text
💬 Chatbot = Mainly generates text

🤖 Agent = Generates text + decides actions + uses tools + remembers context
```

Example:

```text
👤 User: What is 125 × 48?

🤖 Agent:
1. Understands that calculation is needed
2. Calls a calculator tool
3. Gets the result
4. Returns the final answer
```

---

# 🧭 Google ADK vs Other Frameworks

| Framework      | Main purpose                                        | Best use case                            |
| -------------- | --------------------------------------------------- | ---------------------------------------- |
| **Google ADK** | Build AI agents with tools, sessions, and workflows | Tool-using and multi-agent systems       |
| **LangChain**  | Build LLM applications with reusable components     | RAG, prompts, document processing        |
| **LlamaIndex** | Connect LLMs to private data                        | Document search and knowledge assistants |
| **CrewAI**     | Build teams of role-based agents                    | Multi-agent collaboration prototypes     |

```text
🤖 ADK        → Build agents
🔗 LangChain  → Build LLM pipelines
📚 LlamaIndex → Connect LLMs to data
👥 CrewAI     → Build agent teams
```

For this learning plan, **Google ADK is the main framework**.

---

# 🧩 ADK Core Primitives

The main building blocks of ADK are:

```text
🧠 LLM          → The model that understands and reasons
🤖 Agent         → Decides what to do
🛠️ Tools         → Functions that perform actions
💾 Session       → Stores conversation history and state
🏃 Runner        → Executes the agent workflow
```

---

# 🤖 `Agent` and `LlmAgent`

## What is an Agent?

An **Agent** is the general concept or blueprint of an AI agent.

It can have:

* **A name**
* **Instructions**
* **Tools**
* **Sub-agents**
* **Workflow behavior**

```text
🏗️ Agent = General blueprint
```

## What is `LlmAgent`?

An **`LlmAgent`** is an agent powered by an LLM such as Gemini.

```text
Agent
  └── LlmAgent
        └── Uses an LLM to understand language, reason, call tools, and respond
```

Example:

```python
from google.adk.agents import LlmAgent

my_agent = LlmAgent(
    name="helpful_agent",
    model="gemini-2.0-flash",
    instruction="You are a helpful assistant. Answer clearly and simply."
)
```

| Code          | Meaning                         |
| ------------- | ------------------------------- |
| `LlmAgent`    | Creates an LLM-powered agent    |
| `name`        | Internal name of the agent      |
| `model`       | Model used as the agent's brain |
| `instruction` | Rules for agent behavior        |

---

# 🛠️ Tools

A **tool** is a Python function that an agent can call to perform an action.

Examples:

* Calculator
* Weather API
* Database query
* File reader
* Web search
* Email sender

```text
🧠 LLM alone → Can reason and generate text

🤖 Agent + Tools → Can reason, choose actions, and perform tasks
```

Example calculator tool:

```python
def add_numbers(first_number: float, second_number: float) -> float:
    """Adds two numbers and returns the result."""
    return first_number + second_number
```

## Important tool parts

| Part          | Meaning                                 |
| ------------- | --------------------------------------- |
| Function name | Tells the agent what the tool does      |
| Parameters    | Inputs required by the tool             |
| Type hints    | Explain expected input and output types |
| Docstring     | Explains the tool purpose               |
| Return value  | Sends the result back to the agent      |

Attach a tool to an agent:

```python
tools=[add_numbers]
```

```text
add_numbers    → Gives the function to the agent

add_numbers()  → Runs the function immediately
```

The agent should receive the function itself, so it can decide **when** to call it.

---

# 📋 Agent Instructions and System Prompts

The `instruction` field tells the agent how to behave.

It acts like the agent's **job description**.

A good instruction includes:

```text
🎭 Role
🎯 Goal
🛠️ Tool-use rules
🗣️ Response style
```

Example:

```python
instruction="""
You are a calculator assistant.

Rules:
- Use calculator tools for every arithmetic operation.
- Never calculate arithmetic manually.
- Keep answers short and clear.
- If the user asks something unrelated to arithmetic, politely say that you only help with calculations.
"""
```

```text
📋 instruction = system-level behavior rules for the agent
```

---

# 🔄 Tool Calling

**Tool calling** happens when an agent decides to use an approved function.

Example:

```text
👤 User: What is 15 × 8?
        ↓
🤖 Agent understands multiplication is needed
        ↓
🛠️ Agent calls multiply_numbers(15, 8)
        ↓
⚙️ Tool returns 120
        ↓
💬 Agent: 15 × 8 = 120.
```

```text
🛠️ tools=[...]
   → Gives permission to use tools

📋 instruction
   → Guides when tools should be used

🧠 LLM
   → Decides whether to call a tool
```

---

# 💾 Sessions

A **session** stores information for one conversation.

```text
💾 Session = Conversation memory container
```

It can store:

* **Conversation history**
* **Session state**
* **User ID**
* **Session ID**

```text
💾 Session
 ├── 👤 user_id
 ├── 🆔 session_id
 ├── 💬 conversation history
 └── 🧠 state
```

## `user_id` vs `session_id`

| Name         | Meaning                     | Example                  |
| ------------ | --------------------------- | ------------------------ |
| `user_id`    | Identifies the user         | `"rahul"`                |
| `session_id` | Identifies one conversation | `"calculator_session_1"` |

One user can have multiple sessions.

```text
👤 Rahul
   ├── 💬 ADK learning session
   ├── 💬 Calculator test session
   └── 💬 Weather agent session
```

## Session state

Session state stores structured information as key-value pairs.

```python
state = {
    "user_name": "Rahul",
    "learning_topic": "Google ADK",
    "current_day": 1
}
```

```text
💬 Conversation history = Previous messages

🧠 Session state = Structured information such as
name, preferences, language, or current task
```

## Short-term vs persistent state

| Type                 | Meaning                                  |
| -------------------- | ---------------------------------------- |
| **Short-term state** | Exists only while the program is running |
| **Persistent state** | Remains saved after the program stops    |

For learning and testing, we use:

```python
InMemorySessionService
```

```text
▶️ Program starts → Session exists in memory
❌ Program stops → Session data disappears
```

---

# 🏃 Runner

A **Runner** executes the agent workflow.

```text
🤖 Agent     → Thinks and decides
💾 Session   → Remembers
🏃 Runner    → Connects everything and runs the workflow
```

Example:

```python
from google.adk.runners import Runner

runner = Runner(
    agent=calculator_agent,
    app_name="calculator_app",
    session_service=session_service,
)
```

The Runner handles this flow:

```text
👤 User sends a message
        ↓
🏃 Runner receives it
        ↓
💾 Runner loads the session
        ↓
🤖 Agent reads instructions and user message
        ↓
🛠️ Agent may call a tool
        ↓
💬 Agent creates a response
        ↓
💾 Runner saves the response in the session
```

---

# 🧠 Model Integration

An agent needs an LLM as its brain.

For Day 1, we use Gemini:

```python
model="gemini-2.0-flash"
```

```text
✨ Gemini native integration
   → Use Gemini directly with ADK

🔄 LiteLLM integration
   → Use models from other providers through a common interface
```

Examples of providers LiteLLM can support include OpenAI, Anthropic, and Gemini.

For our first ADK project, we use native Gemini integration because it is simpler.

## API key safety

The Gemini API key should be stored in a `.env` file:

```text
GOOGLE_API_KEY=PASTE_YOUR_GEMINI_API_KEY_HERE
```

Never write the key directly in Python code.

```text
❌ api_key = "AIza..."

✅ Store the key in `.env`
```

Add this to `.gitignore`:

```text
.env
venv/
__pycache__/
```

---

# ⚡ Async Programming in the Calculator Agent

ADK uses asynchronous programming because some tasks can take time:

```text
🌐 Gemini API calls
🛠️ Tool execution
💾 Session operations
📡 Agent responses
```

## Important async keywords

| Code                  | Meaning                                |
| --------------------- | -------------------------------------- |
| `import asyncio`      | Imports Python's async toolkit         |
| `async def main()`    | Creates an asynchronous function       |
| `await`               | Waits for an async operation to finish |
| `async for`           | Receives async events one by one       |
| `asyncio.run(main())` | Starts and runs the async program      |

Example:

```python
session = await session_service.create_session(...)
```

```text
⏳ Create the session
      ↓
✅ Wait until it is ready
      ↓
💾 Store it in the `session` variable
```

---

# 🔁 Chat Loop

```python
while True:
```

This keeps the calculator chatbot running continuously.

```python
user_input = input("You: ")
```

This reads the user's message.

```python
if user_input.lower() == "exit":
    break
```

This stops the chatbot when the user types `exit`, `Exit`, or `EXIT`.

```text
while True → Keep chatting
break      → Stop the chat loop
```

---

# 💬 Creating an ADK User Message

```python
user_message = types.Content(
    role="user",
    parts=[types.Part(text=user_input)],
)
```

This converts plain user text into the structured message format expected by ADK.

```text
"Add 10 and 20"

        ↓

{
  role: "user",
  parts: [
    { text: "Add 10 and 20" }
  ]
}
```

---

# 🔄 Running the Agent

```python
async for event in runner.run_async(
    user_id=session.user_id,
    session_id=session.id,
    new_message=user_message,
):
```

This means:

```text
Run the agent with this user message.
Receive each event produced by ADK one by one.
```

Possible events:

```text
1️⃣ Agent starts processing
2️⃣ Agent requests a tool call
3️⃣ Tool returns a result
4️⃣ Agent produces the final response
```

We only print the final response:

```python
if event.is_final_response():
```

Then print each text part:

```python
for part in event.content.parts:
    if part.text:
        print(f"🤖 Calculator Agent: {part.text}")
```

---

# 🚀 End of the Python File

```python
if __name__ == "__main__":
    asyncio.run(main())
```

This means:

> If this Python file is run directly, start the asynchronous `main()` function.

When you run:

```powershell
python calculator_agent.py
```

Python sets:

```python
__name__ = "__main__"
```

So this runs:

```python
asyncio.run(main())
```

Full flow:

```text
▶️ python calculator_agent.py
        ↓
⚡ asyncio.run(main())
        ↓
💾 Create session
        ↓
🏃 Create runner
        ↓
🔁 Start chat loop
        ↓
⌨️ User sends messages
        ↓
🤖 Agent uses tools and replies
        ↓
👋 User types exit
        ↓
🏁 Program ends
```

---

# 🧪 Lab 1 — Calculator Agent Components

Our calculator agent uses:

```text
🧠 Gemini model
      +
🤖 LlmAgent
      +
🛠️ Calculator tools
      +
💾 InMemorySessionService
      +
🏃 Runner
      =
✅ Working tool-using agent
```

Calculator tools:

```text
➕ add_numbers
➖ subtract_numbers
✖️ multiply_numbers
➗ divide_numbers
```

---

# ✅ Day 1 Key Takeaways

```text
🤖 Google ADK helps build AI agents.

🧠 LlmAgent uses an LLM such as Gemini.

🛠️ Tools are Python functions that agents can call.

📋 Instructions define agent behavior.

💾 Sessions store conversation history and state.

🏃 Runner executes the agent workflow.

✨ Gemini is the model used in our first agent.

⚡ async / await helps ADK handle operations that take time.

🔁 runner.run_async() runs the agent and returns events.

🚀 asyncio.run(main()) starts the async application.
```