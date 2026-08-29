import os
from typing import Dict, Any
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from src.state import AgentState


def get_groq_api_key() -> str:
    """
    Retrieves the Groq API key from environment variables or Streamlit session state.
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        try:
            import streamlit as st
            if "groq_api_key" in st.session_state:
                api_key = st.session_state.get("groq_api_key")
        except Exception:
            pass
    return api_key or ""


def invoke_groq_chain(prompt_template, input_data: dict, api_key: str, temperature: float = 0.5):
    """
    Invokes LangChain Groq with fallback across currently supported Groq models.
    """
    candidate_models = [
        "openai/gpt-oss-20b",
        "openai/gpt-oss-120b",
    ]
    last_exception = None
    for model_name in candidate_models:
        try:
            print(f"Trying Groq model: {model_name}")
            llm = ChatGroq(
                model=model_name,
                api_key=api_key,
                temperature=temperature,
            )
            chain = prompt_template | llm
            response = chain.invoke(input_data)
            print(f"Successfully used: {model_name}")
            return response
        except Exception as e:
            last_exception = e
            err_str = str(e).lower()
            print(f"Model {model_name} failed: {e}")
            # Only fall back for model availability/deprecation problems
            if any(keyword in err_str for keyword in [
                "model_not_found", "model_decommissioned", "decommissioned",
                "no longer supported", "does not exist", "404", "not found",
            ]):
                continue
            # Authentication, rate-limit, or other hard failures — stop immediately
            break
    raise last_exception


def extraction_agent_node(state: AgentState) -> Dict[str, Any]:
    """
    Node 1: Extraction Agent
    Acts as a professional dietary researcher to generate a nutritional recipe.
    """
    api_key = get_groq_api_key()
    if not api_key:
        return {"raw_recipe": "ERROR: Groq API Key is not set."}

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", (
            "You are an expert Clinical Nutritionist and Dietary Researcher. "
            "Your task is to design a highly optimal, healthy meal plan for a single day based strictly on the user's metrics: "
            "Age, Weight, Fitness Goal, and Dietary Restrictions. "
            "You must prioritize foods that align with UN Sustainable Development Goal 3 (Good Health and Well-being) "
            "by emphasizing balanced, clean, and nutrient-dense whole foods. "
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

    try:
        response = invoke_groq_chain(
            prompt_template=prompt_template,
            input_data={
                "age": state["age"],
                "weight": state["weight"],
                "goal": state["goal"],
                "dietary_restrictions": state["dietary_restrictions"]
            },
            api_key=api_key,
            temperature=0.5
        )
        return {"raw_recipe": response.content}
    except Exception as e:
        return {"raw_recipe": f"ERROR: Extraction failed due to: {str(e)}"}


def formatting_agent_node(state: AgentState) -> Dict[str, Any]:
    """
    Node 2: Formatting Agent
    Transforms raw research output into a beautifully structured, highly-readable Markdown plan.
    """
    api_key = get_groq_api_key()
    if not api_key:
        return {"formatted_meal_plan": "ERROR: Groq API Key is not set."}

    raw_recipe = state.get("raw_recipe", "")
    if raw_recipe.startswith("ERROR:"):
        return {"formatted_meal_plan": raw_recipe}

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

    try:
        response = invoke_groq_chain(
            prompt_template=prompt_template,
            input_data={"raw_recipe": raw_recipe},
            api_key=api_key,
            temperature=0.2
        )
        return {"formatted_meal_plan": response.content}
    except Exception as e:
        return {"formatted_meal_plan": f"ERROR: Formatting failed due to: {str(e)}"}
