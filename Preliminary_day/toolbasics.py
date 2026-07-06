from google.adk.agents import Agent

def square_number(number:int)->int:
    return number*number

agent=Agent(
    name="MathAgent",
    model="gemini-2.5-flash",
    instruction="You are a helpful math assistant. Use available tools whenever needed.",
    tools=[square_number]
)
print("Agent Created Successfully!")
print(f"Agent Name: {agent.name}")
print("\nRegistered Tools:")
for tool in agent.tools:
    print(f" - {tool.__name__}")