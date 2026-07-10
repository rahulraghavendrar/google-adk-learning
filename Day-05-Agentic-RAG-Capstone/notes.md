# 🚀 Day 5 — RAG with Agents + Capstone

## 🎯 Goal

Combine **RAG**, **Google ADK agents**, and **MCP tools** to build an agent that can choose the right information source before answering.

```text
📚 RAG knowledge base
+ 🤖 ADK agent
+ 🔌 MCP tools
= 🧠 Agentic RAG system
```

# 🧩 Naive RAG vs Agentic RAG

A normal RAG pipeline follows one fixed path:

```text
User question
   ↓
Search vector database
   ↓
Retrieve relevant chunks
   ↓
LLM answers using those chunks
```

This works for document questions, but it may retrieve information even when retrieval is unnecessary.

**Agentic RAG** gives the agent control over retrieval.

```text
User question
   ↓
Agent decides:
“Do I need document retrieval?”
   ↓
Yes → Call retrieval tool
No  → Answer directly
```

For example:

```text
“What is MCP?”
→ Retrieve from the knowledge base.

“Hello”
→ Reply normally without retrieval.
```

Agentic RAG is more flexible because the agent can choose tools, route questions to different sources, retrieve again when needed, and avoid unnecessary searches.

# 🔎 Retrieval as an Agent Tool

In Agentic RAG, retrieval is written as a normal Python function and given to an ADK agent as a tool.

```python
def search_knowledge_base(question: str) -> dict:
    """Searches the knowledge base and returns relevant document chunks."""
```

```python
tools=[search_knowledge_base]
```

The agent can call this tool when a user asks about information stored in the vector database.

```text
ADK Agent
   ↓
search_knowledge_base(question)
   ↓
Qdrant vector database
   ↓
Relevant document chunks
   ↓
Agent answers using retrieved information
```

The agent is not forced to use the tool for every message. It uses it only when the question needs information from the documents.

# 🗃️ RAG Components Used

The Day 5 examples use the same RAG libraries used earlier.

```python
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
```

## `Document`

`Document` stores text that will be added to the knowledge base.

```python
Document(page_content="MCP stands for Model Context Protocol.")
```

A document can also contain metadata such as file name, page number, or source.

## `HuggingFaceEmbeddings`

```python
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
```

This model converts text into a 384-dimensional vector.

```text
Text
   ↓
Embedding model
   ↓
384-number vector
```

Similar text creates similar vectors.

## `QdrantClient`

```python
client = QdrantClient(":memory:")
```

This creates an in-memory Qdrant database. It is useful for learning because no separate Qdrant server is required.

```text
Program starts → vectors are created and stored
Program ends   → in-memory data disappears
```

## Qdrant Collection

```python
client.create_collection(
    collection_name="day5_knowledge_base",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE,
    ),
)
```

A collection is a named container for vectors.

* `size=384` matches the embedding model output.
* `Distance.COSINE` compares how similar vectors are.

## `QdrantVectorStore`

```python
vector_store = QdrantVectorStore(
    client=client,
    collection_name="day5_knowledge_base",
    embedding=embeddings,
)
```

`QdrantVectorStore` connects LangChain documents with Qdrant. It embeds documents before storing them and embeds user questions before searching.

## Adding Documents

```python
vector_store.add_documents(documents)
```

Internally:

```text
Document text
   ↓
Embedding model creates vectors
   ↓
Qdrant stores vectors, text, and metadata
```

## Similarity Search

```python
results = vector_store.similarity_search_with_score(
    query=question,
    k=3,
)
```

Internally:

```text
User question
   ↓
Embedding model creates a query vector
   ↓
Qdrant compares it with stored vectors
   ↓
Returns the closest document chunks
```

The result contains a `Document` and its similarity score.

# 🧭 Query Routing

A query routing agent decides which source should answer a question.

```text
User question
   ↓
Routing agent
   ↓
📚 RAG tool / 🔌 MCP tool / 💬 Direct response
```

Example routing:

