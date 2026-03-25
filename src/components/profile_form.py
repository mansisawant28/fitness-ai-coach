import streamlit as st

def calculate_bmi(weight_kg, height_cm):
    """
    BMI formula = weight(kg) / height(m)²
    We convert height from cm to meters first
    """
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 1)

def get_bmi_category(bmi):
    """Return a label based on BMI value"""
    if bmi < 18.5:
        return "Underweight", "🔵"
    elif bmi < 25:
        return "Normal weight", "🟢"
    elif bmi < 30:
        return "Overweight", "🟡"
    else:
        return "Obese", "🔴"

def calculate_calories(weight, height, age, gender, activity_level):
    """
    Mifflin-St Jeor equation — most accurate calorie formula.
    Calculates BMR (Basal Metabolic Rate) first, then multiplies
    by activity multiplier to get Total Daily Energy Expenditure (TDEE)
    """
    # Step 1: Calculate BMR
    if gender == "Female":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5

    # Step 2: Multiply by activity level
    activity_multipliers = {
        "Sedentary (little or no exercise)":        1.2,
        "Lightly Active (1-3 days/week)":           1.375,
        "Moderately Active (3-5 days/week)":        1.55,
        "Very Active (6-7 days/week)":              1.725,
        "Athlete (twice per day)":                  1.9
    }
    multiplier = activity_multipliers[activity_level]
    tdee = bmr * multiplier
    return round(tdee)

def render_profile_form():
    """
    This is the main function that renders the entire profile form.
    It returns the user's data as a dictionary so other parts
    of the app can use it.
    """

    st.markdown("## 👤 Your Profile")
    st.markdown("Fill in your details to get a fully personalized plan.")
    st.markdown("---")

    # ── Personal details ──────────────────────────────────────────
    st.markdown("### 📋 Personal Details")

    # Two columns side by side
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input(
            "Age",
            min_value=10,
            max_value=100,
            value=25,
            step=1,
            help="Your current age in years"
        )
        height = st.number_input(
            "Height (cm)",
            min_value=100,
            max_value=250,
            value=165,
            step=1,
            help="Your height in centimeters"
        )

    with col2:
        weight = st.number_input(
            "Weight (kg)",
            min_value=30,
            max_value=300,
            value=65,
            step=1,
            help="Your current weight in kilograms"
        )
        gender = st.selectbox(
            "Gender",
            options=["Female", "Male", "Prefer not to say"],
            help="Used for accurate calorie calculations"
        )

    # ── Activity level ────────────────────────────────────────────
    st.markdown("### ⚡ Activity Level")
    activity_level = st.select_slider(
        "How active are you currently?",
        options=[
            "Sedentary (little or no exercise)",
            "Lightly Active (1-3 days/week)",
            "Moderately Active (3-5 days/week)",
            "Very Active (6-7 days/week)",
            "Athlete (twice per day)"
        ],
        value="Lightly Active (1-3 days/week)"
    )

    # ── Fitness goal ──────────────────────────────────────────────
    st.markdown("### 🎯 Your Fitness Goal")

    # Show goals as clickable cards using columns
    goal_col1, goal_col2, goal_col3 = st.columns(3)

    with goal_col1:
        fat_loss = st.button(
            "🔥 Fat Loss\n\nBurn fat, get lean",
            use_container_width=True
        )
    with goal_col2:
        muscle_gain = st.button(
            "💪 Muscle Gain\n\nBuild size and mass",
            use_container_width=True
        )
    with goal_col3:
        strength = st.button(
            "🏆 Strength\n\nGet stronger and powerful",
            use_container_width=True
        )

    # Track which goal is selected using session state
    # session_state is Streamlit's way of remembering values
    # between interactions — like a variable that doesn't reset
    if fat_loss:
        st.session_state["goal"] = "Fat Loss"
    elif muscle_gain:
        st.session_state["goal"] = "Muscle Gain"
    elif strength:
        st.session_state["goal"] = "Strength Building"

    # Show which goal is currently selected
    current_goal = st.session_state.get("goal", "Fat Loss")
    st.success(f"✅ Selected goal: **{current_goal}**")

    # ── Experience level ──────────────────────────────────────────
    st.markdown("### 🎓 Experience Level")
    experience = st.radio(
        "How long have you been training?",
        options=["Beginner (0-1 year)", "Intermediate (1-3 years)", "Advanced (3+ years)"],
        horizontal=True
    )

    # ── Equipment available ───────────────────────────────────────
    st.markdown("### 🏠 Equipment Available")
    equipment = st.multiselect(
        "What equipment do you have access to?",
        options=[
            "No equipment (bodyweight only)",
            "Dumbbells",
            "Barbell + Plates",
            "Resistance Bands",
            "Pull-up Bar",
            "Full Gym Access",
            "Kettlebells"
        ],
        default=["Full Gym Access"]
    )

    # ── Health conditions ─────────────────────────────────────────
    st.markdown("### ⚕️ Any Injuries or Conditions?")
    injuries = st.text_area(
        "List any injuries, conditions or limitations (optional)",
        placeholder="e.g. Lower back pain, bad knees, shoulder injury...",
        height=80
    )

    st.markdown("---")

    # ── Live metrics (calculated instantly) ───────────────────────
    st.markdown("### 📊 Your Stats")

    bmi = calculate_bmi(weight, height)
    bmi_category, bmi_emoji = get_bmi_category(bmi)
    calories = calculate_calories(weight, height, age, gender, activity_level)

    # Adjust calories based on goal
    if current_goal == "Fat Loss":
        target_calories = calories - 400    # caloric deficit
        calorie_note = "(-400 deficit)"
    elif current_goal == "Muscle Gain":
        target_calories = calories + 300    # caloric surplus
        calorie_note = "(+300 surplus)"
    else:
        target_calories = calories          # maintenance for strength
        calorie_note = "(maintenance)"

    # Display as metric cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(label=f"BMI {bmi_emoji}", value=bmi, delta=bmi_category)
    with m2:
        st.metric(label="Maintenance Calories", value=f"{calories} kcal")
    with m3:
        st.metric(label="Target Calories", value=f"{target_calories} kcal", delta=calorie_note)
    with m4:
        # Suggest workout days based on activity level
        workout_days = {
            "Sedentary (little or no exercise)":        "3x / week",
            "Lightly Active (1-3 days/week)":           "3-4x / week",
            "Moderately Active (3-5 days/week)":        "4-5x / week",
            "Very Active (6-7 days/week)":              "5-6x / week",
            "Athlete (twice per day)":                  "6x / week"
        }
        st.metric(label="Suggested Workouts", value=workout_days[activity_level])

    st.markdown("---")

    # ── Generate button ───────────────────────────────────────────
    generate = st.button(
        "🚀 Generate My Personalized Plan",
        use_container_width=True,
        type="primary"
    )

    # ── Package everything into a dictionary ──────────────────────
    # This is what we return to app.py so the AI can use it
    user_profile = {
        "age":            age,
        "height":         height,
        "weight":         weight,
        "gender":         gender,
        "activity_level": activity_level,
        "goal":           current_goal,
        "experience":     experience,
        "equipment":      equipment,
        "injuries":       injuries,
        "bmi":            bmi,
        "bmi_category":   bmi_category,
        "calories":       calories,
        "target_calories": target_calories
    }

    return user_profile, generate