import streamlit as st
from state import SDLCState
from graph import build_graph
from nodes import (
    generate_user_story,
    design_project,
    human_review,
    generate_code,
    review_code,
    generate_security_recommendation,
    generate_test_cases,
    test_cases_review,
    qa_testing,
    qa_testing_review,
    deployment,
)
from utils import generate_pdf_file, download_button_from_pdf

st.set_page_config(
    page_title="ThinkDeploy | SDLC Automation",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
body, .stTextArea textarea, .stMarkdown p, .stMarkdown code {
    font-family: 'Segoe UI', sans-serif;
    font-size: 16px;
    line-height: 1.6;
    color: #333333;
}
code {
    background-color: #f6f8fa;
    padding: 10px;
    display: block;
    border-radius: 5px;
    white-space: pre-wrap;
}
</style>
""", unsafe_allow_html=True)

steps = [
    "Project Setup", "Generate User Story", "Design Project", "Human Review",
    "Generate Code", "Code Review", "Security Recommendation",
    "Generate Test Cases", "Test Case Review", "QA Testing",
    "QA Testing Review", "Deployment", "End"
]

if "state" not in st.session_state:
    st.session_state.state = None
if "active_tab" not in st.session_state:
    st.session_state.active_tab = steps[0]

state = st.session_state.state

st.sidebar.title("Workflow Navigation")
st.session_state.active_tab = st.sidebar.radio("Step", steps, index=steps.index(st.session_state.active_tab))

def render_step(title, key, generator_fn, next_step=None):
    if not state:
        st.warning("Please complete the Project Setup first.")
        st.stop()

    st.markdown(f"## {title}")
    current_value = state.get(key)

    if not current_value:
        state.update(generator_fn(state))
        current_value = state.get(key)

    st.markdown(current_value or "_No output generated yet._")

    if next_step and st.button("Continue", key=f"{key}_continue"):
        state["approved"] = True
        st.session_state.state = state
        st.session_state.active_tab = next_step
        st.rerun()

if st.session_state.active_tab == "Project Setup":
    st.title("ThinkDeploy: AI SDLC Pipeline")
    st.markdown("Enter your project details below to begin.")

    project_name = st.text_input("Project Name", value=state["project_name"] if state else "")
    requirements = st.text_area("Project Requirements", value=state["requirements"] if state else "", height=200)

    if st.button("Start SDLC Pipeline"):
        st.session_state.state = {
            "project_name": project_name.strip(),
            "requirements": requirements.strip(),
            "test_case_retries": 0,
            "qa_retries": 0,
            "approved": True,
            "review_feedback": ""
        }
        st.session_state.active_tab = "Generate User Story"
        st.rerun()

elif st.session_state.active_tab == "Generate User Story":
    render_step("User Story", "user_story", generate_user_story, "Design Project")

elif st.session_state.active_tab == "Design Project":
    render_step("Design Document", "design_doc", design_project, "Human Review")

elif st.session_state.active_tab == "Human Review":
    st.markdown("## Human Review of Design Document")
    feedback = st.text_area("Feedback Before Regenerating", key="human_review_feedback")
    st.markdown(f"System Feedback: {state.get('review_feedback', '')}")

    if st.button("Regenerate with Feedback"):
        state["review_feedback"] = feedback
        state.update(human_review(state))
        st.session_state.state = state
        st.session_state.active_tab = "Design Project"
        st.rerun()

    if st.button("Approve Design"):
        state["approved"] = True
        st.session_state.state = state
        st.session_state.active_tab = "Generate Code"
        st.rerun()

elif st.session_state.active_tab == "Generate Code":
    render_step("Generated Code", "code", generate_code, "Code Review")

elif st.session_state.active_tab == "Code Review":
    render_step("Code Review Summary", "code_review", review_code, "Security Recommendation")

elif st.session_state.active_tab == "Security Recommendation":
    render_step("Security Analysis", "security_report", generate_security_recommendation, "Generate Test Cases")

elif st.session_state.active_tab == "Generate Test Cases":
    render_step("Generated Test Cases", "test_cases", generate_test_cases, "Test Case Review")

elif st.session_state.active_tab == "Test Case Review":
    st.markdown("## Test Case Review")
    feedback = st.text_area("Feedback Before Regenerating", key="test_case_review_feedback")
    st.markdown(f"System Feedback: {state.get('review_feedback', '')}")

    if st.button("Regenerate Tests"):
        state["review_feedback"] = feedback
        state.update(test_cases_review(state))
        st.session_state.state = state
        st.session_state.active_tab = "Generate Test Cases"
        st.rerun()

    if st.button("Approve Test Cases") or state.get("test_case_retries", 0) >= 2:
        state["approved"] = True
        st.session_state.state = state
        st.session_state.active_tab = "QA Testing"
        st.rerun()

elif st.session_state.active_tab == "QA Testing":
    render_step("QA Execution Results", "qa_results", qa_testing, "QA Testing Review")

elif st.session_state.active_tab == "QA Testing Review":
    st.markdown("## QA Testing Review")
    feedback = st.text_area("Feedback Before Re-running QA", key="qa_testing_review_feedback")
    st.markdown(f"System Feedback: {state.get('review_feedback', '')}")

    if st.button("Regenerate Code"):
        state["review_feedback"] = feedback
        state.update(qa_testing_review(state))
        if not state.get("approved"):
            # go back to code generation if QA fails
            st.session_state.state = state
            st.session_state.active_tab = "Generate Code"
        else:
            st.session_state.state = state
            st.session_state.active_tab = "QA Testing"
        st.rerun()

    if st.button("QA Passed") or state.get("qa_retries", 0) >= 2:
        state["approved"] = True
        st.session_state.state = state
        st.session_state.active_tab = "Deployment"
        st.rerun()

elif st.session_state.active_tab == "Deployment":
    render_step("Deployment Strategy", "deployment_log", deployment, "End")

elif st.session_state.active_tab == "End":
    st.success("SDLC Pipeline Completed")
    if state:
        if st.button("Generate PDF Report"):
            pdf_path = generate_pdf_file(state)
            download_button_from_pdf(pdf_path)
    else:
        st.warning("Project state is empty. Nothing to generate.")
