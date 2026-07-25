import os
import streamlit as st
from typing import TypedDict, Dict, Any
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# 1. Page Configuration and Custom CSS
st.set_page_config(
    page_title="Nutritional AI Agent | SDG 3",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium UI Styling using Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    /* Apply Font */
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Gradient Title Styling */
    .hero-title {
        background: linear-gradient(135deg, #10B981 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 2.8rem !important;
        margin-bottom: 0.1rem;
    }
    
    /* Subtitle */
    .hero-subtitle {
        color: #6B7280;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Premium Info Card */
    .info-card {
        background: rgba(16, 185, 129, 0.05);
        border: 1px solid rgba(16, 185, 129, 0.15);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 1.5rem;
    }
    
    .info-card h4 {
        color: #10B981;
        margin-top: 0;
        margin-bottom: 8px;
    }
    
    /* Sidebar Styling Override */
    [data-testid="stSidebar"] {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] p {
        color: #E2E8F0;
    }
    
    /* Make buttons pop out */
    .stButton>button {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.8rem;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(16, 185, 129, 0.3);
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
    }
</style>
""", unsafe_allow_html=True)

# 2. API Key Management
if "groq_api_key" not in st.session_state:
    st.session_state["groq_api_key"] = None

# If we don't have it in session state, try reading from secrets / env
if not st.session_state["groq_api_key"]:
    candidate_key = None
    if "GROQ_API_KEY" in st.secrets:
        candidate_key = st.secrets["GROQ_API_KEY"]
    else:
        candidate_key = os.environ.get("GROQ_API_KEY")
        
    # Ignore empty or placeholder values
    if candidate_key and "YOUR_GROQ" not in candidate_key and candidate_key.strip() != "":
        st.session_state["groq_api_key"] = candidate_key

# Define a helper variable for nodes to access
groq_api_key = st.session_state["groq_api_key"]

# 3. LangGraph State Memory Definition
class AgentState(TypedDict):
    age: int
    weight: float
    goal: str
    dietary_restrictions: str
    raw_recipe: str
    formatted_meal_plan: str

# 4. LangGraph Nodes Definition

def extraction_agent_node(state: AgentState) -> Dict[str, Any]:
    """
    Node 1: Extraction Agent
    Acts as a professional dietary researcher to generate a nutritional recipe.
    """
    api_key = st.session_state.get("groq_api_key")
    if not api_key:
        return {"raw_recipe": "ERROR: Groq API Key is not set."}
        
    # Initialize LangChain Groq Chat model
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        api_key=api_key,
        temperature=0.5
    )
    
    # Formulate prompts
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", (
            "You are an expert Clinical Nutritionist and Dietary Researcher. "
            "Your task is to design a highly optimal, healthy meal plan for a single day based strictly on the user's metrics: Age, Weight, Fitness Goal, and Dietary Restrictions. "
            "You must prioritize foods that align with UN Sustainable Development Goal 3 (Good Health and Well-being) by emphasizing balanced, clean, and nutrient-dense whole foods. "
            "Provide clear portions, ingredients, and the scientific rationale for why these choices support their specific fitness goals."
        )),
        ("user", (
            "Create a personalized daily meal recipe plan for this user profile:\n"
            "- Age: {age} years old\n"
            "- Weight: {weight} kg\n"
            "- Fitness Goal: {goal}\n"
            "- Dietary Restrictions: {dietary_restrictions}\n\n"
            "Return a complete breakdown for Breakfast, Lunch, and Dinner with detailed recipes and estimated macronutrients."
        ))
    ])
    
    chain = prompt_template | llm
    
    try:
        response = chain.invoke({
            "age": state["age"],
            "weight": state["weight"],
            "goal": state["goal"],
            "dietary_restrictions": state["dietary_restrictions"]
        })
        return {"raw_recipe": response.content}
    except Exception as e:
        return {"raw_recipe": f"ERROR: Extraction failed due to: {str(e)}"}

def formatting_agent_node(state: AgentState) -> Dict[str, Any]:
    """
    Node 2: Formatting Agent
    Transforms raw research output into a beautifully structured, highly-readable Markdown plan.
    """
    api_key = st.session_state.get("groq_api_key")
    if not api_key:
        return {"formatted_meal_plan": "ERROR: Groq API Key is not set."}
        
    raw_recipe = state.get("raw_recipe", "")
    if raw_recipe.startswith("ERROR:"):
        return {"formatted_meal_plan": raw_recipe}
        
    # Initialize LangChain Groq Chat model
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        api_key=api_key,
        temperature=0.2
    )
    
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", (
            "You are a Senior Technical Writer and Content Designer. "
            "Take the raw meal plan recipe content and structure it into a stunning, user-friendly Markdown document. "
            "Follow this exact structure:\n"
            "1. Main Title: 🥗 Your Personalized UN SDG 3 Nutrition Plan\n"
            "2. **Daily Macronutrient Target Summary**: Format this as a clean markdown table showing Calories, Protein (g), Carbs (g), and Fats (g).\n"
            "3. **Breakfast**, **Lunch**, and **Dinner** sections. For each, show:\n"
            "   - Emojis and engaging names\n"
            "   - Cook/Preparation Time\n"
            "   - Ingredients checklist\n"
            "   - Clean step-by-step instructions\n"
            "4. **Nutrition & Well-being Alignment**: Explain how this plan specifically supports UN SDG 3 (Good Health and Well-being) for their fitness goal."
        )),
        ("user", "Here is the raw meal plan:\n\n{raw_recipe}")
    ])
    
    chain = prompt_template | llm
    
    try:
        response = chain.invoke({"raw_recipe": raw_recipe})
        return {"formatted_meal_plan": response.content}
    except Exception as e:
        return {"formatted_meal_plan": f"ERROR: Formatting failed due to: {str(e)}"}

# 5. Graph Compilation
def get_nutrition_graph():
    # Build LangGraph workflow
    workflow = StateGraph(AgentState)
    
    # Register the nodes
    workflow.add_node("extraction", extraction_agent_node)
    workflow.add_node("formatting", formatting_agent_node)
    
    # Establish sequential flow
    workflow.add_edge(START, "extraction")
    workflow.add_edge("extraction", "formatting")
    workflow.add_edge("formatting", END)
    
    return workflow.compile()

# 6. Streamlit User Interface
def main():
    st.markdown('<h1 class="hero-title">🥗 Nutritional AI Agent</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Promoting Good Health & Well-being (UN SDG 3) through Personalized Nutrition</p>', unsafe_allow_html=True)

    # Informational card introducing UN SDG 3
    st.markdown("""
    <div class="info-card">
        <h4>🌍 UN Sustainable Development Goal 3: Good Health and Well-being</h4>
        <p>This intelligent agent helps optimize your daily food habits using a dual-agent LangGraph workflow. 
        By designing a custom, macronutrient-balanced diet tailored specifically to your age, weight, and fitness targets, 
        it empowers sustainable lifestyle decisions, prevents diet-related diseases, and enhances metabolic health.</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar for User Profiles & Inputs
    st.sidebar.markdown("## 👤 User Profile & Goals")
    
    age = st.sidebar.number_input("Age (years)", min_value=1, max_value=120, value=28, step=1)
    weight = st.sidebar.number_input("Weight (kg)", min_value=10.0, max_value=300.0, value=70.0, step=0.1)
    
    goal = st.sidebar.selectbox(
        "Fitness Goal",
        [
            "Weight Loss & Caloric Deficit",
            "Muscle Gain & Hypertrophy",
            "Maintenance & Lean Muscle Preservation",
            "Cardiovascular Fitness & Endurance",
            "General Well-being & Healthy Ageing"
        ]
    )
    
    dietary_restrictions = st.sidebar.text_input(
        "Dietary Restrictions / Allergies",
        value="None",
        help="Examples: Vegan, Vegetarian, Gluten-Free, Lactose-Intolerant, Keto, Peanut Allergy"
    )
    
    generate_btn = st.sidebar.button("Generate Meal Plan")
    
    # Display warning if Groq API key is missing and offer a text input fallback for easy onboarding
    if not st.session_state.get("groq_api_key"):
        st.info("💡 **API Key Setup Required**")
        temp_key = st.text_input(
            "Groq API Key not detected in environment or secrets. Enter it below to start:", 
            type="password"
        )
        if temp_key:
            st.session_state["groq_api_key"] = temp_key
            st.success("API key loaded for this session! Click 'Generate Meal Plan' again.")
            st.rerun()
        else:
            st.warning("Please configure `GROQ_API_KEY` in your `.streamlit/secrets.toml` file or paste it above to run the generator.")
            st.stop()

    # Main Area Action
    if generate_btn:
        # Construct the initial state
        initial_state = {
            "age": age,
            "weight": weight,
            "goal": goal,
            "dietary_restrictions": dietary_restrictions,
            "raw_recipe": "",
            "formatted_meal_plan": ""
        }
        
        # Compile the graph
        nutrition_graph = get_nutrition_graph()
        
        # Invoke the LangGraph workflow inside a streamlit spinner
        with st.spinner("🧠 Connecting to the Groq Nutrition Analyst & Formatting Agent... Please wait."):
            try:
                final_state = nutrition_graph.invoke(initial_state)
                formatted_plan = final_state.get("formatted_meal_plan", "")
                
                if formatted_plan.startswith("ERROR:"):
                    st.error(formatted_plan)
                else:
                    st.success("🎉 Your Personalized Meal Plan has been generated successfully!")
                    st.markdown(formatted_plan)
            except Exception as e:
                st.error(f"An unexpected error occurred during execution: {str(e)}")
    else:
        st.info("👈 Set your metrics in the sidebar and click **Generate Meal Plan** to run the agentic workflow.")

if __name__ == "__main__":
    main()
