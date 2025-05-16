import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables safely
try:
    load_dotenv()
except Exception as e:
    st.warning(f"Note: Could not load .env file. You'll need to enter your API key below. Error: {e}")

# Configure Google Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

# Set page configuration
st.set_page_config(
    page_title="punyt💗🔥",
    page_icon="💗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide the sidebar completely
st.markdown(
    """
    <style>
    [data-testid="collapsedControl"] {
        display: none
    }
    
    /* Add scrolling for the chat container */
    .chat-container {
        height: 70vh;
        overflow-y: auto;
        padding: 10px;
        margin-bottom: 10px;
        border: 1px solid #f0f0f0;
        border-radius: 5px;
    }
    
    /* Reduce space in various elements */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0 !important;
    }
    
    h1, h2, h3 {
        margin-top: 0 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stChatInput {
        padding-top: 0 !important;
    }
    
    .css-1544g2n {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    
    /* Hide overflow footer */
    footer {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# System prompt for punyt agent
SYSTEM_PROMPT = """You are a 'punyt' agent. You always talk in Hinglish. 
Answer the user's question in Hinglish and in each answer to user's query replace every 'u', 'i', and 'e' with a 'y' 
and then give the final response. Do this only while you use a Hinglish word."""

# Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_api_key" not in st.session_state:
    st.session_state.user_api_key = GOOGLE_API_KEY or ""

# Initialize model and chat
def initialize_chat():
    api_key = st.session_state.get("user_api_key", "")
    if api_key:
        try:
            genai.configure(api_key=api_key)
            
            # Create the model with default parameters
            model = genai.GenerativeModel(model_name="gemini-2.0-flash")
            
            # Start chat with empty history
            chat = model.start_chat(history=[])
            
            return model, chat
        except Exception as e:
            st.error(f"Failed to initialize Gemini model: {e}")
    return None, None

# Process user prompt and get response
def process_prompt(prompt, chat):
    try:
        # Combine system prompt with user prompt
        combined_prompt = f"{SYSTEM_PROMPT}\n\nUser message: {prompt}"
        response = chat.send_message(combined_prompt, stream=False)
        return response.text
    except Exception as e:
        st.error(f"Error communicating with Gemini API: {e}")
        return "Sorry, I encountered an error. Please try again."

# Compact main app layout
st.markdown('<div style="margin-bottom: 10px;">', unsafe_allow_html=True)
col1, col2 = st.columns([5, 1])
with col1:
    st.title("punyt💗🔥")
    st.subheader("👋 Hyllo! May punyt💗🔥 hoon. Myjhsy kych poocho!")
with col2:
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# API key input - only show if no key is set
if not st.session_state.user_api_key:
    api_key_input = st.text_input(
        "Enter your Google Gemini API Key", 
        type="password",
        help="Enter your Google Gemini API key to start chatting"
    )
    if api_key_input:
        st.session_state.user_api_key = api_key_input
        st.success("API key set successfully!")
        st.rerun()
        
# Display API key warning if no key is set
if not st.session_state.user_api_key:
    st.warning("⚠️ Please enter your Google Gemini API key above to start using the assistant.")
    st.stop()

# Initialize model and chat
model, chat = initialize_chat()

# Create a container for the chat messages
chat_container = st.container()

# Chat input - Put this first so it appears at the bottom
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    # Get AI response
    model, chat = initialize_chat()
    if model and chat:
        with st.spinner("Thinking..."):
            response = process_prompt(prompt, chat)
            # Add AI response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    # Force a rerun to update the chat display
    st.rerun()

# Now display all messages in the chat container
with chat_container:
    # Display all messages in chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
    # If no messages, add some empty space for aesthetics
    if not st.session_state.chat_history:
        st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True) 
