from google.adk.agents import LlmAgent

def divide_numbers(dividend: float,divisor:float)->float:
    '''Calculate the division of the dividend by the divisor
    Return an error message if the divisor is zero'''
    if divisor == 0:
        return "Error: Division by zero is not allowed."
    return dividend / divisor

agent=LlmAgent(
    name="DivisionAgent",
    model="gemini-2.5-flash",
    instruction='''You are a helpful division agent
    Use the necessary division tool when asked to divide two numbers.''',
    tools=[divide_numbers]
)