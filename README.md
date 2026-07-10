# 🤖 Google ADK Learning Journey

A hands-on repository for learning **Google Agent Development Kit (ADK)** through Python examples, notes, tools, MCP integrations, multi-agent systems, and Agentic RAG.

## 🎯 What This Repository Covers

* 🤖 ADK agents, sessions, runners, and prompts
* 🛠️ Built-in tools and custom Python functions
* 🧭 Sequential, parallel, loop, and coordinator agents
* 🔌 Model Context Protocol (MCP)
* 🌐 Chrome DevTools MCP and GitHub MCP
* 📚 RAG with LangChain, HuggingFace embeddings, and Qdrant
* 🧭 Query routing and multi-hop retrieval
* 🛡️ Grounded answers, citations, and guardrails
* 🚀 Multi-agent Agentic RAG capstone

## 📁 Project Structure

```text
google-adk-learning/
│
├── Day-01-ADK-Foundations/
├── Day-02-Tools-Custom-Functions/
├── Day-03-Agent-Orchestration/
├── Day-04-MCP-in-Agents/
├── Day-05-Agentic-RAG-Capstone/
├── .env.example
├── .gitignore
└── README.md
```

## 📅 Day-wise Summary

### 🟢 Day 1 — ADK Foundations

Learned how an ADK agent works using:

```text
User message → LlmAgent → Gemini model → Response
```

Covered agent instructions, sessions, runners, and basic agent execution.

### 🛠️ Day 2 — Tools and Custom Functions

Learned how agents call Python functions as tools.

```text
User request → Agent chooses tool → Python function runs → Agent responds
```

Covered built-in tools, custom tools, type hints, docstrings, function tools, and guardrails.

### 🧭 Day 3 — Agent Orchestration

Learned how multiple agents can work together.

```text
Sequential Agent → tasks run step by step
Parallel Agent   → tasks run together
Loop Agent       → task repeats until complete
Coordinator      → routes requests to specialist agents
```

### 🔌 Day 4 — MCP in Agents

Learned how agents connect to external systems through MCP.

```text
ADK Agent → MCPToolset → MCP Server → External tool or service
```

Built custom MCP servers and explored project tools, Chrome DevTools MCP, GitHub MCP, `.env` secrets, read-only permissions, and safe tool access.

### 📚 Day 5 — Agentic RAG Capstone

Built RAG systems using:

```text
PDF → PyPDFLoader → Text Chunks → Embeddings → Qdrant → Retrieved Answer
```

Covered retrieval tools, query routing, multi-hop retrieval, grounding, citations, and a multi-agent capstone.

```text
Coordinator Agent
├── PDF RAG Specialist
└── Chrome MCP Specialist
```

The capstone uses an approved public PDF, Qdrant vector search, grounded PDF page citations, and Chrome MCP for source inspection.

## ⚙️ Main Technologies

| Technology             | Purpose                     |
| ---------------------- | --------------------------- |
| Google ADK             | AI agents and orchestration |
| Gemini                 | Language model              |
| Python                 | Main language               |
| MCP                    | External tool integration   |
| LangChain              | PDF loading and chunking    |
| HuggingFace Embeddings | Text-to-vector conversion   |
| Qdrant                 | Vector database             |
| Chrome DevTools MCP    | Browser inspection          |
| GitHub MCP             | GitHub access               |
| Python Dotenv          | Environment variables       |

## 🧰 Setup

```powershell
git clone https://github.com/rahulraghavendrar/google-adk-learning.git
cd google-adk-learning

python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the main dependencies:

```powershell
pip install google-adk python-dotenv mcp
pip install langchain-community langchain-text-splitters
pip install langchain-huggingface langchain-qdrant
pip install qdrant-client sentence-transformers pypdf requests
```

Create a root `.env` file:

```env
GOOGLE_API_KEY=your_google_ai_studio_api_key
GITHUB_PERSONAL_ACCESS_TOKEN=your_optional_github_token
```

## 🔐 Security

* Keep API keys and tokens only in `.env`
* Never commit `.env`
* Use read-only GitHub tokens when possible
* Restrict MCP tools to only required actions
* Use approved public PDF URLs for the RAG capstone

Check `.env` is ignored:

```powershell
git check-ignore .env
```

## 👤 Author

**Rahul Raghavendra**
GitHub: https://github.com/rahulraghavendrar
