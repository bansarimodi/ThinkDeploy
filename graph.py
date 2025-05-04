from langgraph.graph import StateGraph, END
from state import SDLCState, SDLCStateRouter
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
    deployment
)

def build_raw_graph():
    graph = StateGraph(SDLCState)

    graph.add_node("generate_user_story", generate_user_story)
    graph.add_node("design_project", design_project)
    graph.add_node("human_review", human_review)
    graph.add_node("generate_code", generate_code)
    graph.add_node("review_code", review_code)
    graph.add_node("generate_security_recommendation", generate_security_recommendation)
    graph.add_node("generate_test_cases", generate_test_cases)
    graph.add_node("test_cases_review", test_cases_review)
    graph.add_node("qa_testing", qa_testing)
    graph.add_node("qa_testing_review", qa_testing_review)
    graph.add_node("deployment", deployment)

    graph.set_entry_point("generate_user_story")

    graph.add_edge("generate_user_story", "design_project")
    graph.add_edge("design_project", "human_review")
    graph.add_conditional_edges("human_review", lambda state: SDLCStateRouter(state).route("human_review"))
    graph.add_edge("generate_code", "review_code")
    graph.add_edge("review_code", "generate_security_recommendation")
    graph.add_edge("generate_security_recommendation", "generate_test_cases")
    graph.add_edge("generate_test_cases", "test_cases_review")
    graph.add_conditional_edges("test_cases_review", lambda state: SDLCStateRouter(state).route("test_cases_review"))
    graph.add_edge("qa_testing", "qa_testing_review")
    graph.add_conditional_edges("qa_testing_review", lambda state: SDLCStateRouter(state).route("qa_testing_review"))
    graph.add_edge("deployment", END)

    return graph

def build_graph():
    return build_raw_graph().compile()


# 🖼 Render final SDLC diagram with Helvetica + solid lines
if __name__ == "__main__":
    import graphviz

    dot_code = '''
    digraph SDLC {
        rankdir=TB;
        fontname="Helvetica";
        bgcolor=white;

        node [
            shape=box
            style="rounded,filled"
            fontname="Helvetica"
            fontsize=12
            fontcolor=black
            color=black
            penwidth=1.3
        ];

        edge [
            fontname="Helvetica"
            fontsize=11
            color="black"
            style=solid
        ];

        start [label="Start", shape=ellipse, fillcolor="#e3e3e3", style=filled]
        input_requirements [label="Input Requirements", fillcolor="#f8d7da"]
        generate_user_story [label="Generate User Story", fillcolor="#d1ecf1"]
        design_project [label="Design Project", fillcolor="#f8d7da"]
        human_review [label="Human Review", shape=diamond, fillcolor="#d1ecf1", style=filled]
        revise_design [label="Revise Design", fillcolor="#f8d7da"]
        generate_code [label="Generate Code", fillcolor="#d1ecf1"]
        review_code [label="Code Review", fillcolor="#d1ecf1"]
        generate_security_recommendation [label="Security Agent", fillcolor="#f8d7da"]
        generate_test_cases [label="Generate Test Cases", fillcolor="#e2d4f8"]
        test_cases_review [label="Test Case Review (Human)", shape=diamond, fillcolor="#d1ecf1", style=filled]
        qa_testing [label="QA Testing", fillcolor="#e0f2f1"]
        qa_testing_review [label="QA Testing Review (Human)", shape=diamond, fillcolor="#d1ecf1", style=filled]
        deployment [label="Deployment Agent", fillcolor="#fff3cd"]
        end [label="End", shape=ellipse, fillcolor="#e3e3e3", style=filled]

        start -> input_requirements
        input_requirements -> generate_user_story
        generate_user_story -> design_project
        design_project -> human_review

        human_review -> generate_code [label="Approve"]
        human_review -> revise_design [label="Revise"]
        revise_design -> design_project

        generate_code -> review_code
        review_code -> generate_security_recommendation
        generate_security_recommendation -> generate_test_cases
        generate_test_cases -> test_cases_review

        test_cases_review -> generate_test_cases [label="Revise"]
        test_cases_review -> qa_testing [label="Approve"]

        qa_testing -> qa_testing_review
        qa_testing_review -> deployment [label="Approve"]
        qa_testing_review -> generate_code [label="Revise"]

        deployment -> end
    }
    '''

    graph = graphviz.Source(dot_code)
    graph.render("thinkdeploy_sdlc_graph", format="png", cleanup=True)
    print("✅ Diagram saved as: thinkdeploy_sdlc_graph.png with Helvetica and clean edges.")
