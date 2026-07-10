# 🚀 Day 5 — RAG with Agents + Capstone

## 🎯 Goal

Combine **RAG**, **Google ADK agents**, and **MCP tools** to build an agent that can choose the right source of information before answering.

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

This works for document questions, but it may retrieve information even when it is unnecessary.

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

The agent is not forced to use the tool for every message. The tool is used only when the question needs knowledge from the documents.

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

A document can also contain metadata, such as file name, page number, or source.

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

```text
Agent
   ↓
search_knowledge_base("How does ADK use MCP?")
   ↓
Retrieved MCP chunks
   ↓
search_knowledge_base("How does Qdrant help Agentic RAG?")
   ↓
Retrieved Qdrant chunks
   ↓
Grounded final answer
```

Multi-hop retrieval is useful when a question combines several concepts or requires information from different document sections.
