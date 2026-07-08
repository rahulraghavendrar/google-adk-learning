from google.adk.agents import LlmAgent

def validate_transfer_amount(amount: float) -> dict:
    '''Validates if the transfer amount is within the allowed range'''
    maximum_allowed_amount = 100000.0
    if amount<=0:
        return{
            "allowed": False,
            "message": "Transfer amount must be a positive value."
        }
    elif amount>maximum_allowed_amount:
        return{
            "allowed": False,
            "message": f"Transfer amount exceeds the maximum allowed limit of {maximum_allowed_amount}."
        }
    else:
        return{
            "allowed": True,
            "message": "Transfer amount is valid."
        }
    
agent=LlmAgent(
    name="TransferValidationAgent",
    model="gemini-2.5-flash",
    instruction='''You are a helpful transfer validation agent.
    Use the necessary validation tool when asked to validate a transfer amount
    and follow the guardrails provided in the tool.''',
    tools=[validate_transfer_amount]
)