from google.adk.agents import Agent
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)

documents = [
    "Google ADK is a framework for building AI agents.",
    "Agents can use tools to perform actions.",
    "Agents can use memory to remember information.",
    "Qdrant is a vector database used in RAG systems.",
    "Embeddings convert text into numerical vectors."
]

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

vectors = embedding_model.encode(documents)

client = QdrantClient(":memory:")

client.create_collection(
    collection_name="rag_demo",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)

points = []

for i, (doc, vector) in enumerate(
    zip(documents, vectors)
):
    points.append(
        PointStruct(
            id=i,
            vector=vector.tolist(),
            payload={
                "text": doc
            }
        )
    )

client.upsert(
    collection_name="rag_demo",
    points=points
)


def retrieve_documents(query: str) -> str:
    query_vector = embedding_model.encode(query)

    results = client.query_points(
        collection_name="rag_demo",
        query=query_vector.tolist(),
        limit=3
    )

    retrieved_chunks = []

    for point in results.points:
        retrieved_chunks.append(
            point.payload["text"]
        )

    return "\n".join(retrieved_chunks)


agent = Agent(
    name="RAGAgent",
    model="gemini-2.5-flash",
    description="A RAG Agent using Qdrant",
    instruction="""
    Use the retrieve_documents tool
    to answer user questions.

    Always use retrieved context
    before generating answers.
    """,
    tools=[retrieve_documents]
)

print("Agent Created Successfully")
print("Tool Registered:")
print(agent.tools)