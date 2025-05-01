from state import ThinkDeployState
from llm.llm import llm

def generate_security_recommendation(state: ThinkDeployState) -> ThinkDeployState:
    prompt = f"""
You are a cybersecurity engineer.

Analyze the following Python code and provide best practices and recommendations.

Code:
{state.generated_code}

User Feedback for Security:
{state.security_feedback}
"""
    result = llm.invoke(prompt)
    return state.copy(update={"security_guidelines": result.content.strip()})
