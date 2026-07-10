import asyncio

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


load_dotenv()


documents = [
    Document(
        page_content="""
MCP stands for Model Context Protocol.
It is a standard way for AI agents to connect with external tools,
data sources, and services through MCP servers.
""",
        metadata={
            "source": "day4_mcp_notes.md",
            "section": "What is MCP",
        },
    ),
    Document(
        page_content="""
Google ADK uses MCPToolset to connect an LlmAgent to tools exposed
by an MCP server.
""",
        metadata={
            "source": "day4_mcp_notes.md",
            "section": "MCPToolset in ADK",
        },
    ),
    Document(
        page_content="""
RAG stands for Retrieval-Augmented Generation.
It retrieves relevant document chunks and provides them to an LLM
so answers can be based on retrieved information.
""",
        metadata={
            "source": "day5_rag_notes.md",
            "section": "Naive RAG vs Agentic RAG",
        },
    ),
    Document(
        page_content="""
Agentic RAG allows an agent to decide when retrieval is needed.
It can call retrieval tools, route questions to different sources,
and retrieve again when the first search is not enough.
""",
        metadata={
            "source": "day5_rag_notes.md",
            "section": "Agentic RAG",
        },
    ),
]


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


client = QdrantClient(":memory:")


client.create_collection(
    collection_name="grounded_knowledge_base",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE,
    ),
)


vector_store = QdrantVectorStore(
    client=client,
    collection_name="grounded_knowledge_base",
    embedding=embeddings,
)


vector_store.add_documents(documents)


def search_knowledge_base(question: str) -> dict:
    """Searches the knowledge base and returns relevant chunks with citations."""
    results = vector_store.similarity_search_with_score(
        query=question,
        k=3,
    )

    chunks = []

    for document, score in results:
        chunks.append(
            {
                "content": document.page_content.strip(),
                "source": document.metadata.get("source", "Unknown source"),
                "section": document.metadata.get("section", "Unknown section"),
                "similarity_score": round(float(score), 4),
            }
        )

    return {
        "query": question,
        "retrieved_chunks": chunks,
    }


def validate_retrieval_query(
    tool,
    args,
    tool_context,
):
    """Blocks an empty retrieval query before the Qdrant search runs."""
    question = args.get("question", "").strip()

    if not question:
        return {
            "error": "The retrieval query cannot be empty."
        }

    return None


def inspect_retrieval_result(
    tool,
    args,
    tool_context,
    tool_response,
):
    """Checks that the retrieval tool returned document chunks."""
    chunks = tool_response.get("retrieved_chunks", [])

    if not chunks:
        return {
            "query": args.get("question", ""),
            "retrieved_chunks": [],
            "message": "No relevant knowledge-base chunks were found.",
        }

    return None


grounded_rag_agent = LlmAgent(
    name="grounded_rag_agent",
    model="gemini-2.5-flash",
    instruction="""
You are a grounded learning assistant.

Use search_knowledge_base for questions about MCP, Google ADK, RAG,
and Agentic RAG.

For knowledge-base questions:
- Always use search_knowledge_base first.
- Answer only using the retrieved chunks.
- Do not add facts that are not in the retrieved chunks.
- End every grounded answer with a Sources section.
- In Sources, list each source in this format:
  [source file — section]

If the tool says no relevant chunks were found, say that the knowledge
base does not contain enough information.

Keep answers short and easy to understand.
""",
    tools=[search_knowledge_base],
    before_tool_callback=validate_retrieval_query,
    after_tool_callback=inspect_retrieval_result,
)


async def main():
    session_service = InMemorySessionService()

    session = await session_service.create_session(
        app_name="grounded_rag_app",
        user_id="rahul",
        session_id="grounded_rag_session_1",
    )

    runner = Runner(
        agent=grounded_rag_agent,
        app_name="grounded_rag_app",
        session_service=session_service,
    )

    print("Grounded RAG Agent")
    print("Type 'exit' to stop.\n")

    print("Try:")
    print("• What is MCP?")
    print("• Explain Agentic RAG.")
    print("• How does ADK use MCP?\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        if not user_input:
            continue

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
                            print(f"\n🤖 Assistant: {part.text}\n")

        except Exception as error:
            print(f"\nError: {error}\n")
if __name__ == "__main__":
    asyncio.run(main())