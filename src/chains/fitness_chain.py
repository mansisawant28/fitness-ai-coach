from langchain_ollama import OllamaLLM
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from rag.retriever import retrieve_relevant_content
import os

def get_llm():
    """
    Smart LLM selector — Ollama locally, Groq on cloud.
    """
    deployment = os.getenv("DEPLOYMENT", "local")
    if deployment == "cloud":
        llm = ChatGroq(
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=1024,
            api_key=os.getenv("GROQ_API_KEY")
        )
    else:
        llm = OllamaLLM(
            model=os.getenv("OLLAMA_MODEL", "gemma:2b"),
            temperature=0.7,
            num_predict=1024
        )
    return llm

# ── RAG-powered workout prompt ─────────────────────────────────────
WORKOUT_PROMPT = PromptTemplate(
    input_variables=[
        "age", "gender", "weight", "height", "bmi",
        "goal", "experience", "activity_level",
        "equipment", "injuries", "target_calories",
        "relevant_knowledge"    # ← this is the RAG context
    ],
    template="""
You are an expert fitness coach with 10 years of experience.
Use the following verified fitness knowledge to create an accurate plan:

VERIFIED KNOWLEDGE BASE:
{relevant_knowledge}

Now create a personalized weekly workout plan for:

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
   - Workout name and focus
   - Exercises with sets, reps, and rest time
   - Estimated duration
3. Warm-up and cool-down routine
4. One specific tip based on the verified knowledge above

Base your recommendations on the verified knowledge provided.
Format clearly with sections and bullet points.
"""
)

# ── RAG-powered nutrition prompt ───────────────────────────────────
NUTRITION_PROMPT = PromptTemplate(
    input_variables=[
        "age", "gender", "weight", "height",
        "goal", "activity_level", "target_calories",
        "experience", "relevant_knowledge"
    ],
    template="""
You are an expert nutritionist and dietitian.
Use the following verified nutrition knowledge to create an accurate guide:

VERIFIED KNOWLEDGE BASE:
{relevant_knowledge}

Now create a personalized nutrition guide for:

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
3. Sample meal plan for one full day
4. Top 5 food recommendations for their goal
5. Foods to avoid
6. Hydration recommendation

Base your recommendations on the verified knowledge provided.
Format clearly with sections and bullet points.
"""
)

def generate_workout_plan(user_profile: dict) -> str:
    """
    RAG-powered workout plan generation.
    1. Retrieve relevant fitness knowledge
    2. Inject into prompt
    3. Generate personalized plan
    """
    # Step 1 — RAG retrieval
    query = f"{user_profile['goal']} workout plan for {user_profile['experience']} {user_profile['activity_level']}"
    relevant_knowledge = retrieve_relevant_content(query, k=4)

    # Step 2 and 3 — Generate with context
    llm = get_llm()
    chain = WORKOUT_PROMPT | llm

    response = chain.invoke({
        "age":                  user_profile["age"],
        "gender":               user_profile["gender"],
        "weight":               user_profile["weight"],
        "height":               user_profile["height"],
        "bmi":                  user_profile["bmi"],
        "goal":                 user_profile["goal"],
        "experience":           user_profile["experience"],
        "activity_level":       user_profile["activity_level"],
        "equipment":            ", ".join(user_profile["equipment"]) if user_profile["equipment"] else "No equipment",
        "injuries":             user_profile["injuries"] if user_profile["injuries"] else "None",
        "target_calories":      user_profile["target_calories"],
        "relevant_knowledge":   relevant_knowledge    # ← RAG context injected
    })

    if hasattr(response, "content"):
        return response.content
    return response

def generate_nutrition_plan(user_profile: dict) -> str:
    """
    RAG-powered nutrition plan generation.
    """
    # Step 1 — RAG retrieval
    query = f"{user_profile['goal']} nutrition protein calories for {user_profile['experience']}"
    relevant_knowledge = retrieve_relevant_content(query, k=4)

    # Step 2 and 3 — Generate with context
    llm = get_llm()
    chain = NUTRITION_PROMPT | llm

    response = chain.invoke({
        "age":                  user_profile["age"],
        "gender":               user_profile["gender"],
        "weight":               user_profile["weight"],
        "height":               user_profile["height"],
        "goal":                 user_profile["goal"],
        "activity_level":       user_profile["activity_level"],
        "target_calories":      user_profile["target_calories"],
        "experience":           user_profile["experience"],
        "relevant_knowledge":   relevant_knowledge
    })

    if hasattr(response, "content"):
        return response.content
    return response