import asyncio
from google.adk.sessions import InMemorySessionService
session_service = InMemorySessionService()
session= await session_service.create_session(
    app_name="my_app",
    user_id="user_1",
    session_id="session1"
)