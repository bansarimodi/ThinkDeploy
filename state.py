from pydantic import BaseModel

class ThinkDeployState(BaseModel):
    project_name: str = ""
    requirements: str = ""

    # User Story
    user_stories: str = ""
    user_story_feedback: str = ""

    # Design
    design_doc: str = ""
    design_feedback: str = ""

    # Code Generation & Review
    generated_code: str = ""
    code_feedback: str = ""
    code_review: str = ""

    # Security
    security_guidelines: str = ""
    security_feedback: str = ""
    security_review: str = ""

    # Test Cases
    test_cases: str = ""
    test_cases_feedback: str = ""
    test_cases_review: str = ""

    # QA
    qa_results: str = ""
    qa_feedback: str = ""
    qa_review: str = ""
    qa_approved: bool = False

    # Deployment
    deployment_plan: str = ""
    deployment_feedback: str = ""
