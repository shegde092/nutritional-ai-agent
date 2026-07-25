import sys
from fpdf import FPDF

class LeanCanvasPDF(FPDF):
    def header(self):
        # Header banner at the top of the canvas
        self.set_fill_color(15, 23, 42) # Dark Slate
        self.rect(10, 8, 277, 12, "F")
        
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 11)
        self.set_xy(10, 8)
        self.cell(277, 12, "LEAN CANVAS: NUTRITIONAL AI AGENT (SDG 3)", 0, 0, "C")

    def footer(self):
        self.set_y(-10)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 116, 139)
        self.cell(0, 10, "IBM SkillsBuild Project Delivery | Aligned with UN Sustainable Development Goal 3 (Good Health and Well-being)", 0, 0, "C")

def draw_box(pdf, title, subtitle, content, x, y, w, h):
    # Draw outer box
    pdf.set_draw_color(16, 185, 129) # SDG 3 Green (Emerald)
    pdf.set_line_width(0.3)
    pdf.rect(x, y, w, h)
    
    # Draw Title Area Background
    pdf.set_fill_color(240, 253, 250) # Light Mint / Emerald tint
    pdf.rect(x + 0.1, y + 0.1, w - 0.2, 6, "F")
    
    # Render Title Text
    pdf.set_xy(x + 2, y + 1)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(15, 118, 110) # Dark Teal
    pdf.cell(w - 4, 4, title, 0, 1)
    
    # Render Subtitle
    if subtitle:
        pdf.set_xy(x + 2, y + 5)
        pdf.set_font("Helvetica", "I", 6.5)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(w - 4, 3, subtitle, 0, 1)
        content_y = y + 9
    else:
        content_y = y + 7
        
    # Render Content Text
    pdf.set_xy(x + 2, content_y)
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(15, 23, 42) # Slate-900
    pdf.multi_cell(w - 4, 4.2, content)

def generate_lean_canvas():
    # Landscape A4 size: 297mm wide x 210mm high
    pdf = LeanCanvasPDF(orientation="L", unit="mm", format="A4")
    pdf.set_margins(10, 10, 10)
    pdf.set_auto_page_break(auto=False)
    pdf.add_page()
    
    # Width of each main column
    # Total width = 277mm (297 - 20)
    col_w = 55.4 
    
    # Column 1
    draw_box(pdf, "PROBLEM", "List your top 1-3 problems", 
             "Manual, time-consuming dietary tracking lacking personalized guidance.", 
             10, 22, col_w, 62.5)
    draw_box(pdf, "EXISTING ALTERNATIVES", "How these problems are solved today", 
             "Standard calorie apps (MyFitnessPal), manual web searches.", 
             10, 84.5, col_w, 62.5)
             
    # Column 2
    draw_box(pdf, "SOLUTION", "Outline a possible solution for each problem", 
             "Autonomous LangGraph AI agent generating customized meal plans.", 
             65.4, 22, col_w, 62.5)
    draw_box(pdf, "KEY METRICS", "List the key numbers that tell you how your business is doing", 
             "Daily active users, recipe generation success rate, user retention.", 
             65.4, 84.5, col_w, 62.5)
             
    # Column 3
    draw_box(pdf, "UNIQUE VALUE PROPOSITION", "Single, clear, compelling message of difference", 
             "Fully automated end-to-end dietary planning - from metric analysis to structured meals.", 
             120.8, 22, col_w, 62.5)
    draw_box(pdf, "HIGH-LEVEL CONCEPT", "List your X for Y analogy", 
             "An AI nutritionist that builds your meals for you.", 
             120.8, 84.5, col_w, 62.5)
             
    # Column 4
    draw_box(pdf, "UNFAIR ADVANTAGE", "Something that cannot easily be bought or copied", 
             "Proprietary stateful AI workflow integration.", 
             176.2, 22, col_w, 62.5)
    draw_box(pdf, "CHANNELS", "List your path to customers", 
             "App stores, health clubs, student networks.", 
             176.2, 84.5, col_w, 62.5)
             
    # Column 5
    draw_box(pdf, "CUSTOMER SEGMENTS", "List your target customers and users", 
             "Health-conscious individuals, fitness enthusiasts, dietitians.", 
             231.6, 22, col_w, 62.5)
    draw_box(pdf, "EARLY ADOPTERS", "The characteristics of your ideal customers", 
             "Tech-savvy college students.", 
             231.6, 84.5, col_w, 62.5)
             
    # Bottom Row (Cost & Revenue) - Width = 138.5mm each
    draw_box(pdf, "COST STRUCTURE", "List your fixed and variable costs", 
             "LLM API costs (Groq), cloud hosting, system maintenance, and API key monitoring.", 
             10, 147, 138.5, 40)
    draw_box(pdf, "REVENUE STREAMS", "List your sources of revenue", 
             "Freemium model (free basic meal lists, premium dynamic clinical nutrition audits).", 
             148.5, 147, 138.5, 40)
             
    pdf.output("Lean_Canvas.pdf")
    print("Lean_Canvas.pdf successfully written in landscape grid layout.")

if __name__ == "__main__":
    generate_lean_canvas()
