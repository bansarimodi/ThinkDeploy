from state import ThinkDeployState
from llm.llm import llm

def generate_test_cases(state: ThinkDeployState) -> ThinkDeployState:
    prompt = f"""
You are a QA test engineer.

Project Requirements:
{state.requirements}

Design Summary:
{state.design_doc}

Code:
{state.generated_code}

User Feedback for Test Cases:
{state.test_cases_feedback}

Generate comprehensive functional and edge test cases.
"""
    result = llm.invoke(prompt)
    return state.copy(update={"test_cases": result.content.strip()})
