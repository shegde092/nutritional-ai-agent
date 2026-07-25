import sys
from fpdf import FPDF

class ConceptNotePDF(FPDF):
    def header(self):
        # Header banner at the top of each page (matching style)
        self.set_fill_color(16, 185, 129) # SDG 3 Green (Emerald)
        self.rect(0, 0, 210, 20, "F")
        
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 13)
        self.set_xy(10, 5)
        self.cell(0, 10, "CONCEPT NOTE: NUTRITIONAL AI AGENT (SDG 3)", 0, 1, "C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 116, 139)
        self.cell(0, 10, f"Page {self.page_no()} | IBM SkillsBuild Deliverable", 0, 0, "C")

def create_concept_note():
    pdf = ConceptNotePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # 1. Project Title
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(16, 185, 129)
    pdf.cell(0, 8, "1. Project Overview", 0, 1)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(55, 65, 81)
    overview_text = (
        "- Project Name: Nutritional AI Agent\n"
        "- Core Scope: Autonomous and personalized daily dietary planning and recipes.\n"
        "- UN SDG Alignment: Goal 3 (Good Health and Well-being).\n"
        "- Technologies: Streamlit, LangGraph (StateGraph), LangChain, Groq API (Llama 3.3 70B)."
    )
    pdf.multi_cell(0, 5, overview_text)
    pdf.ln(4)
    
    # 2. Introduction & Background
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(16, 185, 129)
    pdf.cell(0, 8, "2. Introduction & Relevance to SDG 3", 0, 1)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(55, 65, 81)
    intro_text = (
        "Good Health and Well-being (UN SDG 3) emphasizes healthy lifestyles and disease mitigation. "
        "Metabolic health is directly determined by dietary intake, yet obesity and malnutrition affect "
        "millions worldwide. Standard tools fail because manual logs require high cognitive friction and "
        "do not provide personalized, context-aware suggestions. This project implements a conversational, "
        "agentic solution that autonomously calculates nutrient requirements and designs complete daily recipe plans."
    )
    pdf.multi_cell(0, 5, intro_text)
    pdf.ln(4)
    
    # 3. Problem Statement & Specific Goals
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(16, 185, 129)
    pdf.cell(0, 8, "3. Problem Statement & System Objectives", 0, 1)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(55, 65, 81)
    problem_text = (
        "- The Objective: Develop an autonomous AI system that extracts personal metabolic metrics (Age, Weight, Goal, Allergies) and compiles highly optimal meal structures.\n"
        "- Specific Technical Goals:\n"
        "  - Automate user feature processing through a secure Streamlit UI sidebar.\n"
        "  - Coordinate nodes in a sequential StateGraph to guarantee clean recipe outputs.\n"
        "  - Format recipes into structured target calorie breakdown tables (Breakfast, Lunch, Dinner)."
    )
    pdf.multi_cell(0, 5, problem_text)
    pdf.ln(4)
    
    # 4. Methodology & Solution Architecture
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(16, 185, 129)
    pdf.cell(0, 8, "4. Technical Methodology & Solution Architecture", 0, 1)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(55, 65, 81)
    architecture_text = (
        "The system utilizes a modern agentic AI architecture with a sequential dual-agent LangGraph workflow:\n"
        "1. User Interface (Streamlit): Collects physical parameters and fitness targets safely in the sidebar.\n"
        "2. State Management (TypedDict): Passes feature attributes dynamically across nodes.\n"
        "3. Extraction Node (Dietary Researcher): Prompts Groq API (llama-3.3-70b-versatile) to run clinical diet research and output ingredients, portion sizes, and health rationales.\n"
        "4. Formatting Node (Content Writer): Re-writes raw text into clean, markdown-compliant tables.\n"
        "5. Output Render: Main content area updates asynchronously showing the complete recipes."
    )
    pdf.multi_cell(0, 5, architecture_text)
    pdf.ln(4)
    
    # 5. Tools and Future Scope
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(16, 185, 129)
    pdf.cell(0, 8, "5. Development Tools & Future Scope", 0, 1)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(55, 65, 81)
    future_text = (
        "- Core Stack: Python, Streamlit, LangGraph, LangChain, Groq API (Llama 3.3 70B).\n"
        "- IBM Cloud & Watson Integration Concept: Uses IBM Cloud Code Engine for serverless Streamlit hosting and IBM Cloud Object Storage for logging recipes.\n"
        "- Future Work: Integrate wearable sensors (e.g. Fitbit/Apple Watch) for dynamic heart-rate/activity-adjusted calorie models, use Vision LLMs to log meal photographs, and train Watson Studio predictors for custom BMR estimation."
    )
    pdf.multi_cell(0, 5, future_text)
    
    pdf.output("Concept_Note.pdf")
    print("Concept_Note.pdf successfully generated.")

if __name__ == "__main__":
    create_concept_note()
