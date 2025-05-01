from state import ThinkDeployState
from llm.llm import llm

def generate_user_stories(state: ThinkDeployState) -> ThinkDeployState:
    prompt = f"""
You are an Agile analyst.

Based on the project below, generate 3 detailed user stories in this format:
- As a [user], I want to [do something], so that [benefit].

Project Name: {state.project_name}
Requirements: {state.requirements}
"""
    result = llm.invoke(prompt)
    return state.copy(update={"user_stories": result.content.strip()})
