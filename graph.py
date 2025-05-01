from langgraph.graph import StateGraph
from state import ThinkDeployState

# Import node functions
from nodes.user_story import generate_user_stories
from nodes.design_project import design_project
from nodes.generate_code import generate_code
from nodes.review_code import review_code
from nodes.generate_security_recommendation import generate_security_recommendation
from nodes.security_review import security_review
from nodes.generate_test_cases import generate_test_cases
from nodes.test_cases_review import test_cases_review
from nodes.qa_testing import qa_testing
from nodes.qa_testing_review import qa_testing_review
from nodes.deployment import deployment
from nodes.end import end

def build_graph():
    builder = StateGraph(ThinkDeployState)

    builder.add_node("GenerateUserStories", generate_user_stories)
    builder.add_node("DesignProject", design_project)
    builder.add_node("GenerateCode", generate_code)
    builder.add_node("ReviewCode", review_code)
    builder.add_node("GenerateSecurityRecommendation", generate_security_recommendation)
    builder.add_node("SecurityReview", security_review)
    builder.add_node("GenerateTestCases", generate_test_cases)
    builder.add_node("TestCasesReview", test_cases_review)
    builder.add_node("QATesting", qa_testing)
    builder.add_node("QATestingReview", qa_testing_review)
    builder.add_node("Deployment", deployment)
    builder.add_node("End", end)

    builder.set_entry_point("GenerateUserStories")
    builder.add_edge("GenerateUserStories", "DesignProject")
    builder.add_edge("DesignProject", "GenerateCode")
    builder.add_edge("GenerateCode", "ReviewCode")
    builder.add_edge("ReviewCode", "GenerateSecurityRecommendation")
    builder.add_edge("GenerateSecurityRecommendation", "SecurityReview")
    builder.add_edge("SecurityReview", "GenerateTestCases")
    builder.add_edge("GenerateTestCases", "TestCasesReview")
    builder.add_edge("TestCasesReview", "QATesting")
    builder.add_edge("QATesting", "QATestingReview")

    def qa_review_conditional(state: ThinkDeployState) -> str:
        return "Deployment" if state.qa_approved else "GenerateCode"

    builder.add_conditional_edges("QATestingReview", qa_review_conditional)
    builder.add_edge("Deployment", "End")

    return builder.compile()