| User question type               | Correct source           |
| -------------------------------- | ------------------------ |
| MCP, ADK, RAG concepts           | Qdrant knowledge base    |
| Project status or remaining days | Project tool or MCP tool |
| Greeting or casual message       | Direct response          |

One agent can receive multiple tools:

```python
tools=[
    search_knowledge_base,
    get_project_status,
]
```

The agent reads the tool names, type hints, docstrings, and instructions, then selects the correct tool.

```text
“What is MCP?”
→ search_knowledge_base()

“What is the status of google-adk-learning?”
→ get_project_status()

“Hello”
→ No tool call
```

Routing improves accuracy because it prevents the agent from searching the wrong source.

# 🔁 Multi-Hop Retrieval

Multi-hop retrieval means the agent searches more than once when one search is not enough.

```text
User question
   ↓
First retrieval
   ↓
Agent reads result
   ↓
Second retrieval if information is missing
   ↓
Final grounded answer
```

A simple question may need one search:

```text
“What is Qdrant?”
→ One retrieval call
```

A combined question may need multiple searches:

```text
“How do ADK, MCP, and Qdrant work together in Agentic RAG?”
```

The agent can retrieve information step by step:

```text
1. Search for how ADK uses MCP.
2. Read the retrieved MCP information.
3. Search for how Qdrant supports Agentic RAG.
4. Combine the retrieved information into one answer.
```

The retrieval tool is added once:

```python
tools=[search_knowledge_base]
```

The LLM can call it multiple times when the instructions allow multi-hop retrieval.

# 🛡️ Grounding

A grounded answer is based on retrieved evidence instead of the model guessing.

```text
❌ Ungrounded:
“MCP was created in a certain year.”

✅ Grounded:
“Based on the retrieved notes, MCP is a standard way for agents
to connect with external tools and services.”
```

For RAG questions, the agent should retrieve relevant chunks before answering and should not add facts that are not present in those chunks.

# 📌 Citations with Metadata

Metadata is extra information attached to a document.

```python
Document(
    page_content="MCP stands for Model Context Protocol.",
    metadata={
        "source": "day4_mcp_notes.md",
        "section": "What is MCP",
    }
)
```

```text
Document chunk
├── page_content → actual text
└── metadata
    ├── source
    └── section
```

Qdrant stores this metadata with the vector. When the document is retrieved, the source information also returns.

A grounded answer can include citations such as:

```text
Sources:
[day4_mcp_notes.md — What is MCP]
```

# 🔔 Callbacks and Guardrails

A callback is a function that runs at a specific point in the agent flow.

```text
User message
   ↓
Before-agent callback
   ↓
Agent reasoning and tool calls
   ↓
Before-tool callback
   ↓
Tool runs
   ↓
After-tool callback
   ↓
Final answer
   ↓
After-agent callback
```

Callbacks can be used for guardrails, logging, validation, observability, and citation checks.

## `before_tool_callback`

```python
before_tool_callback=validate_retrieval_query
```

This runs before the retrieval tool starts.

```text
Agent wants to search
   ↓
Validate query
   ↓
Valid query → Tool runs
Invalid query → Tool is blocked
```

Returning `None` allows the tool call.

Returning a dictionary stops the tool call and sends that dictionary back as the tool result.

## `after_tool_callback`

```python
after_tool_callback=inspect_retrieval_result
```

This runs after the retrieval tool returns.

```text
Qdrant search finishes
   ↓
Inspect result
   ↓
Chunks found → Allow result
No chunks → Return a clear fallback message
```

Callbacks validate tool usage, but the agent instruction is still needed to enforce response behavior such as citations.

```text
🛠️ Retrieval tool → gets evidence
🛡️ Callbacks → validate tool use
🧠 Agent instruction → requires citations and grounded answers
```

Together, these parts make the RAG system more reliable.

# Day 5 Capstone — Explanation of the Architecture and Internal Flow

## Project Goal

This capstone combines Google ADK agents, Chrome MCP, PDF processing, Qdrant vector search, multi-hop retrieval, grounding, citations, and query routing.

