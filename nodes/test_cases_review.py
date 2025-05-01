from state import ThinkDeployState
from llm.llm import llm

def test_cases_review(state: ThinkDeployState) -> ThinkDeployState:
    prompt = f"""
You are a QA reviewer.

Here are the generated test cases:
{state.test_cases}

Provide a review and identify missing edge cases or logic coverage gaps.
"""
    result = llm.invoke(prompt)
    return state.copy(update={"test_cases_review": result.content.strip()})
