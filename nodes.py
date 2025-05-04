from prompts import *
from typing import Dict
import random
from llm import llm


def generate_user_story(state: Dict) -> Dict:
    prompt = generate_user_story_prompt.format(requirements=state["requirements"])
    result = llm.invoke(prompt)
    return {"user_story": result.content}


def design_project(state: Dict) -> Dict:
    prompt = design_project_prompt.format(
        user_story=state["user_story"],
        feedback=state.get("review_feedback", "")
    )
    result = llm.invoke(prompt)
    return {"design_doc": result.content}


def generate_code(state: Dict) -> Dict:
    prompt = generate_code_prompt.format(design_doc=state["design_doc"])
    result = llm.invoke(prompt)
    return {"code": result.content}


def review_code(state: Dict) -> Dict:
    prompt = review_code_prompt.format(code=state["code"])
    result = llm.invoke(prompt)
    return {"code_review": result.content}


def generate_security_recommendation(state: Dict) -> Dict:
    prompt = security_review_prompt.format(code=state["code"])
    result = llm.invoke(prompt)
    return {"security_report": result.content}


def generate_test_cases(state: Dict) -> Dict:
    prompt = generate_test_cases_prompt.format(code=state["code"])
    result = llm.invoke(prompt)
    return {"test_cases": result.content}


def qa_testing(state: Dict) -> Dict:
    prompt = qa_testing_prompt.format(test_cases=state["test_cases"])
    result = llm.invoke(prompt)
    return {"qa_results": result.content}


def deployment(state: Dict) -> Dict:
    prompt = deployment_prompt.format(code=state["code"])
    result = llm.invoke(prompt)
    return {"deployment_log": result.content}


def human_review(state: Dict) -> Dict:
    feedback = state.get("review_feedback", "")
    approved = False if feedback else random.choice([True, False])
    reason = feedback if feedback else ("Looks good." if approved else "Design needs refinement.")
    return {"approved": approved, "review_feedback": reason}


def test_cases_review(state: Dict) -> Dict:
    feedback = state.get("review_feedback", "")
    approved = False if feedback else random.choice([True, False])
    reason = feedback if feedback else ("Test cases are comprehensive." if approved else "Add more edge cases.")
    return {"approved": approved, "review_feedback": reason}


def qa_testing_review(state: Dict) -> Dict:
    feedback = state.get("review_feedback", "")
    approved = False if feedback else random.choice([True, False])
    reason = feedback if feedback else ("QA passed all checks." if approved else "QA encountered failures.")
    return {"approved": approved, "review_feedback": reason}
