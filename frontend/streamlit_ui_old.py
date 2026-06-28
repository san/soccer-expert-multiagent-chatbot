#streamlit_ui.py

"""
Streamlit UI for Soccer Expert Chatbot Agent

Simple and intuitive interface for chatting with the chatbot.
Can connect to local FastAPI or Cloud Run deployment.
"""

import streamlit as st
import requests
from datetime import datetime
import time
import os


def response_generator(response_text: str):
    
    for word in response_text.split():
        yield word + " "
        time.sleep(0.05)
# ============================================================================
# Page Configuration
# ============================================================================

st.set_page_config(
    page_title="Soccer Expert Chatbot",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# Styling
# ============================================================================

st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd !important;
        border-left: 4px solid #2196F3;
        color: #000000 !important;
    }
    .assistant-message {
        background-color: #ffffff !important;
        border-left: 4px solid #4CAF50;
        color: #000000 !important;
    }
    .error-message {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        color: #000000 !important;
    }
    .info-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.85rem;
        font-weight: 500;
        margin-right: 0.5rem;
    }
    .rag-badge {
        background-color: #c8e6c9;
        color: #1b5e20;
    }
    .web-badge {
        background-color: #bbdefb;
        color: #0d47a1;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# Session State Initialization
# ============================================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = f"streamlit_session_{datetime.now().timestamp()}"

if "api_url" not in st.session_state:
    st.session_state.api_url = os.environ.get("API_URL", "http://localhost:8000")  # Default to localhost if not set

if "connected" not in st.session_state:
    st.session_state.connected = False

# ============================================================================
# Helper Functions
# ============================================================================

def submit_message(message_text: str) -> None:
    """Submit a message to the chatbot API and update chat history."""
    if not st.session_state.connected:
        st.error("❌ API not connected. Please configure connection in sidebar.")
        return
    
    # Add user message to chat
    st.session_state.messages.append({
        "role": "user",
        "content": message_text
    })

    # Get response from API
    try:
        with st.spinner("🔄 Agents thinking..."):
            response = requests.post(
                f"{st.session_state.api_url}/query",
                json={
                    "user_id": "streamlit_user",
                    "session_id": st.session_state.session_id,
                    "message": message_text
                },
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": data["response"],
                    "tool_used": data.get("tool_used")
                })
                st.rerun()
            else:
                error_data = response.json() if response.text else {}
                error_msg = error_data.get("detail", f"Status {response.status_code}")
                st.error(f"❌ Error: {error_msg}")

    except requests.exceptions.Timeout:
        st.error("❌ Request timeout. Please try again.")
    except requests.exceptions.ConnectionError:
        st.error("❌ Connection error. Please check the API URL.")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

# ============================================================================
# Sidebar Configuration
# ============================================================================

with st.sidebar:
    st.title("⚙️ Configuration")

    # API Configuration
    st.subheader("🌐 API Connection")

    custom_url = st.text_input(
        "Enter API URL",
        value=st.session_state.api_url,
        help="Enter API URL"
    )
    if custom_url:
        st.session_state.api_url = custom_url.rstrip("/")

    # Test Connection
    if st.button("🔌 Test Connection", use_container_width=True):
        with st.spinner("Testing connection..."):
            try:
                response = requests.get(f"{st.session_state.api_url}/health", timeout=60)
                if response.status_code == 200:
                    st.session_state.connected = True
                    data = response.json()
                    st.success("✓ Connected!")
                    st.write(f"Status: {data['status']}")
                    st.write(f"Active sessions: {data['active_sessions']}")
                else:
                    st.session_state.connected = False
                    st.error(f"✗ Error: Status {response.status_code}")
            except Exception as e:
                st.session_state.connected = False
                st.error(f"✗ Connection failed: {str(e)}")

    st.divider()

    # Session Information
    st.subheader("📋 Session Info")
    st.write(f"**Session ID:** `{st.session_state.session_id}`")
    st.write(f"**Messages:** {len(st.session_state.messages)}")
    st.write(f"**Connected:** {'✓ Yes' if st.session_state.connected else '✗ No'}")

    st.divider()

    # Clear Chat
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.success("Chat history cleared")
        st.rerun()

# ============================================================================
# Main Content
# ============================================================================

# Header
col1, col2 = st.columns([4, 1])
with col1:
    st.title("⚽ Soccer Expert Chatbot")
    st.caption("Google ADK-powered soccer expert chatbot with RAG and web search")

with col2:
    if st.session_state.connected:
        st.success("🟢 Connected")
    else:
        st.warning("🔴 Not Connected")

# ============================================================================
# Info Section
# ============================================================================

# if len(st.session_state.messages) == 0:
expander = st.expander("ℹ️ About Soccer Expert Chatbot", expanded=False)
with expander:
    st.info("""
    ### Welcome to Soccer Expert Chatbot! 👋

    This chatbot uses **Google ADK with Gemini 2.5 Flash** to provide intelligent soccer expertise.

    **Features:**
    - 🧠 **Intelligent Tool Selection** - Automatically chooses between knowledge base and web search
    - 📚 **RAG System** - Semantic search over company knowledge base
    - 🌐 **Web Search** - Real-time external information
    - 💬 **Conversation Memory** - Remembers previous messages
    - 🔌 **REST API** - Easy integration with any application

    **How to Use:**
    1. Configure your API connection in the sidebar
    2. Test the connection
    3. Start asking questions!
    """)

st.divider()

# Chat Messages Display
chat_container = st.container()

with chat_container:
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Input Area
st.divider()

# Create form for message input - allows Enter key to submit
with st.form(key="message_form"):
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Message:",
            placeholder="Ask me anything about soccer...",
            label_visibility="collapsed",
            key="user_input_field"
        )
    
    with col2:
        send_button = st.form_submit_button("📤 Send", use_container_width=True)

# Handle Message Sending
if send_button and user_input:
    submit_message(user_input)


# ============================================================================
# Sample Questions Section
# ============================================================================
sample_questions_container = st.container()

with sample_questions_container:
    col1, col2, col3 = st.columns(3)

    sample_questions = [
        "Who won World Cup in 2022?",
        "Explain throw-in rule in soccer.",
        "Tell me about world cup 2026."
    ]

    with col1:
        if st.button(sample_questions[0], use_container_width=True, key="q1"):
            submit_message(sample_questions[0])

    with col2:
        if st.button(sample_questions[1], use_container_width=True, key="q2"):
            submit_message(sample_questions[1])

    with col3:
        if st.button(sample_questions[2], use_container_width=True, key="q3"):
            submit_message(sample_questions[2])


# ============================================================================
# Footer
# ============================================================================

st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    st.caption("📖 [Documentation](https://github.com/san/soccer-expert-multiagent-chatbot)")

with col2:
    st.caption("🐛 [Report Issues](https://github.com/san/soccer-expert-multiagent-chatbot/issues)")

with col3:
    st.caption("💬 Chat Sessions: " + str(len(st.session_state.messages) // 2))
