from state import ThinkDeployState
from llm.llm import llm

def design_project(state: ThinkDeployState) -> ThinkDeployState:
    prompt = f"""
You are a senior software architect.

Project Requirements:
{state.requirements}

User Stories:
{state.user_stories}

User Feedback for Design:
{state.design_feedback}

Generate a markdown-formatted design document with:
1. Project Overview
2. Project Timeline (table)
3. Resource Allocation (table)
4. Risk Assessment (table)
5. Coordination Strategy (bullet points)
"""
    result = llm.invoke(prompt)
    return state.copy(update={"design_doc": result.content.strip()})
