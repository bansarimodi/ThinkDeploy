from state import ThinkDeployState
from llm.llm import llm

def review_code(state: ThinkDeployState) -> ThinkDeployState:
    prompt = f"""
You are a software architecture reviewer.

Here is the generated code:
{state.generated_code}

Please review the code for:
- Structure
- Readability
- Maintainability
- Security risks

Provide a concise review.
"""
    result = llm.invoke(prompt)
    return state.copy(update={"code_review": result.content.strip()})
