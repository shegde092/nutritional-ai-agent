import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file if available
load_dotenv()

from src.graph import get_nutrition_graph

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
    try:
        if "GROQ_API_KEY" in st.secrets:
            candidate_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        pass

    if not candidate_key:
        candidate_key = os.environ.get("GROQ_API_KEY")
        
    # Ignore empty or placeholder values
    if candidate_key and "YOUR_GROQ" not in candidate_key and candidate_key.strip() != "":
        st.session_state["groq_api_key"] = candidate_key
        os.environ["GROQ_API_KEY"] = candidate_key

# Define a helper variable for nodes to access
groq_api_key = st.session_state["groq_api_key"]


# 3. Streamlit User Interface
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
            os.environ["GROQ_API_KEY"] = temp_key
            st.success("API key loaded for this session! Click 'Generate Meal Plan' again.")
            st.rerun()
        else:
            st.warning("Please configure `GROQ_API_KEY` in your `.env` file, `.streamlit/secrets.toml`, or paste it above to run the generator.")
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
        
        # Compile the graph from src/graph.py
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
