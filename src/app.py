import streamlit as st
from dotenv import load_dotenv
import os

# Import our profile form component
from components.profile_form import render_profile_form

# Load API keys from .env file
load_dotenv()

# ── Page config ────────────────────────────────────────────────────
st.set_page_config(
    page_title="FitCoach AI",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Sidebar navigation ─────────────────────────────────────────────
with st.sidebar:
    st.image("https://via.placeholder.com/150x60?text=FitCoach+AI")
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
    st.markdown("### 📌 Quick Tips")
    st.info("Fill your profile first to get the most accurate personalized plan!")

# ── Main content ───────────────────────────────────────────────────
st.title("🏋️ FitCoach AI")
st.caption("Your personalized AI-powered fitness coach")
st.markdown("---")

# ── Route to correct page ──────────────────────────────────────────
if page == "👤 My Profile":
    # Render the profile form and get back user data
    user_profile, generate_clicked = render_profile_form()

    # If the user clicked Generate Plan
    if generate_clicked:
        # Save profile to session state so all pages can access it
        st.session_state["user_profile"] = user_profile
        st.balloons()
        st.success("✅ Profile saved! Your personalized plan is being prepared.")
        st.markdown("### 📋 Your Profile Summary")
        
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
    st.markdown("## 🏋️ Your Workout Plan")
    if "user_profile" not in st.session_state:
        st.warning("⚠️ Please fill your profile first!")
        st.stop()
    st.info("🔧 AI workout generation coming in Phase 3!")

elif page == "🥗 Nutrition Guide":
    st.markdown("## 🥗 Your Nutrition Guide")
    if "user_profile" not in st.session_state:
        st.warning("⚠️ Please fill your profile first!")
        st.stop()
    st.info("🔧 AI nutrition guidance coming in Phase 3!")

elif page == "📊 Progress Tracker":
    st.markdown("## 📊 Progress Tracker")
    st.info("🔧 Progress tracking coming in Phase 5!")

elif page == "💬 AI Coach":
    st.markdown("## 💬 AI Coach")
    if "user_profile" not in st.session_state:
        st.warning("⚠️ Please fill your profile first!")
        st.stop()
    st.info("🔧 AI chat coach coming in Phase 3!")