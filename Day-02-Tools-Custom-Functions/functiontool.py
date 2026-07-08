from google.adk.agents import LlmAgent

def cube_number(number: int) -> int:
    '''Calculates the cube of a given number'''
    return number * number * number

agent=LlmAgent(
    name="CubeAgent",
    model="gemini-2.5-flash",
    instruction='''You are helpful math assistant used to calculate the cube of a number
    Use the necessary cube tool when asked to.'''
    tools=[cube_number]
)