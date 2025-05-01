import streamlit as st
import streamlit.components.v1 as components

from state import ThinkDeployState
from graph import build_graph
from utils import generate_pdf_file, download_button_from_pdf

# Node imports
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

# Set up page
st.set_page_config(
    page_title="ThinkDeploy | Software Lifecycle Automation",
    layout="wide",
    initial_sidebar_state="expanded"
)

steps = [
    "Workflow Diagram", "Project Setup", "User Story", "Design", "Generate Code",
    "Code Review", "Security Recommendation", "Security Review",
    "Test Cases", "Test Case Review", "QA Testing", "QA Testing Review",
    "Deployment", "End"
]

if "state" not in st.session_state:
    st.session_state.state = None
if "active_tab" not in st.session_state:
    st.session_state.active_tab = steps[0]

state = st.session_state.state

st.sidebar.title("ThinkDeploy")
st.sidebar.subheader("Workflow Navigation")
st.session_state.active_tab = st.sidebar.radio("Select step", steps, index=steps.index(st.session_state.active_tab))

def show_workflow_diagram():
    graph = build_graph()
    mermaid_code = graph.get_graph().draw_mermaid()

    html = f"""
    <div class="mermaid">
    {mermaid_code}
    </div>
    <script type="module">
      import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
      mermaid.initialize({{ startOnLoad: true }});
    </script>
    """
    components.html(html, height=600, scrolling=True)

def approve_and_advance(next_tab):
    st.session_state.active_tab = next_tab
    st.rerun()

def render_section(state, title, field_name, generator_fn, feedback_key, next_tab=None):
    st.title(title)
    if not getattr(state, field_name):
        state = generator_fn(state)
        st.session_state.state = state

    st.subheader("Generated Output")
    st.markdown(getattr(state, field_name), unsafe_allow_html=True)
    feedback = st.text_area("Provide feedback to regenerate", key=feedback_key)

    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("Regenerate with Feedback", key=f"{feedback_key}_regen"):
            if feedback.strip():
                updated_state = state.model_copy(update={f"{feedback_key}_feedback": feedback})
                updated_state = generator_fn(updated_state)
                updated_state = updated_state.model_copy(update={f"{feedback_key}_feedback": ""})
                st.session_state.state = updated_state
                st.rerun()
    with col2:
        if next_tab and st.button("Approve and Continue", key=f"{feedback_key}_approve"):
            st.session_state.state = state
            approve_and_advance(next_tab)

    return state

# Step pages
if st.session_state.active_tab == "Workflow Diagram":
    st.title("Visual Workflow: ThinkDeploy SDLC")
    st.caption("Below is a live agent-based LangGraph workflow diagram.")
    show_workflow_diagram()

elif st.session_state.active_tab == "Project Setup":
    st.title("Project Setup")
    project_name = st.text_input("Project Name")
    requirements = st.text_area("Project Requirements")
    if st.button("Start Project"):
        state = ThinkDeployState(project_name=project_name.strip(), requirements=requirements.strip())
        st.session_state.state = state
        approve_and_advance("User Story")

elif st.session_state.active_tab == "User Story":
    state = render_section(state, "User Story", "user_stories", generate_user_stories, "user_story", "Design")

elif st.session_state.active_tab == "Design":
    state = render_section(state, "Design Document", "design_doc", design_project, "design", "Generate Code")

elif st.session_state.active_tab == "Generate Code":
    state = render_section(state, "Generated Code", "generated_code", generate_code, "code", "Code Review")

elif st.session_state.active_tab == "Code Review":
    state = render_section(state, "Code Review", "code_review", review_code, "code_review", "Security Recommendation")

elif st.session_state.active_tab == "Security Recommendation":
    state = render_section(state, "Security Recommendations", "security_guidelines", generate_security_recommendation, "security", "Security Review")

elif st.session_state.active_tab == "Security Review":
    state = render_section(state, "Security Review", "security_review", security_review, "security_review", "Test Cases")

elif st.session_state.active_tab == "Test Cases":
    state = render_section(state, "Test Case Generation", "test_cases", generate_test_cases, "test_cases", "Test Case Review")

elif st.session_state.active_tab == "Test Case Review":
    state = render_section(state, "Test Case Review", "test_cases_review", test_cases_review, "test_case_review", "QA Testing")

elif st.session_state.active_tab == "QA Testing":
    state = render_section(state, "QA Testing", "qa_results", qa_testing, "qa", "QA Testing Review")

elif st.session_state.active_tab == "QA Testing Review":
    st.title("QA Testing Review")
    if state.qa_results and not state.qa_review:
        state = qa_testing_review(state)
        st.session_state.state = state

    st.markdown(state.qa_review)
    feedback = st.text_area("QA Feedback", key="qa_review")
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("QA Failed – Return to Code"):
            state.qa_approved = False
            st.session_state.state = state
            approve_and_advance("Generate Code")
    with col2:
        if st.button("QA Passed – Continue"):
            state.qa_approved = True
            st.session_state.state = state
            approve_and_advance("Deployment")

elif st.session_state.active_tab == "Deployment":
    state = render_section(state, "Deployment Plan", "deployment_plan", deployment, "deployment", "End")

elif st.session_state.active_tab == "End":
    st.title("Project Complete")
    st.success("The full software lifecycle is complete.")

    if state.project_name:
        pdf_path = generate_pdf_file(
            project_name=state.project_name,
            requirements=state.requirements,
            user_stories=state.user_stories,
            design_doc=state.design_doc,
            generated_code=state.generated_code,
            code_review=state.code_review,
            security_guidelines=state.security_guidelines,
            security_review=state.security_review,
            test_cases=state.test_cases,
            test_cases_review=state.test_cases_review,
            qa_results=state.qa_results,
            qa_review=state.qa_review,
            deployment_plan=state.deployment_plan
        )
        st.subheader("Download Project Report")
        download_button_from_pdf(pdf_path)
