import streamlit as st
from dotenv import load_dotenv
import os
import sys

sys.path.append(os.path.dirname(__file__))

from components.profile_form import render_profile_form
from components.plan_display import display_workout_plan, display_nutrition_plan
from chains.fitness_chain import generate_workout_plan, generate_nutrition_plan

load_dotenv()

# ── Page config ────────────────────────────────────────────────────
st.set_page_config(
    page_title="FitCoach AI",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Sidebar ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("# 🏋️ FitCoach AI")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        options=[
            "👤 My Profile",
            "🏋️ Workout Plan",
            "🥗 Nutrition Guide",
            "📊 Progress Tracker",
            "💬 AI Coach"
        ]
    )
    st.markdown("---")
    st.info("💡 Fill your profile first to get your personalized plan!")

# ── Header ─────────────────────────────────────────────────────────
st.title("🏋️ FitCoach AI")
st.caption("Your personalized AI-powered fitness coach")
st.markdown("---")

# ── Pages ──────────────────────────────────────────────────────────
if page == "👤 My Profile":
    user_profile, generate_clicked = render_profile_form()

    if generate_clicked:
        st.session_state["user_profile"] = user_profile
        st.balloons()
        st.success("✅ Profile saved! Go to Workout Plan or Nutrition Guide.")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"- **Age:** {user_profile['age']} years")
            st.markdown(f"- **Height:** {user_profile['height']} cm")
            st.markdown(f"- **Weight:** {user_profile['weight']} kg")
            st.markdown(f"- **Gender:** {user_profile['gender']}")
            st.markdown(f"- **BMI:** {user_profile['bmi']} ({user_profile['bmi_category']})")
        with col2:
            st.markdown(f"- **Goal:** {user_profile['goal']}")
            st.markdown(f"- **Activity:** {user_profile['activity_level']}")
            st.markdown(f"- **Experience:** {user_profile['experience']}")
            st.markdown(f"- **Target Calories:** {user_profile['target_calories']} kcal/day")
            st.markdown(f"- **Equipment:** {', '.join(user_profile['equipment'])}")

elif page == "🏋️ Workout Plan":
    st.markdown("## 🏋️ Workout Plan")

    # Check profile exists
    if "user_profile" not in st.session_state:
        st.warning("⚠️ Please fill your profile first!")
        st.stop()

    user_profile = st.session_state["user_profile"]

    # Show profile summary in sidebar style
    st.info(f"🎯 Goal: **{user_profile['goal']}** | "
            f"💪 Level: **{user_profile['experience']}** | "
            f"🔥 Calories: **{user_profile['target_calories']} kcal**")

    # Check if plan already generated — don't regenerate unnecessarily
    if "workout_plan" not in st.session_state:
        if st.button("🚀 Generate Workout Plan", use_container_width=True, type="primary"):
            with st.spinner("🤖 AI is creating your personalized workout plan... this takes 20-30 seconds"):
                plan = generate_workout_plan(user_profile)
                st.session_state["workout_plan"] = plan
            st.success("✅ Workout plan generated!")
            st.rerun()
    else:
        # Plan already exists — show it
        display_workout_plan(st.session_state["workout_plan"])

        # Option to regenerate
        if st.button("🔄 Generate New Plan", use_container_width=True):
            del st.session_state["workout_plan"]
            st.rerun()

elif page == "🥗 Nutrition Guide":
    st.markdown("## 🥗 Nutrition Guide")

    if "user_profile" not in st.session_state:
        st.warning("⚠️ Please fill your profile first!")
        st.stop()

    user_profile = st.session_state["user_profile"]

    st.info(f"🎯 Goal: **{user_profile['goal']}** | "
            f"🔥 Target: **{user_profile['target_calories']} kcal/day**")

    if "nutrition_plan" not in st.session_state:
        if st.button("🚀 Generate Nutrition Guide", use_container_width=True, type="primary"):
            with st.spinner("🤖 AI is creating your personalized nutrition guide... this takes 20-30 seconds"):
                plan = generate_nutrition_plan(user_profile)
                st.session_state["nutrition_plan"] = plan
            st.success("✅ Nutrition guide generated!")
            st.rerun()
    else:
        display_nutrition_plan(st.session_state["nutrition_plan"])

        if st.button("🔄 Generate New Guide", use_container_width=True):
            del st.session_state["nutrition_plan"]
            st.rerun()

elif page == "📊 Progress Tracker":
    st.markdown("## 📊 Progress Tracker")
    st.info("🔧 Progress tracking coming in Phase 5!")

elif page == "💬 AI Coach":
    st.markdown("## 💬 AI Coach")
    if "user_profile" not in st.session_state:
        st.warning("⚠️ Please fill your profile first!")
        st.stop()
    st.info("🔧 AI chat coach coming in Phase 4!")