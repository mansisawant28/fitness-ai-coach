import streamlit as st
import uuid

def get_or_create_user_id() -> str:
    """
    Get or create a user ID that survives page refreshes.
    
    Strategy:
    1. Check URL query params first (survives refresh)
    2. Check session state (same tab)
    3. Create new one if neither exists
    """

    # Step 1 — Check if user_id is in the URL
    # e.g. http://localhost:8501/?user_id=abc123
    query_params = st.query_params
    
    if "user_id" in query_params:
        # Found in URL — use it and save to session
        user_id = query_params["user_id"]
        st.session_state["user_id"] = user_id
        return user_id

    # Step 2 — Check session state
    if "user_id" in st.session_state:
        # Save to URL so it survives refresh
        st.query_params["user_id"] = st.session_state["user_id"]
        return st.session_state["user_id"]

    # Step 3 — Brand new user — create fresh ID
    new_id = str(uuid.uuid4())[:8]  # short 8 char ID
    st.session_state["user_id"] = new_id
    st.query_params["user_id"] = new_id
    print(f"🆕 New user created: {new_id}")
    return new_id

def get_user_display_name() -> str:
    """Short display name for the sidebar"""
    user_id = get_or_create_user_id()
    return f"User {user_id}"