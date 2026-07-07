from google.adk.agents import LlmAgent

def square_number(number: int) -> int:
    return number*number

agent=LlmAgent(
    name="MathAgent",
    model="gemini-2.5-flash",
    instruction='''You are a helpful math assistant.
    Use the square tool whenever asked to square a number.''',
    tools=[square_number]
)
