import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.database import save_progress_entry, load_progress
from datetime import datetime

def render_progress_tracker(user_id: str, user_profile: dict):
    """
    Render the full progress tracking dashboard.
    """
    st.markdown("## 📊 Progress Tracker")
    st.markdown("Track your weight and workouts over time.")
    st.markdown("---")

    # ── Log new entry ──────────────────────────────────────────────
    st.markdown("### ➕ Log Today's Progress")

    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input(
            "Today's Weight (kg)",
            min_value=30.0,
            max_value=300.0,
            value=float(user_profile.get("weight", 65)),
            step=0.1
        )
    with col2:
        workout_done = st.selectbox(
            "Workout Completed",
            options=[
                "Rest Day",
                "Full Body",
                "Push Day (Chest/Shoulders/Triceps)",
                "Pull Day (Back/Biceps)",
                "Leg Day",
                "Cardio",
                "Custom Workout"
            ]
        )

    notes = st.text_input(
        "Notes (optional)",
        placeholder="e.g. Felt strong today, increased bench press weight"
    )

    if st.button("💾 Save Today's Entry",
                 use_container_width=True,
                 type="primary"):
        save_progress_entry(user_id, weight, workout_done, notes)
        st.success("✅ Progress saved!")
        st.rerun()

    st.markdown("---")

    # ── Load and display progress ──────────────────────────────────
    progress_data = load_progress(user_id)

    if not progress_data:
        st.info("📝 No progress logged yet. Start logging above!")
        return

    # Convert to DataFrame for easy charting
    df = pd.DataFrame(progress_data)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    # ── Summary metrics ────────────────────────────────────────────
    st.markdown("### 📈 Your Progress Summary")

    start_weight = df["weight"].iloc[0]
    current_weight = df["weight"].iloc[-1]
    weight_change = current_weight - start_weight
    total_days = len(df)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Starting Weight", f"{start_weight} kg")
    with m2:
        st.metric("Current Weight", f"{current_weight} kg",
                  delta=f"{weight_change:+.1f} kg")
    with m3:
        st.metric("Days Tracked", total_days)
    with m4:
        workouts = df[df["workout"] != "Rest Day"].shape[0]
        st.metric("Workouts Logged", workouts)

    st.markdown("---")

    # ── Weight chart ───────────────────────────────────────────────
    st.markdown("### ⚖️ Weight Over Time")

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(
        df["date"],
        df["weight"],
        marker="o",
        linewidth=2,
        color="#FF6B35",
        markersize=6
    )

    # Add goal line
    goal = user_profile.get("goal", "")
    if goal == "Fat Loss" and len(df) > 1:
        ax.axhline(
            y=start_weight - 5,
            color="green",
            linestyle="--",
            alpha=0.5,
            label="Goal (-5kg)"
        )
        ax.legend()

    ax.set_xlabel("Date")
    ax.set_ylabel("Weight (kg)")
    ax.set_title("Weight Progress")
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    # ── Workout log table ──────────────────────────────────────────
    st.markdown("### 📋 Workout History")
    display_df = df[["date", "weight", "workout", "notes"]].copy()
    display_df["date"] = display_df["date"].dt.strftime("%Y-%m-%d")
    display_df.columns = ["Date", "Weight (kg)", "Workout", "Notes"]
    st.dataframe(display_df, use_container_width=True, hide_index=True)