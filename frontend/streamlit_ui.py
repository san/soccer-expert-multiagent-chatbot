import os

import streamlit as st
import requests
from datetime import datetime
import time

# ============================================================================
# Page Configuration
# ============================================================================

st.set_page_config(
    page_title="Soccer Expert Chatbot",
    page_icon="⚽",
    # layout="wide",
    initial_sidebar_state="expanded"
)


# Streamed response emulator
def generate_response(message_text):
 
    if not st.session_state.connected:
        st.error("❌ API not connected. Please configure connection in sidebar.")
        return ""
    
    try:
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
            return data["response"]
        else:
            error_data = response.json() if response.text else {}
            error_msg = error_data.get("detail", f"Status {response.status_code}")
            st.error(f"❌ Error: {error_msg}")
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Oops! Something went wrong. Please try again."
            })
            return "Oops! Something went wrong. Please try again."
        
    except requests.exceptions.Timeout:
        st.error("❌ Request timeout. Please try again.")
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Oops! Something went wrong. Please try again."
        })
        return "Oops! Something went wrong. Please try again."
    except requests.exceptions.ConnectionError:
        st.error("❌ Connection error. Please check the API URL.")
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Oops! Something went wrong. Please try again."
        })
        return "Oops! Something went wrong. Please try again."

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Oops! Something went wrong. Please try again."
        })
        return "Oops! Something went wrong. Please try again."


def handle_user_input(message_text, chat_container=None):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": message_text})
    # Display user message in chat message container
    with chat_container.chat_message("user"):
        st.markdown(message_text)

    # Display assistant response in chat message container
    with chat_container.chat_message("assistant"):
        with st.spinner("Thinking..."):
            full_response = ""
            assistant_response = generate_response(message_text)
            message_placeholder = st.empty()
        for chunk in assistant_response.split(" "):
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)


if "session_id" not in st.session_state:
    st.session_state.session_id = f"streamlit_session_{datetime.now().timestamp()}"

# Set the API URL from secrets
if "api_url" not in st.session_state:
    st.session_state.api_url = os.environ.get("API_URL", "http://localhost:8000")  # Default to localhost if not set

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "connected" not in st.session_state:
    st.session_state.connected = False

if "connection_tested" not in st.session_state:
    st.session_state.connection_tested = False

if "testing_connection" not in st.session_state:
    st.session_state.testing_connection = False


# ============================================================================
# Test Connection Function
# ============================================================================

def connect_with_api():
    """Establish connection with API and update connection status"""
    st.session_state.testing_connection = True
    try:
        with st.spinner("Connecting..."):
            try:
                response = requests.get(f"{st.session_state.api_url}/health", timeout=60)
                if response.status_code == 200:
                    st.session_state.connected = True
                    data = response.json()
                    st.write(f"Status: {data['status']}")
                    st.write(f"Active sessions: {data['active_sessions']}")
                else:
                    st.session_state.connected = False
                    st.error(f"✗ Error: Status {response.status_code}")
            except Exception as e:
                st.session_state.connected = False
                st.error(f"✗ Connection failed: {str(e)}")
    finally:
        st.session_state.connection_tested = True
        st.session_state.testing_connection = False


# ============================================================================
# Sidebar Configuration
# ============================================================================

with st.sidebar:
    st.title("⚽ Soccer Expert Chatbot")
    st.caption("Google ADK-powered soccer expert chatbot with RAG and web search")
    
    # API Configuration
    st.header("⚙️ Configuration")

    st.subheader("🌐 API Connection")

    custom_url = st.text_input(
        "Enter API URL",
        value=st.session_state.api_url,
        help="Enter API URL"
    )
    if custom_url and custom_url.rstrip("/") != st.session_state.api_url:
        st.session_state.api_url = custom_url.rstrip("/")
        st.session_state.connected = False

    if not st.session_state.connection_tested:
        connect_with_api()

    # Manual test button
    if st.button("🔌 Connect", use_container_width=True):
        connect_with_api()
    
    if st.session_state.connected:
        st.success("🟢 Connected")
    else:
        st.warning("🔴 Not Connected")

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


chat_container = st.container()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with chat_container.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
prompt = st.chat_input("Ask me anything about soccer...")
if prompt:
    handle_user_input(prompt, chat_container)

# ============================================================================
# Sample Questions Section
# ============================================================================
sample_questions_container = st.bottom.container()

with sample_questions_container:
    col1, col2, col3 = st.columns(3)

    sample_questions = [
        "Who won World Cup in 2022?",
        "Explain throw-in rule in soccer.",
        "Tell me about world cup 2026."
    ]

    with col1:
        if st.button(sample_questions[0], use_container_width=True, key="q1"):
            handle_user_input(sample_questions[0], chat_container)

    with col2:
        if st.button(sample_questions[1], use_container_width=True, key="q2"):
            handle_user_input(sample_questions[1], chat_container)

    with col3:
        if st.button(sample_questions[2], use_container_width=True, key="q3"):
            handle_user_input(sample_questions[2], chat_container)


# ============================================================================
# Footer
# ============================================================================

st.bottom.divider()
col1, col2, col3 = st.bottom.columns(3)

with col1:
    st.caption("📖 [Documentation](https://github.com/san/soccer-expert-multiagent-chatbot)")

with col2:
    st.caption("🐛 [Report Issues](https://github.com/san/soccer-expert-multiagent-chatbot/issues)")

with col3:
    st.caption("💬 Chat Sessions: " + str(len(st.session_state.messages) // 2))

