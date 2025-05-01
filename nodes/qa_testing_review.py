from state import ThinkDeployState
from llm.llm import llm

def qa_testing_review(state: ThinkDeployState) -> ThinkDeployState:
    prompt = f"""
You are a senior QA reviewer.

Here are the QA results:
{state.qa_results}

Evaluate whether QA passed. If not, specify required fixes or retesting.
"""
    result = llm.invoke(prompt)
    return state.copy(update={"qa_review": result.content.strip()})
