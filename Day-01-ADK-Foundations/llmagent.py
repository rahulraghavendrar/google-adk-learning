from google.adk.agents import LlmAgent

agent=LlmAgent(
    name="HelpfulLlmAgent",
    model="gemini-2.5-flash",
    instruction="You are a helpful assistant. Use available tools whenever needed."
)