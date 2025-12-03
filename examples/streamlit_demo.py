"""Simple Streamlit chat interface for the luxury concierge agent.

To run this demo:
1. Install streamlit: pip install streamlit
2. Run: streamlit run examples/streamlit_demo.py
"""

import json
import uuid
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from concierge.agent.main import Agent  # noqa: E402

# Page configuration
st.set_page_config(
    page_title="Luxury Concierge Chat",
    page_icon="🎩",
    layout="centered",
)


# Initialize the Agent
@st.cache_resource
def get_agent() -> Agent:
    """Initialize and cache the Agent."""
    return Agent()


# Load example users
@st.cache_data
def load_users() -> dict:
    """Load example users from JSON file."""
    users_path = Path(__file__).parent.parent / "data" / "users.json"
    with users_path.open() as f:
        return json.load(f)


# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())

# Display header
st.title("🎩 Luxury Concierge")
st.caption("Your personal AI assistant for premium products and services")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("How may I assist you today?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get agent response
    with st.chat_message("assistant"), st.spinner("Processing..."):
        agent = get_agent()

        # Agent handles conversation history internally
        response = agent.process_message(
            conversation_id=st.session_state.conversation_id,
            message=prompt,
        )

        st.markdown(response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar with info
with st.sidebar:
    st.header("About")
    st.markdown("""
    This is a demo of the luxury concierge agent that can help with:

    - 🛍️ **Product inquiries** - Search and browse premium items
    - 📦 **Order management** - Check status, modify orders
    - 📅 **Appointments** - Schedule fittings and styling sessions
    - 📋 **Policies** - Returns, shipping, warranty info
    """)

    st.divider()

    st.header("Example Users")
    st.markdown("Reference these users when testing:")

    users = load_users()
    for _, user_data in users.items():
        with st.expander(f"👤 {user_data['name']}", expanded=False):
            st.markdown(f"""
            **User ID:** `{user_data["user_id"]}`
            **Email:** `{user_data["email"]}`
            **Phone:** `{user_data["phone"]}`
            """)

    st.divider()

    st.header("Sample Queries")
    st.markdown("""
    Try asking:
    - "Show me merino wool jackets"
    - "What's the status of order ORD-001?"
    - "Show appointments for john.doe@example.com"
    - "What's your return policy?"
    - "I need a new suit and want to book a fitting"
    """)

    st.divider()

    if st.button("Clear Chat", type="secondary"):
        st.session_state.messages = []
        st.session_state.conversation_id = str(uuid.uuid4())
        st.rerun()
