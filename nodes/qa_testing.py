from state import ThinkDeployState
from llm.llm import llm

def qa_testing(state: ThinkDeployState) -> ThinkDeployState:
    prompt = f"""
Simulate QA testing.

Test Cases:
{state.test_cases}

Code:
{state.generated_code}

Summarize results: bugs found, test outcomes, and severity.
"""
    result = llm.invoke(prompt)
    return state.copy(update={"qa_results": result.content.strip()})