The system uses one approved public PDF source:

Stanford CS229 Linear Algebra Review PDF.

The purpose is to let a user ask questions about the PDF and receive answers based only on retrieved PDF content, including page citations.

## Overall Architecture

```text
User
  ↓
Coordinator Agent
  ↓
────────────────────────────────────────────
│                                          │
PDF RAG Specialist                  Chrome MCP Specialist
│                                          │
Qdrant Vector Database              Chrome DevTools MCP
│                                          │
PDF chunks with page metadata       Opens/inspects approved public PDF URL
────────────────────────────────────────────
  ↓
Grounded answer with PDF citations
```

The project is split into three files so that each file has one clear responsibility.

```text
Day-05-Agentic-RAG-Capstone/
│
├── capstone_pdf_rag.py
├── capstone_chrome_mcp.py
└── capstone_multi_agent.py
```

## 1. `capstone_pdf_rag.py` — PDF Ingestion and Retrieval Layer

This file is responsible for converting a PDF into a searchable knowledge base.

It does not contain the ADK coordinator logic and does not communicate with Chrome MCP directly.

Its main responsibilities are:

```text
1. Download an approved PDF.
2. Load the PDF page by page.
3. Split pages into smaller chunks.
4. Convert chunks into embeddings.
5. Store embeddings in Qdrant.
6. Search Qdrant when the agent needs information.
7. Return chunks with PDF page numbers for citations.
```

The approved PDF is stored in an allowlist:

```python
ALLOWED_PDF_SOURCES = {
    "cs229_linear_algebra": {
        "url": "https://cs229.stanford.edu/section/cs229-linalg.pdf",
        "filename": "cs229_linear_algebra.pdf",
    }
}
```

This is a safety control. The system does not download arbitrary URLs given by users. It only downloads known sources that the developer has approved.

The internal PDF ingestion flow is:

```text
Approved PDF URL
  ↓
requests downloads the PDF into data/pdfs
  ↓
PyPDFLoader reads the PDF page by page
  ↓
Each page becomes a LangChain Document
  ↓
RecursiveCharacterTextSplitter breaks pages into smaller chunks
  ↓
HuggingFaceEmbeddings converts each chunk into a 384-dimensional vector
  ↓
Qdrant stores:
- vector
- chunk text
- source name
- source URL
- page number
```

The important functions are:

```text
download_approved_pdf()
→ Downloads only an allowlisted PDF.

build_pdf_knowledge_base()
→ Loads the PDF, chunks it, creates embeddings, and stores vectors in Qdrant.

search_pdf_knowledge_base()
→ Converts the user question into an embedding and retrieves the closest PDF chunks.

get_pdf_source_details()
→ Returns the approved source name and URL.
```

When `search_pdf_knowledge_base()` returns results, it includes the original text plus metadata such as:

```text
Source: Stanford CS229 Linear Algebra Review
Page: 25
```

This makes grounded citations possible.

## 2. `capstone_chrome_mcp.py` — Browser and Source-Inspection Layer

This file creates a specialist agent connected to Chrome DevTools MCP.

Its purpose is not to download or parse PDFs. Its purpose is to safely inspect the approved public PDF URL in Chrome.

```text
Chrome PDF Specialist
  ↓
MCPToolset
  ↓
Chrome DevTools MCP
  ↓
Chrome browser
  ↓
Approved Stanford PDF URL
```

The agent uses:

```python
MCPToolset(
    connection_params=StdioConnectionParams(
        command="npx",
        args=["-y", "chrome-devtools-mcp@latest"],
    )
)
```

Internally, ADK starts the Chrome DevTools MCP server through `npx`. The MCP server exposes browser tools to the Chrome specialist agent.

The Chrome specialist is intentionally restricted by instructions:

```text
Allowed:
- Open the approved public PDF URL
- Inspect the approved PDF page
- Confirm the source URL

Not allowed:
- Open arbitrary URLs
- Log into websites
- Submit forms
- Download arbitrary files
- Access private browser pages
```

