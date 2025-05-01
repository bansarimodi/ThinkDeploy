import streamlit as st
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

# Configure Streamlit
st.set_page_config(
    page_title="ThinkDeploy | Software Lifecycle Automation",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Centered Title 
st.markdown("""
    <h1 style="
        text-align: left;
        font-size: 3rem;
        font-weight: 800;
        color: #1f2937;
        margin-top: 0;
        margin-bottom: 0.4rem;
    ">ThinkDeploy</h1>

    <p style="
        text-align: left;
        font-size: 1.5rem;
        color: #4b5563;
        margin: 0;
        padding-bottom: 1.5rem;
    ">The AI Software Architect That Builds It All</p>
""", unsafe_allow_html=True)

# Custom styling
st.markdown("""
    <style>
        .block-container {
            padding: 2rem 4rem;
        }

        .stTextInput > div > input,
        .stTextArea > div > textarea {
            background-color: #f9fafb;
            border-radius: 0.5rem;
            border: 1px solid #ddd;
            padding: 0.75rem;
            font-size: 1rem;
        }

        .stButton > button {
            background-color: #2e7d32;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            transition: 0.3s;
        }

        .stButton > button:hover {
            background-color: #1b5e20;
        }

        .stTextArea label, .stTextInput label {
            font-weight: 600;
            color: #333333;
        }
    </style>
""", unsafe_allow_html=True)

# Steps
steps = [
    "Project Setup", "User Story", "Design", "Generate Code", "Code Review",
    "Security Recommendation", "Security Review", "Test Cases",
    "Test Case Review", "QA Testing", "QA Testing Review", "Deployment", "End"
]

if "state" not in st.session_state:
    st.session_state.state = None
if "active_tab" not in st.session_state:
    st.session_state.active_tab = steps[0]

state = st.session_state.state

# Sidebar Navigation

st.sidebar.subheader("Navigation")
st.session_state.active_tab = st.sidebar.radio("Step", steps, index=steps.index(st.session_state.active_tab))

def approve_and_advance(next_tab):
    st.session_state.active_tab = next_tab
    st.rerun()

def render_section(state, title, field_name, generator_fn, feedback_key, next_tab=None):
    st.subheader(title)
    if not getattr(state, field_name):
        state = generator_fn(state)
        st.session_state.state = state

    st.markdown(getattr(state, field_name), unsafe_allow_html=True)
    feedback = st.text_area("Feedback", key=feedback_key)

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

# Routing
if st.session_state.active_tab == "Project Setup":
    st.subheader("Project Setup")
    project_name = st.text_input("Project Name", value=state.project_name if state else "")
    requirements = st.text_area("Project Requirements", value=state.requirements if state else "")
    if st.button("Start Project"):
        state = ThinkDeployState(project_name=project_name.strip(), requirements=requirements.strip())
        st.session_state.state = state
        approve_and_advance("User Story")

elif st.session_state.active_tab == "User Story":
    state = render_section(state, "User Story", "user_stories", generate_user_stories, "user_story", "Design")

elif st.session_state.active_tab == "Design":
    state = render_section(state, "Design", "design_doc", design_project, "design", "Generate Code")

elif st.session_state.active_tab == "Generate Code":
    state = render_section(state, "Generate Code", "generated_code", generate_code, "code", "Code Review")

elif st.session_state.active_tab == "Code Review":
    state = render_section(state, "Code Review", "code_review", review_code, "code_review", "Security Recommendation")

elif st.session_state.active_tab == "Security Recommendation":
    state = render_section(state, "Security Recommendation", "security_guidelines", generate_security_recommendation, "security", "Security Review")

elif st.session_state.active_tab == "Security Review":
    state = render_section(state, "Security Review", "security_review", security_review, "security_review", "Test Cases")

elif st.session_state.active_tab == "Test Cases":
    state = render_section(state, "Test Cases", "test_cases", generate_test_cases, "test_cases", "Test Case Review")

elif st.session_state.active_tab == "Test Case Review":
    state = render_section(state, "Test Case Review", "test_cases_review", test_cases_review, "test_case_review", "QA Testing")

elif st.session_state.active_tab == "QA Testing":
    state = render_section(state, "QA Testing", "qa_results", qa_testing, "qa", "QA Testing Review")

elif st.session_state.active_tab == "QA Testing Review":
    st.subheader("QA Testing Review")
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
    st.subheader("Project Complete")
    st.success("The software lifecycle is complete. Download your project report below.")

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
        st.subheader("Download Final Report")
        download_button_from_pdf(pdf_path)
