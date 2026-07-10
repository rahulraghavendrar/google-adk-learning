# 🔌 Day 4 — Using MCP in Agents

## 🎯 Goal

Learn how a Google ADK agent can connect to tools and data outside its own Python file using **MCP (Model Context Protocol)**.

---

# 🧩 What is MCP?

**MCP** stands for **Model Context Protocol**.

It is a standard way for AI agents to connect with external tools, data sources, and services.

```text
🤖 AI Agent
   ↓
🔌 MCP
   ↓
🛠️ Tools / 📁 Files / 🗃️ Databases / 🌐 APIs
```

Without MCP, every external integration may need custom code.

```text
❌ Without MCP

Agent → separate custom code for files
Agent → separate custom code for GitHub
Agent → separate custom code for databases
```

With MCP, external systems can expose their capabilities in a common format.

```text
✅ With MCP

Agent → MCP Client → MCP Server → External system
```

MCP does not automatically give an agent unlimited access. The MCP server decides which tools are available, and the developer decides which server the agent can connect to.

---

# 🏗️ MCP Architecture

MCP has three important parts.

```text
🤖 MCP Client
   ↓
🚚 Transport
   ↓
🖥️ MCP Server
```

## 🖥️ MCP Server

An MCP server is a separate program that exposes useful capabilities.

It can expose:

```text
🛠️ Tools
📄 Resources
💬 Prompt templates
```

For this Day 4 example, the server exposes student-information tools:

```text
get_student_attendance(student_id)
get_internal_marks(student_id)
```

The server acts as a controlled gateway.

```text
🖥️ MCP Server
   ↓
Allowed:
✅ Get attendance
✅ Get internal marks

Not allowed:
❌ Read every file on the computer
❌ Delete data
```

## 🤖 MCP Client

The MCP client connects to the MCP server, discovers available tools, and sends tool calls.

In ADK, `MCPToolset` helps perform the client-side work.

```text
🤖 ADK Agent
   ↓
🔌 MCPToolset
   ↓
🤖 MCP Client connection
   ↓
🖥️ MCP Server
```

## 🚚 Transport

A transport is the communication method between the MCP client and server.

| Transport  | Meaning                                      | Best use                       |
| ---------- | -------------------------------------------- | ------------------------------ |
| `stdio` 💻 | Standard input/output between local programs | Local development and learning |
| SSE 🌐     | Server-Sent Events over a network            | Remote streaming connections   |
| HTTP 🌍    | Normal web requests and responses            | Cloud or web-hosted servers    |

For this project, we use **`stdio`**.

```text
ADK Agent
   ↕
Local MCP Server
```

---

# 🔌 `MCPToolset` in ADK

`MCPToolset` connects an ADK agent to an MCP server and makes the server’s tools available to the agent.

```text
🤖 ADK Agent
   ↓
🔌 MCPToolset
   ↓
🖥️ MCP Server
   ↓
🛠️ MCP Tools
```

This is different from a normal Python tool.

```text
Day 2 normal tool:
Agent → Python function in the same program

Day 4 MCP tool:
Agent → MCPToolset → separate MCP server → Python function
```

A basic `MCPToolset` connection looks like this:

```python
mcp_toolset = MCPToolset(
    connection_params=StdioConnectionParams(
        command=sys.executable,
        args=[SERVER_FILE],
    )
)
```

`command=sys.executable` starts the MCP server using the same Python interpreter and virtual environment currently running the ADK agent.

`args=[SERVER_FILE]` passes the MCP server file to Python.

Conceptually, ADK runs:

```text
python student_mcp_server.py
```

The toolset is then added to the agent:

```python
tools=[mcp_toolset]
```

This gives the agent access to every tool exposed by the connected MCP server.

---

# 🖥️ Student MCP Server

The file:

```text
student_mcp_server.py
```

runs separately from the ADK agent and exposes student-information tools.

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Student Information Server")
```

`FastMCP` creates the MCP server.

A normal Python function becomes an MCP tool using:

```python
@mcp.tool()
def get_student_attendance(student_id: str) -> dict:
```

`@mcp.tool()` is a decorator. It tells MCP:

```text
“Expose this function so an MCP client can call it.”
```

The server starts with:

```python
mcp.run(transport="stdio")
```

For `stdio`, do not use normal `print()` statements inside the MCP server because standard output is used for MCP communication.

---

# 🤖 MCP Student Agent

The file:

```text
mcp_student_agent.py
```

contains the ADK agent.

It does not contain the student tools directly. Instead, it connects to `student_mcp_server.py` through `MCPToolset`.

```text
mcp_student_agent.py
        ↓
MCPToolset
        ↓
student_mcp_server.py
        ↓
get_student_attendance()
get_internal_marks()
```

The agent receives user questions such as:

```text
What is the attendance for SNU101?
Show internal marks for SNU102.
```

It chooses the correct MCP tool, sends the request to the MCP server, receives the result, and gives a clear final response.

---

# 🔄 Complete Request Flow

```text
👤 User:
What is the attendance for SNU101?

        ↓

🤖 ADK Agent:
Recognizes that attendance information is needed.

        ↓

🔌 MCPToolset:
Connects to the local MCP server.

        ↓

🖥️ MCP Server:
Runs get_student_attendance("SNU101").

        ↓

📦 Tool Result:
Rahul has 82.5% attendance.

        ↓

🤖 ADK Agent:
Returns the answer to the user.
```

---

# 📁 Day 4 File Structure

```text
Day-04-MCP-in-Agents/
│
├── student_mcp_server.py
├── mcp_student_agent.py
└── notes.md
```

`student_mcp_server.py` exposes tools.

`mcp_student_agent.py` connects an ADK agent to those tools through `MCPToolset`.

`notes.md` contains the Day 4 learning notes.
🔌 MCPToolset in ADK

MCPToolset connects an ADK agent to an MCP server and makes the server’s tools available to the agent.

mcp_toolset = MCPToolset(
    connection_params=StdioConnectionParams(
        command=sys.executable,
        args=[SERVER_FILE],
    )
)
command=sys.executable
→ Uses the same Python interpreter and virtual environment.

args=[SERVER_FILE]
→ Starts the MCP server file.

tools=[mcp_toolset]
→ Gives the agent access to tools exposed by that server.

This differs from a normal Python tool:

Normal tool:
Agent → Python function in the same program

MCP tool:
Agent → MCPToolset → separate MCP server → Python function
🖥️ Custom MCP Servers

A custom MCP server is a separate Python file that exposes functions as MCP tools.

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My Server")

A function becomes an MCP tool using the @mcp.tool() decorator.

@mcp.tool()
def get_student_attendance(student_id: str) -> dict:
    """Get attendance information for a student."""

The server starts with:

mcp.run(transport="stdio")

For stdio servers, avoid normal print() statements because standard output is reserved for MCP communication. Return values from tools instead.

Student MCP Server

student_mcp_server.py exposes:

get_student_attendance(student_id)
get_internal_marks(student_id)

mcp_student_agent.py connects to that server using MCPToolset.

User asks about attendance
        ↓
ADK agent selects an MCP tool
        ↓
Student MCP server runs the function
        ↓
Agent receives the result and answers
Project MCP Server

project_mcp_server.py exposes project-related tools:

get_project_status(project_name)
calculate_days_remaining(total_days, completed_days)

project_mcp_agent.py connects to this server and uses its tools for project questions.

This shows that MCP tools can contain normal Python logic, but the logic is kept in a separate reusable server process.

🌐 Existing MCP Servers

Instead of building every server yourself, an agent can connect to existing MCP servers.

Examples:

📁 Filesystem MCP server
🐙 GitHub MCP server
🌐 Chrome DevTools MCP server
🗃️ Database MCP server
Chrome DevTools MCP

Chrome DevTools MCP allows an agent to interact with and inspect a Chrome browser.

It can be used to open public pages, inspect content, and summarize search results.

🤖 ADK Agent
   ↓
🔌 MCPToolset
   ↓
🌐 Chrome DevTools MCP
   ↓
🖥️ Chrome browser

It should be used carefully. Good learning use cases include public documentation pages and web searches. Avoid important logins, banking pages, purchases, and automatic form submissions.

GitHub MCP

GitHub MCP allows an agent to interact with GitHub through selected GitHub tools.

A read-only GitHub agent can inspect:

✅ Repositories
✅ Files
✅ Commits
✅ Issues
✅ Pull requests

It should not be allowed to create, edit, delete, merge, or comment unless those actions are specifically required and approved.

🔐 Credentials and Safe Scoping

Credentials prove that a program is allowed to access an external system.

Examples include API keys, GitHub Personal Access Tokens, and database usernames/passwords.

Never place secrets directly inside Python files.

# ❌ Unsafe
TOKEN = "secret_value"

Use a .env file instead:

GOOGLE_API_KEY=your_gemini_key
GITHUB_PERSONAL_ACCESS_TOKEN=your_github_token

Read secrets in Python using:

import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")

The .env file must not be committed to Git.

git check-ignore .env

If Git prints .env, it is being ignored correctly.

Least Privilege

Least privilege means giving only the minimum access required.

✅ GitHub token with read-only access to one repository
❌ Token with full access to every repository

✅ Database user with SELECT permission
❌ Database admin user with DELETE and DROP permissions

✅ Browser access for public pages
❌ Browser access to sensitive logged-in accounts

For GitHub, use a fine-grained Personal Access Token with:

Repository access: Only selected repositories
Contents: Read-only
Issues: Read-only only if needed
Pull requests: Read-only only if needed
📁 Day 4 Files
Day-04-MCP-in-Agents/
│
├── student_mcp_server.py
├── mcp_student_agent.py
├── chrome_mcp_agent.py
├── github_mcp_agent.py
├── project_mcp_server.py
├── project_mcp_agent.py
└── notes.md

The server files expose tools. The agent files connect to those tools through MCPToolset.