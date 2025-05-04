from graph import build_graph
from state import SDLCState

# Create a valid initial state
state: SDLCState = {
    "project_name": "Calculator App",
    "requirements": "A basic calculator app that supports +, -, *, / with two numbers.",
    "user_story": None,
    "design_doc": None,
    "code": None,
    "code_review": None,
    "security_report": None,
    "test_cases": None,
    "qa_results": None,
    "deployment_log": None,
    "review_feedback": "",
    "approved": True,
    "test_case_retries": 0,
    "qa_retries": 0
}

# Run the graph
print("🚀 Running ThinkDeploy Pipeline...")
graph = build_graph()
final_state = graph.invoke(dict(state))

# Output results
print("\n✅ Pipeline Complete. Final Results:")
for k, v in final_state.items():
    print(f"\n🔹 {k}:\n{v}")
