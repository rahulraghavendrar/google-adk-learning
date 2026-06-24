from google.adk.agents import Agent


def square_number(number: int) -> int:
    return number * number


print("Testing the tool directly:")
print(square_number(5))


agent = Agent(
    name="MathAgent",
    model="gemini-2.5-flash",
    description="A simple math assistant",
    instruction="""
    You are a helpful math assistant.
    Use available tools whenever needed.
    """,
    tools=[square_number]
)

print("\nAgent Created Successfully!")
print(f"Agent Name: {agent.name}")

print("\nRegistered Tools:")
for tool in agent.tools:
    print(tool.name)
