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
It is a standard that allows AI agents to connect with external tools,
data sources, and services through MCP servers.
"""
    ),
    Document(
        page_content="""
Google ADK uses MCPToolset to connect an LlmAgent to tools exposed
by an MCP server.
"""
    ),
    Document(
        page_content="""
RAG stands for Retrieval-Augmented Generation.
It retrieves relevant document chunks and gives them to an LLM
so answers can be based on retrieved information.
"""
    ),
    Document(
        page_content="""
Agentic RAG allows an agent to decide whether retrieval is needed.
The agent can call a retrieval tool only when the user asks a question
that requires knowledge from the document collection.
"""
    ),
]


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


client = QdrantClient(":memory:")


client.create_collection(
    collection_name="routing_knowledge_base",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE,
    ),
)


vector_store = QdrantVectorStore(
    client=client,
    collection_name="routing_knowledge_base",
    embedding=embeddings,
)


vector_store.add_documents(documents)


projects = [
    {
        "name": "google-adk-learning",
        "status": "In progress",
        "completed_days": 5,
        "total_days": 7,
    },
    {
        "name": "agentic-ai",
        "status": "Active",
        "completed_days": 12,
        "total_days": 20,
    },
]


def search_knowledge_base(question: str) -> dict:
    """Searches the learning knowledge base for MCP, ADK, RAG, and Agentic RAG information."""
    results = vector_store.similarity_search_with_score(
        query=question,
        k=3,
    )

    chunks = []

    for document, score in results:
        chunks.append(
            {
                "content": document.page_content.strip(),
                "similarity_score": round(float(score), 4),
            }
        )

    return {
        "source": "Qdrant learning knowledge base",
        "retrieved_chunks": chunks,
    }


def get_project_status(project_name: str) -> dict:
    """Gets the current status and progress of a learning project."""
    project_name = project_name.lower().strip()

    for project in projects:
        if project["name"] == project_name:
            return {
                "success": True,
                "source": "Project status tool",
                "project_name": project["name"],
                "status": project["status"],
                "completed_days": project["completed_days"],
                "total_days": project["total_days"],
                "days_remaining": project["total_days"] - project["completed_days"],
            }

    return {
        "success": False,
        "source": "Project status tool",
        "message": f"Project '{project_name}' was not found.",
    }


routing_agent = LlmAgent(
    name="query_routing_agent",
    model="gemini-2.5-flash",
    instruction="""
You are a learning assistant with two information sources.

Use search_knowledge_base for questions about:
- MCP
- Google ADK
- RAG
- Agentic RAG
- concepts from the learning notes

Use get_project_status for questions about:
- project status
- completed days
- total days
- remaining days
- google-adk-learning
- agentic-ai

For greetings and casual conversation, answer directly without tools.

Always use the correct tool for factual questions.
Do not invent information.
When you use search_knowledge_base, answer only using the retrieved chunks.
Mention the source used in your answer.
Keep the response short and easy to understand.
""",
    tools=[
        search_knowledge_base,
        get_project_status,
    ],
)


async def main():
    session_service = InMemorySessionService()

    session = await session_service.create_session(
        app_name="query_routing_app",
        user_id="rahul",
        session_id="query_routing_session_1",
    )

    runner = Runner(
        agent=routing_agent,
        app_name="query_routing_app",
        session_service=session_service,
    )

    print("🧭 Day 5 Query Routing Agent")
    print("Type 'exit' to stop.\n")

    print("Try:")
    print("• What is MCP?")
    print("• Explain Agentic RAG.")
    print("• What is the status of google-adk-learning?")
    print("• Tell me about agentic-ai.")
    print("• Hello\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("👋 Goodbye!")
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
            print(f"\n❌ Error: {error}\n")


if __name__ == "__main__":
    asyncio.run(main())