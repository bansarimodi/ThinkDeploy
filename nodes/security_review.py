from state import ThinkDeployState
from llm.llm import llm

def security_review(state: ThinkDeployState) -> ThinkDeployState:
    prompt = f"""
You are a security analyst.

Here are the security recommendations generated:
{state.security_guidelines}

Please review and suggest improvements or flag missing concerns.
"""
    result = llm.invoke(prompt)
    return state.copy(update={"security_review": result.content.strip()})
