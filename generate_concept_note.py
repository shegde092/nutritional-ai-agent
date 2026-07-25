from fpdf import FPDF

class ConceptNotePDF(FPDF):
    def header(self):
        # Emerald Green banner for SDG 3
        self.set_fill_color(16, 185, 129)
        self.rect(0, 0, 210, 20, "F")
        
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 6, "PROJECT CONCEPT NOTE", 0, 1, "C")
        self.set_font("Helvetica", "I", 9)
        self.cell(0, 4, "Nutritional AI Agent | Aligned with UN Sustainable Development Goal 3", 0, 1, "C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

def create_concept_note():
    pdf = ConceptNotePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Metadata Block
    pdf.set_fill_color(248, 250, 252) # Slate 50
    pdf.rect(10, 25, 190, 34, "F")
    pdf.set_xy(12, 27)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(15, 23, 42) # Slate 900
    pdf.cell(0, 5, "PROJECT METADATA", 0, 1)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 5, "Project Title: Nutritional AI Agent", 0, 1)
    pdf.cell(0, 5, "Authors: soujanya k hegde and mohammed umar F", 0, 1)
    pdf.cell(0, 5, "College: cambridge institue of technology", 0, 1)
    pdf.cell(0, 5, "Goal Chosen: UN Sustainable Development Goal 3 (Good Health and Well-being)", 0, 1)
    pdf.ln(10)
    
    sections = [
        ("1. Executive Summary", 
         "The Nutritional AI Agent is an autonomous, conversational diet-planning system designed to provide personalized, healthy recipe suggestions and macronutrient calculations. Built on top of Streamlit, LangGraph, and LangChain, and powered by the Groq API (llama-3.3-70b-versatile), this agent acts as a stateful nutrition researcher and copywriter, mapping out custom nutritional needs dynamically to democratize access to dietetic healthcare."),
        
        ("2. Problem Statement", 
         "Traditional diet tracking relies heavily on manual calorie logging which has high user friction and failure rates. Standard calorie apps do not generate optimal, customized meal suggestions but merely record historical intake. The lack of scalable, automated, and context-specific nutrition guidance prevents individuals from effectively managing metabolic goals, contributing to global obesity and diabetes rates (critical indicators under UN SDG 3)."),
        
        ("3. Project Objectives", 
         "- Automate personalized dietary planning by extracting metabolic user features (Age, Weight, Goal, Restrictions) in real-time.\n"
         "- Implement a sequential, multi-agent state graph (LangGraph) to safely decouple the nutritional research phase from the content formatting phase.\n"
         "- Leverage the Groq Llama 3 model to generate optimal daily meal plans, complete with step-by-step recipes and a macronutrient target summary table.\n"
         "- Design a highly responsive Streamlit user interface featuring premium, responsive CSS styles."),
        
        ("4. System Architecture & Methodology", 
         "The system is built as a stateful multi-agent system:\n"
         "- State Memory: A LangGraph TypedDict manages user physical parameters, raw recipes, and final formatted outputs.\n"
         "- Extraction Agent (Node 1): Gathers user features and queries Groq to draft a detailed calorie and meal plan.\n"
         "- Formatting Agent (Node 2): Takes the raw draft and structures it into Breakfast, Lunch, Dinner, and daily macro tables.\n"
         "- UI Wrapper: Streamlit hosts the sidebar inputs and renders the formatted markdown output with custom CSS."),
        
        ("5. SDG 3 Alignment & Expected Impact", 
         "By automating expert-level dietary planning, this project directly supports UN Sustainable Development Goal 3 (Good Health and Well-being). It increases nutrition literacy, reduces the financial barrier to nutritional advice, and supports preventative care by helping users prevent obesity-related and cardiovascular conditions. The solution is highly scalable and non-invasive, allowing users worldwide to optimize their eating habits autonomously."),
        
        ("6. Future Scope", 
         "Future enhancements will involve integrating wearable devices (e.g., Fitbit, Apple Watch) to import active caloric expenditure, utilizing Vision LLMs to allow users to upload photos of their meals for automated ingredient extraction, and expanding Watson Studio analytics to train custom metabolic rate prediction models.")
    ]
    
    for title, text in sections:
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(16, 185, 129)
        pdf.cell(0, 6, title, 0, 1)
        
        pdf.set_font("Helvetica", "", 9.5)
        pdf.set_text_color(51, 65, 85)
        pdf.multi_cell(0, 5, text)
        pdf.ln(4)
        
    pdf.output("Concept_Note.pdf")
    print("Concept_Note.pdf successfully generated.")

if __name__ == "__main__":
    create_concept_note()
