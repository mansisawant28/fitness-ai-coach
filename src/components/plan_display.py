import streamlit as st

def display_workout_plan(plan: str):
    """
    Displays the AI generated workout plan
    in a clean formatted way.
    """
    st.markdown("## 🏋️ Your Personalized Workout Plan")
    st.markdown("---")

    # Display the plan in a nice container
    with st.container():
        st.markdown(plan)

    st.markdown("---")

    # Download button so user can save their plan
    st.download_button(
        label="📥 Download Workout Plan",
        data=plan,
        file_name="my_workout_plan.txt",
        mime="text/plain",
        use_container_width=True
    )

def display_nutrition_plan(plan: str):
    """
    Displays the AI generated nutrition guide
    in a clean formatted way.
    """
    st.markdown("## 🥗 Your Personalized Nutrition Guide")
    st.markdown("---")

    with st.container():
        st.markdown(plan)

    st.markdown("---")

    # Download button
    st.download_button(
        label="📥 Download Nutrition Guide",
        data=plan,
        file_name="my_nutrition_guide.txt",
        mime="text/plain",
        use_container_width=True
    )