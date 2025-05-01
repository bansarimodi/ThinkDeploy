from state import ThinkDeployState
from llm.llm import llm

def deployment(state: ThinkDeployState) -> ThinkDeployState:
    prompt = f"""
Prepare a deployment plan.

Project Name: {state.project_name}
Requirements: {state.requirements}
Design Overview:
{state.design_doc}

User Feedback for Deployment:
{state.deployment_feedback}

Include: Environment setup, CI/CD strategy, and rollback plan.
"""
    result = llm.invoke(prompt)
    return state.copy(update={"deployment_plan": result.content.strip()})
