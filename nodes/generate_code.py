from state import ThinkDeployState
from llm.llm import llm

def generate_code(state: ThinkDeployState) -> ThinkDeployState:
    prompt = f"""
You are a senior software engineer.

Design Document:
{state.design_doc}

User Feedback for Code:
{state.code_feedback}

Generate modular Python code using classes or functions. Ensure clean architecture.
"""
    result = llm.invoke(prompt)
    return state.copy(update={"generated_code": result.content.strip()})
