from state import ThinkDeployState
from llm.llm import llm

def generate_code(state: ThinkDeployState) -> ThinkDeployState:
    prompt = f"""
    You are an expert software developer. Generate production-quality code for the following file
    based on the provided requirements and design documents.

Design Document:
{state.design_doc}

User Feedback for Code:
{state.code_feedback}

Generate modular Python code using classes or functions. Ensure clean architecture. Generate complete, well-structured, and fully functional code for this file.
    Include comprehensive comments, proper error handling, and follow best practices for the language.
    The code should be ready for production use.
"""
    result = llm.invoke(prompt)
    return state.copy(update={"generated_code": result.content.strip()})
