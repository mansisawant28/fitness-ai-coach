from langchain_ollama import OllamaLLM
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os

def get_llm():
    """
    Smart LLM selector:
    - Local development → Ollama (offline, free)
    - Cloud deployment  → Groq  (online, free)
    This is called a strategy pattern in software engineering.
    """
    deployment = os.getenv("DEPLOYMENT", "local")

    if deployment == "cloud":
        # Groq — for Streamlit Cloud deployment
        print("🌐 Using Groq (cloud mode)")
        llm = ChatGroq(
            model="llama3-8b-8192",   # free and fast on Groq
            temperature=0.7,
            max_tokens=1024,
            api_key=os.getenv("GROQ_API_KEY")
        )
    else:
        # Ollama — for local development
        print("💻 Using Ollama (local mode)")
        llm = OllamaLLM(
            model=os.getenv("OLLAMA_MODEL", "gemma:2b"),
            temperature=0.7,
            num_predict=1024
        )
    return llm

# ── Workout plan prompt ────────────────────────────────────────────
WORKOUT_PROMPT = PromptTemplate(
    input_variables=[
        "age", "gender", "weight", "height", "bmi",
        "goal", "experience", "activity_level",
        "equipment", "injuries", "target_calories"
    ],
    template="""
You are an expert fitness coach with 10 years of experience.
Create a detailed, personalized weekly workout plan for this person:

PROFILE:
- Age: {age} years old
- Gender: {gender}
- Weight: {weight} kg | Height: {height} cm | BMI: {bmi}
- Fitness Goal: {goal}
- Experience Level: {experience}
- Activity Level: {activity_level}
- Available Equipment: {equipment}
- Injuries/Limitations: {injuries}
- Daily Calorie Target: {target_calories} kcal

Create a WEEKLY WORKOUT PLAN with:
1. Training schedule (which days to train and rest)
2. For each training day:
   - Workout name and focus (e.g. Push Day, Leg Day)
   - List of exercises with sets, reps, and rest time
   - Estimated duration
3. Warm-up and cool-down routine
4. One specific tip for their goal

Keep it practical, safe, and tailored to their equipment and experience.
Format it clearly with sections and bullet points.
"""
)

# ── Nutrition prompt ───────────────────────────────────────────────
NUTRITION_PROMPT = PromptTemplate(
    input_variables=[
        "age", "gender", "weight", "height",
        "goal", "activity_level", "target_calories",
        "experience"
    ],
    template="""
You are an expert nutritionist and dietitian.
Create a personalized nutrition guide for this person:

PROFILE:
- Age: {age} years old
- Gender: {gender}
- Weight: {weight} kg | Height: {height} cm
- Fitness Goal: {goal}
- Activity Level: {activity_level}
- Daily Calorie Target: {target_calories} kcal
- Experience Level: {experience}

Create a NUTRITION GUIDE with:
1. Daily macronutrient targets (protein, carbs, fats in grams)
2. Meal timing recommendations
3. Sample meal plan for one full day:
   - Breakfast
   - Mid-morning snack
   - Lunch
   - Pre-workout meal
   - Post-workout meal
   - Dinner
4. Top 5 food recommendations for their goal
5. Foods to avoid for their goal
6. Hydration recommendation

Keep it practical and easy to follow.
Format it clearly with sections and bullet points.
"""
)

def generate_workout_plan(user_profile: dict) -> str:
    """
    Takes user profile dictionary and returns
    a personalized workout plan as a string.
    """
    llm = get_llm()
    chain = WORKOUT_PROMPT | llm

    response = chain.invoke({
        "age":              user_profile["age"],
        "gender":           user_profile["gender"],
        "weight":           user_profile["weight"],
        "height":           user_profile["height"],
        "bmi":              user_profile["bmi"],
        "goal":             user_profile["goal"],
        "experience":       user_profile["experience"],
        "activity_level":   user_profile["activity_level"],
        "equipment":        ", ".join(user_profile["equipment"]) if user_profile["equipment"] else "No equipment",
        "injuries":         user_profile["injuries"] if user_profile["injuries"] else "None",
        "target_calories":  user_profile["target_calories"]
    })

    # Groq returns an object, Ollama returns a string
    # This handles both cases cleanly
    if hasattr(response, "content"):
        return response.content
    return response

def generate_nutrition_plan(user_profile: dict) -> str:
    """
    Takes user profile dictionary and returns
    a personalized nutrition guide as a string.
    """
    llm = get_llm()
    chain = NUTRITION_PROMPT | llm

    response = chain.invoke({
        "age":              user_profile["age"],
        "gender":           user_profile["gender"],
        "weight":           user_profile["weight"],
        "height":           user_profile["height"],
        "goal":             user_profile["goal"],
        "activity_level":   user_profile["activity_level"],
        "target_calories":  user_profile["target_calories"],
        "experience":       user_profile["experience"]
    })

    if hasattr(response, "content"):
        return response.content
    return response