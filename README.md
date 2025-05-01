# ThinkDeploy — The AI Software Architect That Builds It All

**ThinkDeploy** is an AI-powered automation platform that transforms high-level software ideas into complete, deployment-ready solutions. Built with LangGraph and powered by LLaMA 3 via the Groq API, ThinkDeploy mirrors the entire Software Development Life Cycle (SDLC) with human-in-the-loop feedback at every stage.

---

## Features

- Modular agentic AI workflow using LangGraph
- Automatically generates user stories from natural language requirements
- Produces structured design documents with timelines, risk analysis, and resource planning
- Generates Python starter code with separation of concerns
- Conducts LLM-powered code reviews and security audits
- Builds test cases and simulates QA testing
- Includes approval loops and conditional logic (QA pass/fail)
- Exports a final professional-grade PDF report including budget and timeline tables

---

## Tech Stack

| Tool/Library       | Purpose                             |
|--------------------|--------------------------------------|
| LangGraph           | Agent workflow orchestration        |
| LangChain           | Prompt management                   |
| Groq API + LLaMA 3  | High-performance language model     |
| Streamlit           | Interactive user interface          |
| Pydantic            | State/data modeling                 |
| FPDF                | PDF report generation               |
| dotenv              | Environment variable management     |

---

## Workflow Overview

1. Project Setup
2. User Story Generation
3. Design Documentation
4. Code Generation
5. Code Review
6. Security Recommendations
7. Security Review
8. Test Case Generation
9. Test Case Review
10. QA Testing
11. QA Review
12. Deployment Planning
13. Project Completion with PDF export

---

## Installation

### Prerequisites

- Python 3.10+
- Groq API key (get from https://console.groq.com)

Create a `.env` file with:

```env
GROQ_API_KEY=your_groq_key_here
```

### Setup Instructions

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit app:

```bash
streamlit run app.py
```

---

## Project Structure

```
ThinkDeploy/
├── app.py                      # Streamlit UI frontend
├── graph.py                    # LangGraph workflow definition
├── state.py                    # ThinkDeployState (Pydantic state model)
├── utils.py                    # PDF generation and formatting utilities
├── requirements.txt
├── .env.example                # Sample env config
├── llm/
│   └── llm.py                  # Groq LLaMA 3 configuration
├── nodes/
│   ├── user_story.py                   # User story generation
│   ├── user_story_review.py            # Placeholder for user story feedback
│   ├── design_project.py               # Design doc generation (tables + markdown)
│   ├── review_doc.py                   # Placeholder for design doc feedback
│   ├── generate_code.py                # Initial code generation (Python)
│   ├── review_code.py                  # Code review logic
│   ├── generate_security_recommendation.py  # Static security guideline generation
│   ├── security_review.py              # Security audit feedback
│   ├── generate_test_cases.py          # Functional and edge case generation
│   ├── test_cases_review.py            # Review of generated test cases
│   ├── qa_testing.py                   # QA test simulation by LLM
│   ├── qa_testing_review.py           # QA approval (loop-back if failed)
│   ├── deployment.py                  # CI/CD and infra deployment plan
│   └── end.py                         # Final end step of the workflow
```

---

## Output

The application generates a final PDF report that includes:

- Requirements summary
- User stories and design documentation
- Generated source code
- Code review and security analysis
- Test cases and QA results
- Deployment plan
- Timeline and budget estimate tables

---
