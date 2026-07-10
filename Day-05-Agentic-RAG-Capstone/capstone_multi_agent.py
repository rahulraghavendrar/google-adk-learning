import asyncio
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from capstone_chrome_mcp import chrome_pdf_specialist
from capstone_pdf_rag import (
    build_pdf_knowledge_base,
    get_pdf_source_details,
    search_pdf_knowledge_base,
)
load_dotenv()
def prepare_pdf_knowledge_base() -> dict:
    """Downloads and indexes the approved PDF before document questions are answered."""
    return build_pdf_knowledge_base()
def search_pdf(question: str) -> dict:
    """Searches the approved Stanford CS229 PDF and returns chunks with page citations."""
    if not question.strip():
        return {
            "success": False,
            "message": "The PDF search question cannot be empty.",
        }
    return search_pdf_knowledge_base(question, k=3)
def get_approved_pdf_source() -> dict:
    """Returns the title and URL of the approved public PDF source."""
    return get_pdf_source_details()


rag_specialist = LlmAgent(
    name="pdf_rag_specialist",
    model="gemini-2.5-flash",
    instruction="""
You are a grounded PDF RAG specialist.

Your knowledge source is the approved Stanford CS229 Linear Algebra Review PDF.

For every factual question about linear algebra or the PDF:
1. Call prepare_pdf_knowledge_base if the knowledge base is not ready.
2. Call search_pdf with a focused query.
3. Read the retrieved chunks.
4. If the first retrieval does not answer every part of the question,
   call search_pdf again with a more specific follow-up query.
5. Answer only using the retrieved chunks.

This is multi-hop retrieval. You may search more than once when needed.

Every factual answer must end with:

Sources:
[Stanford CS229 Linear Algebra Review — page X]

If the retrieved chunks do not contain enough information, say so clearly.
Do not invent information.
Keep answers simple and concise.
""",
    tools=[
        prepare_pdf_knowledge_base,
        search_pdf,
        get_approved_pdf_source,
    ],
)
coordinator_agent = LlmAgent(
    name="day5_capstone_coordinator",
    model="gemini-2.5-flash",
    instruction="""
You are the coordinator for a safe multi-agent PDF RAG system.

Route questions about:
- vectors
- matrices
- linear algebra
- content from the Stanford CS229 PDF
- explanations that require PDF evidence

to pdf_rag_specialist.

Route questions about:
- the approved PDF URL
- whether the PDF source is public
- opening or inspecting the approved PDF in Chrome

to chrome_pdf_specialist.

For greetings or simple casual conversation, answer directly.

Do not answer PDF factual questions yourself.
Delegate them to pdf_rag_specialist.
Do not route users to arbitrary URLs.
""",
    sub_agents=[
        rag_specialist,
        chrome_pdf_specialist,
    ],
)
async def main():
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="day5_pdf_rag_capstone",
        user_id="rahul",
        session_id="day5_pdf_rag_session",
    )
    runner = Runner(
        agent=coordinator_agent,
        app_name="day5_pdf_rag_capstone",
        session_service=session_service,
    )
    print("Day 5 Capstone: Multi-Agent PDF RAG")
    print("Type 'exit' to stop.\n")
    print("Try:")
    print("• What is the approved PDF source?")
    print("• Explain matrix-vector multiplication from the PDF.")
    print("• What is linear independence and how is it related to vectors?")
    print("• Explain the difference between matrix-vector and matrix-matrix multiplication.\n")
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
                            print(f"\nAssistant: {part.text}\n")
        except Exception as error:
            print(f"\nError: {error}\n")
if __name__ == "__main__":
    asyncio.run(main())