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
An MCP server exposes tools, resources, and prompts.
An MCP client connects to the server and can call the exposed tools.
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
A RAG system retrieves relevant document chunks and gives them to an LLM
so the answer can be based on the retrieved information.
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
    collection_name="day5_knowledge_base",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE,
    ),
)


vector_store = QdrantVectorStore(
    client=client,
    collection_name="day5_knowledge_base",
    embedding=embeddings,
)


vector_store.add_documents(documents)


def search_knowledge_base(question: str) -> dict:
    """Searches the Day 5 knowledge base and returns relevant document chunks."""
    results = vector_store.similarity_search_with_score(
        query=question,
        k=3,
    )

    retrieved_chunks = []

    for document, score in results:
        retrieved_chunks.append(
            {
                "content": document.page_content.strip(),
                "similarity_score": round(float(score), 4),
            }
        )

    return {
        "query": question,
        "retrieved_chunks": retrieved_chunks,
    }


rag_agent = LlmAgent(
    name="rag_agent",
    model="gemini-2.5-flash",
    instruction="""
You are a helpful learning assistant.

Use the search_knowledge_base tool when the user asks about:
- MCP
- Google ADK
- RAG
- Agentic RAG
- concepts that may exist in the knowledge base

Do not use the tool for greetings or simple casual conversation.

When you use the tool:
- Answer only using the retrieved chunks.
- Do not invent facts that are not present in the retrieved chunks.
- Mention that your answer is based on the knowledge base.
- If the retrieved chunks do not contain enough information, say so clearly.

Keep answers simple and easy to understand.
""",
    tools=[search_knowledge_base],
)


async def main():
    session_service = InMemorySessionService()

    session = await session_service.create_session(
        app_name="day5_rag_tool_app",
        user_id="rahul",
        session_id="day5_rag_session_1",
    )

    runner = Runner(
        agent=rag_agent,
        app_name="day5_rag_tool_app",
        session_service=session_service,
    )

    print("Day 5 RAG Tool Agent")
    print("Type 'exit' to stop.\n")

    print("Try:")
    print("• What is MCP?")
    print("• Explain Agentic RAG.")
    print("• How does ADK use MCP?")
    print("• Hello\n")

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