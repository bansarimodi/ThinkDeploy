from fpdf import FPDF
import base64
import streamlit as st
import tempfile
import os
import re

# Utility: Remove emojis or non-ASCII characters
def remove_emojis(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

# PDF Generator Class
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 18)
        self.set_text_color(60, 60, 60)
        self.cell(0, 12, "ThinkDeploy Project Report", ln=True, align="C")
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 10)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_section(self, title, content):
        self.set_text_color(0, 102, 204)
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, f"{title}:", ln=True)
        self.set_text_color(0, 0, 0)
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 8, content.strip())
        self.ln(5)

    def add_table(self, title, headers, rows):
        self.set_text_color(0, 102, 204)
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, f"{title}:", ln=True)

        self.set_fill_color(230, 230, 250)
        self.set_text_color(0)
        self.set_font("Arial", "B", 12)

        total_width = self.w - 2 * self.l_margin
        col_widths = [total_width / len(headers)] * len(headers)

        # Table headers
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 10, header, border=1, fill=True, align="C")
        self.ln()

        self.set_font("Arial", "", 11)
        for row in rows:
            for i in range(len(headers)):
                self.cell(col_widths[i], 10, row[i], border=1)
            self.ln()
        self.ln(5)

# PDF Export Function
def generate_pdf_file(
    project_name,
    requirements,
    user_stories,
    design_doc,
    generated_code="",
    code_review="",
    security_guidelines="",
    security_review="",
    test_cases="",
    test_cases_review="",
    qa_results="",
    qa_review="",
    deployment_plan=""
):
    pdf = PDF()
    pdf.add_page()

    # Clean inputs
    fields = {
        "Project Name": project_name,
        "Requirements": requirements,
        "User Stories": user_stories,
        "Design Document": design_doc,
        "Generated Code": generated_code,
        "Code Review": code_review,
        "Security Guidelines": security_guidelines,
        "Security Review": security_review,
        "Test Cases": test_cases,
        "Test Case Review": test_cases_review,
        "QA Results": qa_results,
        "QA Review": qa_review,
        "Deployment Plan": deployment_plan
    }

    for title, content in fields.items():
        pdf.add_section(title, remove_emojis(content or ""))

    # Add timeline table
    pdf.add_table(
        "Project Timeline",
        headers=["Phase", "Start Date", "End Date"],
        rows=[
            ["Initiation", "2025-05-01", "2025-05-05"],
            ["Design", "2025-05-06", "2025-05-10"],
            ["Development", "2025-05-11", "2025-06-15"],
            ["Testing", "2025-06-16", "2025-06-30"],
            ["Deployment", "2025-07-01", "2025-07-05"]
        ]
    )

    # Add budget table
    pdf.add_table(
        "Budget Estimate",
        headers=["Role", "Headcount", "Monthly Cost ($)"],
        rows=[
            ["Project Manager", "1", "6000"],
            ["Developers", "4", "20000"],
            ["QA Engineers", "2", "8000"],
            ["DevOps Engineer", "1", "5000"],
            ["UX/UI Designer", "1", "4000"]
        ]
    )

    # Save
    file_path = os.path.join(tempfile.gettempdir(), f"{project_name.replace(' ', '_')}_report.pdf")
    pdf.output(file_path)
    return file_path

# Download Button for Streamlit
def download_button_from_pdf(file_path, label="Download Final Report (PDF)"):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
        st.markdown(
            f"""
            <div style="margin-top:20px;">
                <a href="data:application/pdf;base64,{base64_pdf}" download="{os.path.basename(file_path)}" style="
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px 20px;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                ">
                {label}
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )
