import asyncio
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
load_dotenv()
APPROVED_PDF_URL = "https://cs229.stanford.edu/section/cs229-linalg.pdf"
chrome_toolset = MCPToolset(
    connection_params=StdioConnectionParams(
        command="npx",
        args=[
            "-y",
            "chrome-devtools-mcp@latest",
        ],
    )
)
chrome_pdf_specialist = LlmAgent(
    name="chrome_pdf_specialist",
    model="gemini-2.5-flash",
    instruction=f"""
You are a safe browser specialist.

You may inspect only this approved public PDF URL:
{APPROVED_PDF_URL}

Use Chrome MCP tools only to open or inspect this approved URL.

Do not:
- open any other URL
- log into websites
- submit forms
- download files
- make purchases
- access private browser pages

When asked about the approved PDF source, briefly confirm that it is a
public Stanford CS229 PDF and provide the approved URL.
""",
    tools=[chrome_toolset],
)