import json
import os
import uuid
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from concierge.agent.main import Agent  # noqa: E402

# Page configuration
st.set_page_config(
    page_title="Luxury Concierge Chat",
    page_icon="🎩",
    layout="wide",
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

if "admin_mode" not in st.session_state:
    st.session_state.admin_mode = False

# Display header
st.title("🎩 Luxury Concierge")
st.caption("Your personal AI assistant for premium products and services")

# Create tabs
if st.session_state.admin_mode:
    chat_tab, metrics_tab = st.tabs(["💬 Chat", "📊 Metrics"])
else:
    chat_tab = st.container()
    metrics_tab = None

# Chat Tab
with chat_tab:
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

# Metrics Tab (only visible in admin mode)
if st.session_state.admin_mode and metrics_tab is not None:
    with metrics_tab:
        st.header("📊 Analytics Dashboard")

        agent = get_agent()

        # Global metrics
        st.subheader("Global Metrics")
        global_metrics = agent.memory.get_global_metrics()

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Conversations", global_metrics.total_conversations)
        with col2:
            st.metric("Total Messages", global_metrics.total_messages)
        with col3:
            st.metric("Avg Latency (ms)", f"{global_metrics.avg_latency_ms:.2f}")
        with col4:
            st.metric("Total Tool Calls", global_metrics.total_tool_calls)

        col5, col6 = st.columns(2)
        with col5:
            st.metric("Guardrail Blocks", global_metrics.guardrail_blocks)
        with col6:
            if global_metrics.total_messages > 0:
                block_rate = (global_metrics.guardrail_blocks / global_metrics.total_messages) * 100
                st.metric("Block Rate", f"{block_rate:.1f}%")

        # Tool usage chart
        if global_metrics.tools_usage:
            st.subheader("Tool Usage Distribution")
            tools_df = pd.DataFrame(list(global_metrics.tools_usage.items()), columns=["Tool", "Count"]).sort_values(
                "Count", ascending=False
            )
            st.bar_chart(tools_df.set_index("Tool"))

        st.divider()

        # Conversation-specific metrics
        st.subheader("Current Conversation Metrics")
        conversation_metrics = agent.memory.get_conversation_metrics(st.session_state.conversation_id)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Messages", conversation_metrics.total_messages)
        with col2:
            st.metric("Avg Latency (ms)", f"{conversation_metrics.avg_latency_ms:.2f}")
        with col3:
            st.metric("Tool Calls", conversation_metrics.total_tool_calls)

        col4, col5 = st.columns(2)
        with col4:
            st.metric("Guardrail Blocks", conversation_metrics.guardrail_blocks)
        with col5:
            if conversation_metrics.total_messages > 0:
                block_rate = (conversation_metrics.guardrail_blocks / conversation_metrics.total_messages) * 100
                st.metric("Block Rate", f"{block_rate:.1f}%")

        # Conversation-specific tool usage
        if conversation_metrics.tools_usage:
            st.subheader("Tool Usage in This Conversation")
            conv_tools_df = pd.DataFrame(
                list(conversation_metrics.tools_usage.items()), columns=["Tool", "Count"]
            ).sort_values("Count", ascending=False)
            st.bar_chart(conv_tools_df.set_index("Tool"))
        else:
            st.info("No tool usage recorded for this conversation yet.")

        st.divider()

        # Raw metrics data
        with st.expander("📋 Raw Metrics Data"):
            st.subheader("All Message Metrics")
            if agent.memory.metrics:
                metrics_data = []
                for metric in agent.memory.metrics:
                    metrics_data.append(
                        {
                            "Timestamp": metric.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                            "Conversation ID": metric.conversation_id,
                            "Latency (ms)": f"{metric.latency_ms:.2f}",
                            "Tools Used": ", ".join(metric.tools_used) if metric.tools_used else "None",
                            "Iterations": metric.num_iterations,
                            "Guardrail Blocked": metric.guardrail_blocked,
                        }
                    )
                metrics_df = pd.DataFrame(metrics_data)
                st.dataframe(metrics_df, use_container_width=True)
            else:
                st.info("No metrics data available yet.")

# Sidebar with info
with st.sidebar:
    st.header("Settings")

    # Admin mode toggle
    admin_password = st.text_input("Admin Password", type="password", key="admin_password")
    if st.button("Toggle Admin Mode"):
        if admin_password == os.getenv("ADMIN_PASSWORD"):  # Simple password check
            st.session_state.admin_mode = not st.session_state.admin_mode
            st.success(f"Admin mode: {'ON' if st.session_state.admin_mode else 'OFF'}")
            st.rerun()
        else:
            st.error("Invalid password")

    if st.session_state.admin_mode:
        st.success("🔓 Admin mode enabled")

    st.divider()

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
