generate_user_story_prompt = """
User Story Generation

You are a product manager. Based on the following software requirements, write 5–7 user stories that follow the criteria:

- Independent
- Negotiable
- Valuable
- Estimable
- Small
- Testable

Each user story must be clear and should follow this structure:
As a [type of user], I want to [do something] so that [benefit].

Use bullet points and separate each story with spacing for readability.

Software Requirements:
{requirements}
"""

design_project_prompt = """
System Design Document

You are a senior software architect tasked with creating a detailed technical design for the software solution. This design should be suitable for handoff to an engineering team.

User Story:
{user_story}

Human Feedback (if any):
{feedback}

Provide the following:

1. High-Level Architecture
- Describe system overview, key components, and interactions.

2. System Components (Table)
| Component        | Responsibility                           | Technologies     |
|------------------|-------------------------------------------|------------------|
|                  |                                           |                  |

3. Technology Stack
- Backend: Framework, language
- Frontend: Framework
- Database: Type, rationale
- DevOps: CI/CD, deployment

4. Sequence Flow
- Describe request/response cycle
- Indicate asynchronous operations if applicable

5. Timeline (Estimates)
| Phase          | Description                 | Duration |
|----------------|-----------------------------|----------|
| Design         | Design activities           | 1 week   |
| Development    | Feature implementation      | 2 weeks  |
| QA             | Testing phase               | 1 week   |
| Deployment     | Final deployment & review   | 1 week   |

6. Risk Assessment
| Risk                     | Impact     | Mitigation Strategy         |
|--------------------------|------------|------------------------------|
| API dependency failures  | Medium     | Retry + fallback logic       |
| Security vulnerabilities | High       | Use best practices, scan     |

7. Assumptions & Constraints
- Describe key assumptions (tech availability, team skill, time limits)
- Highlight any constraints
"""

generate_code_prompt = """
Code Implementation

You are a senior backend engineer. Convert the following design into working, clean, well-structured Python code. Prioritize readability, modularity, and robustness.

Design Document:
{design_doc}
"""

review_code_prompt = """
Code Review Summary

Act as a senior code reviewer. Assess the code below based on these 5 categories:
1. Correctness
2. Maintainability
3. Performance
4. Security & Error Handling
5. Suggestions for Improvement

Give structured feedback in bullets.

Code:
{code}
"""

security_review_prompt = """
Security Analysis

Act as an experienced cybersecurity analyst. Review the code below and identify any potential vulnerabilities.

Checklist:
- Input validation
- Authentication / authorization
- Secure data handling
- Use of 3rd party packages
- Known CWE categories

Recommend remediations for each risk.

Code:
{code}
"""

generate_test_cases_prompt = """
Test Case Design

You are a QA engineer. Write a comprehensive suite of unit and edge test cases for the code below.

Provide:
- List of well-named test cases
- A markdown table for coverage
- Note any edge case handling gaps

Code:
{code}
"""

qa_testing_prompt = """
QA Report

Run the test suite and return a QA execution report.

Include:
- Summary of test execution
- Bugs found (if any)
- Pass/fail status

Test Cases:
{test_cases}
"""

deployment_prompt = """
Deployment Plan

You are a DevOps engineer. Prepare a detailed deployment plan based on the final application code.

Include:
- Hosting strategy (cloud / container / VM)
- CI/CD pipeline steps
- Rollback strategy
- Monitoring setup

Application Code:
{code}
"""
