import streamlit as st
from langchain_core.prompts import PromptTemplate
from rag.retriever import retrieve_relevant_content
from llm import get_llm as get_shared_llm
from utils.database import (
    save_chat_message,
    load_chat_history,
    clear_chat_history
)
def get_llm():
    """Use the shared provider configuration for chat responses."""
    return get_shared_llm(max_tokens=512)

def get_ai_response(
    user_message: str,
    user_profile: dict,
    chat_history: list
) -> str:
    """
    Generate AI coach response using:
    1. User's current message
    2. Their profile (personalization)
    3. Chat history (memory)
    4. RAG knowledge base (accuracy)
    """

    # Step 1 — RAG retrieval for this specific question
    relevant_knowledge = retrieve_relevant_content(user_message, k=3)

    # Step 2 — Format chat history for context
    history_text = ""
    for msg in chat_history[-6:]:  # last 6 messages for context
        role = "User" if msg["role"] == "user" else "Coach"
        history_text += f"{role}: {msg['message']}\n"

    # Step 3 — Build the prompt
    prompt = f"""You are FitCoach AI, a friendly and knowledgeable personal 
fitness coach. You have been talking with this user and know their profile.

USER PROFILE:
- Goal: {user_profile.get('goal', 'Not specified')}
- Age: {user_profile.get('age', 'Not specified')}
- Experience: {user_profile.get('experience', 'Not specified')}
- BMI: {user_profile.get('bmi', 'Not specified')}
- Target Calories: {user_profile.get('target_calories', 'Not specified')} kcal

VERIFIED FITNESS KNOWLEDGE:
{relevant_knowledge}

CONVERSATION HISTORY:
{history_text if history_text else "This is the start of the conversation."}

USER'S CURRENT MESSAGE: {user_message}

Respond as a supportive, expert fitness coach. Be concise (3-5 sentences),
practical, and base your advice on the verified knowledge above.
Address them personally based on their profile and conversation history.
"""

    llm = get_llm()
    response = llm.invoke(prompt)

    if hasattr(response, "content"):
        return response.content
    return response

def render_chat(user_id: str, user_profile: dict):
    """
    Render the full chat interface with memory.
    """
    st.markdown("## 💬 AI Fitness Coach")
    st.markdown("Ask me anything about fitness, nutrition, or your plan!")
    st.markdown("---")

    # Load chat history from database
    chat_history = load_chat_history(user_id)

    # Display existing messages
    for msg in chat_history:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(msg["message"])
        else:
            with st.chat_message("assistant", avatar="🏋️"):
                st.markdown(msg["message"])

    # Clear chat button
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            clear_chat_history(user_id)
            st.rerun()

    # Chat input
    user_input = st.chat_input(
        "Ask your fitness coach anything..."
    )

    if user_input:
        # Show user message immediately
        with st.chat_message("user"):
            st.markdown(user_input)

        # Save user message to database
        save_chat_message(user_id, "user", user_input)

        # Generate AI response
        with st.chat_message("assistant", avatar="🏋️"):
            with st.spinner("Coach is thinking..."):
                response = get_ai_response(
                    user_input,
                    user_profile,
                    chat_history
                )
            st.markdown(response)

        # Save AI response to database
        save_chat_message(user_id, "assistant", response)
        st.rerun()