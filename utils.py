from fpdf import FPDF
import streamlit as st
import os
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 14)
        self.cell(0, 10, "Software Development Lifecycle Report", ln=True, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')


def sanitize_text(text: str) -> str:
    """Remove any non-latin1 characters (like emojis)"""
    return ''.join(c for c in text if ord(c) < 256)


def generate_pdf_file(state):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    def write_section(title, content):
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, sanitize_text(title), ln=True)
        pdf.set_font("Arial", "", 12)
        for line in sanitize_text(content or "").split("\n"):
            pdf.multi_cell(0, 8, line)
        pdf.ln(5)

    write_section("Project Name", state.get("project_name", "N/A"))
    write_section("Requirements", state.get("requirements", "N/A"))
    write_section("User Story", state.get("user_story", "N/A"))
    write_section("Design Document", state.get("design_doc", "N/A"))
    write_section("Code", state.get("code", "N/A"))
    write_section("Code Review", state.get("code_review", "N/A"))
    write_section("Security Report", state.get("security_report", "N/A"))
    write_section("Test Cases", state.get("test_cases", "N/A"))
    write_section("QA Results", state.get("qa_results", "N/A"))
    write_section("Deployment Log", state.get("deployment_log", "N/A"))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"report_{timestamp}.pdf"
    pdf.output(output_path)
    return output_path


def download_button_from_pdf(file_path):
    with open(file_path, "rb") as f:
        pdf_data = f.read()
    st.download_button(
        label="⬇️ Download Report PDF",
        data=pdf_data,
        file_name=os.path.basename(file_path),
        mime="application/pdf"
    )
