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
