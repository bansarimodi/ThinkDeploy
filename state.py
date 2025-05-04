from typing import Optional, TypedDict


class SDLCState(TypedDict):
    project_name: str
    requirements: str
    user_story: Optional[str]
    design_doc: Optional[str]
    code: Optional[str]
    code_review: Optional[str]
    security_report: Optional[str]
    test_cases: Optional[str]
    qa_results: Optional[str]
    deployment_log: Optional[str]
    review_feedback: Optional[str]
    approved: Optional[bool]
    test_case_retries: int
    qa_retries: int


class SDLCStateRouter:
    def __init__(self, state: SDLCState):
        self.state = state

    def route(self, node: str) -> str:
        if node == "human_review":
            return "generate_code" if self.state.get("approved") else "design_project"

        if node == "test_cases_review":
            if self.state.get("approved"):
                return "qa_testing"
            retries = self.state.get("test_case_retries", 0)
            self.state["test_case_retries"] = retries + 1
            return "generate_test_cases" if retries < 2 else "qa_testing"

        if node == "qa_testing_review":
            if self.state.get("approved"):
                return "deployment"
            retries = self.state.get("qa_retries", 0)
            self.state["qa_retries"] = retries + 1
            return "generate_code" if retries < 2 else "deployment"

        return "deployment"