This is an example of safe scoping and least privilege.

## 3. `capstone_multi_agent.py` — Coordinator and Agent Orchestration Layer

This is the main entry point of the application.

It creates three ADK agents:

```text
1. Coordinator Agent
2. PDF RAG Specialist
3. Chrome PDF Specialist
```

The PDF RAG specialist uses functions imported from `capstone_pdf_rag.py`.

```python
from capstone_pdf_rag import (
    build_pdf_knowledge_base,
    get_pdf_source_details,
    search_pdf_knowledge_base,
)
```

These functions are wrapped as ADK tools:

```text
prepare_pdf_knowledge_base()
→ Builds the Qdrant knowledge base.

search_pdf(question)
→ Searches the PDF knowledge base.

get_approved_pdf_source()
→ Returns the approved PDF source information.
```

The PDF RAG specialist uses these tools to answer factual questions about linear algebra.

```text
PDF RAG Specialist
  ↓
prepare_pdf_knowledge_base()
  ↓
search_pdf()
  ↓
Qdrant retrieval
  ↓
Grounded answer with page citations
```

The coordinator agent does not search Qdrant or use Chrome directly.

Its only responsibility is query routing.

```text
Question about vectors, matrices, linear algebra, or PDF content
  ↓
Route to PDF RAG Specialist

Question about the approved PDF URL or inspecting the PDF source
  ↓
Route to Chrome PDF Specialist

Greeting or casual conversation
  ↓
Coordinator answers directly
```

This separation makes the architecture easier to maintain because each agent has a focused role.

## Multi-Hop Retrieval

Multi-hop retrieval is used when one search result is not enough to answer a question.

For example:

```text
User:
What is linear independence and how is it related to vectors?
```

The PDF RAG specialist can do this:

```text
1. Search PDF:
“What is linear independence?”

2. Read retrieved chunks.

3. Search PDF again:
“How are vectors related to linear independence?”

4. Combine both retrieved results.

5. Return a final answer with PDF page citations.
```

The agent is allowed to call `search_pdf()` more than once because its instructions explicitly permit additional retrieval when information is missing.

## Grounding and Citations

Grounding means the final answer must be based on retrieved PDF chunks instead of the model’s general knowledge.

The RAG specialist is instructed to:

```text
- Always retrieve before answering factual PDF questions.
- Answer only using retrieved chunks.
- Avoid inventing missing information.
- Include source citations with page numbers.
```

A final answer should look similar to:

```text
Linear independence means that no vector in a set can be written as a
combination of the other vectors. It is important because independent
vectors provide unique directions in a vector space.

Sources:
[Stanford CS229 Linear Algebra Review — page 25]
```

## Full Internal Process

```text
User asks:
“What is linear independence and how is it related to vectors?”

        ↓

Coordinator Agent reads the question.

        ↓

Coordinator identifies it as a PDF knowledge question.

        ↓

Coordinator delegates the request to PDF RAG Specialist.

        ↓

PDF RAG Specialist checks whether the Qdrant knowledge base exists.

        ↓

If needed:
- Download approved PDF
- Load PDF pages
- Split pages into chunks
- Create embeddings
- Store chunks in Qdrant

        ↓

PDF RAG Specialist calls search_pdf().

        ↓

Qdrant returns the most semantically similar chunks with page metadata.

        ↓

If one search is insufficient, the agent calls search_pdf() again.

        ↓

PDF RAG Specialist creates an answer only from retrieved chunks.

        ↓

The answer includes PDF page citations.
```

## Why This Is Agentic RAG

This is Agentic RAG because the system does not use one fixed retrieval pipeline for every user message.

The coordinator decides which specialist should handle the request.

The PDF RAG specialist decides whether it needs one retrieval call or multiple retrieval calls.

The Chrome specialist is used only for source inspection questions.

```text
Routing
+ Tool calling
+ Multi-hop retrieval
+ Grounded answers
+ Citations
+ MCP integration
= Agentic RAG system
```
