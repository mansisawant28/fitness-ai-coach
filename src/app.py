import streamlit as st
from dotenv import load_dotenv
import os
import sys

sys.path.append(os.path.dirname(__file__))

from components.profile_form import render_profile_form
from components.plan_display import display_workout_plan, display_nutrition_plan
from components.chat import render_chat
from components.progress_tracker import render_progress_tracker
from chains.fitness_chain import generate_workout_plan, generate_nutrition_plan
from utils.database import initialize_database, save_user_profile, load_user_profile, save_plan, load_latest_plan
from utils.memory import get_or_create_user_id, get_user_display_name

load_dotenv()

# ── Initialize database on startup ────────────────────────────────
initialize_database()

# ── Get or create user ID ──────────────────────────────────────────
user_id = get_or_create_user_id()

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
    st.caption(f"👤 {get_user_display_name()}")
    st.markdown("---")
    if st.button("🆕 New User / Switch User", use_container_width=True):
        # Clear everything from session
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        # Clear URL params
        st.query_params.clear()
        st.rerun()
    
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

# ── Load saved profile if exists ───────────────────────────────────
saved_profile = load_user_profile(user_id)
if saved_profile and "user_profile" not in st.session_state:
    st.session_state["user_profile"] = saved_profile

# ── Pages ──────────────────────────────────────────────────────────
if page == "👤 My Profile":
    user_profile, generate_clicked = render_profile_form()

    if generate_clicked:
        # Save to session state AND database
        st.session_state["user_profile"] = user_profile
        save_user_profile(user_id, user_profile)
        st.balloons()
        st.success("✅ Profile saved! Your data is remembered for next time.")

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

    if "user_profile" not in st.session_state:
        st.warning("⚠️ Please fill your profile first!")
        st.stop()

    user_profile = st.session_state["user_profile"]
    st.info(f"🎯 Goal: **{user_profile['goal']}** | "
            f"💪 Level: **{user_profile['experience']}** | "
            f"🔥 Calories: **{user_profile['target_calories']} kcal**")

    # Check saved plan in database first
    saved_plan = load_latest_plan(user_id, "workout")
    if saved_plan and "workout_plan" not in st.session_state:
        st.session_state["workout_plan"] = saved_plan

    if "workout_plan" not in st.session_state:
        if st.button("🚀 Generate Workout Plan",
                     use_container_width=True,
                     type="primary"):
            with st.spinner("🤖 Creating your personalized workout plan..."):
                plan = generate_workout_plan(user_profile)
                st.session_state["workout_plan"] = plan
                save_plan(user_id, "workout", plan)
            st.success("✅ Workout plan generated and saved!")
            st.rerun()
    else:
        display_workout_plan(st.session_state["workout_plan"])
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

    # Check saved plan in database first
    saved_plan = load_latest_plan(user_id, "nutrition")
    if saved_plan and "nutrition_plan" not in st.session_state:
        st.session_state["nutrition_plan"] = saved_plan

    if "nutrition_plan" not in st.session_state:
        if st.button("🚀 Generate Nutrition Guide",
                     use_container_width=True,
                     type="primary"):
            with st.spinner("🤖 Creating your personalized nutrition guide..."):
                plan = generate_nutrition_plan(user_profile)
                st.session_state["nutrition_plan"] = plan
                save_plan(user_id, "nutrition", plan)
            st.success("✅ Nutrition guide generated and saved!")
            st.rerun()
    else:
        display_nutrition_plan(st.session_state["nutrition_plan"])
        if st.button("🔄 Generate New Guide", use_container_width=True):
            del st.session_state["nutrition_plan"]
            st.rerun()

elif page == "📊 Progress Tracker":
    if "user_profile" not in st.session_state:
        st.warning("⚠️ Please fill your profile first!")
        st.stop()
    render_progress_tracker(user_id, st.session_state["user_profile"])

elif page == "💬 AI Coach":
    if "user_profile" not in st.session_state:
        st.warning("⚠️ Please fill your profile first!")
        st.stop()
    render_chat(user_id, st.session_state["user_profile"])
