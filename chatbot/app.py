import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Google Gemini AI
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Streamlit page configuration
st.set_page_config(page_title="FinTech Chatbot", page_icon="💰", layout="centered")

# Custom CSS for chat bubbles & fixed input
st.markdown("""
    <style>
        * {
            font-family: "Times New Roman", Times, serif !important;
        }
        body {
            background-color: #121212;
            color: white;
        }
        .chat-container {
            max-width: 600px;
            margin: auto;
            padding-bottom: 60px; /* Space for input box */
        }
        .user-bubble {
            background: linear-gradient(to right, #007bff, #0056b3);
            color: white;
            padding: 12px;
            border-radius: 15px;
            max-width: 75%;
            text-align: right;
            align-self: flex-end;
            margin: 5px 0;
        }
        .bot-bubble {
            background: linear-gradient(to right, #d4edda, #a8e6cf);
            color: black;
            padding: 12px;
            border-radius: 15px;
            max-width: 75%;
            text-align: left;
            align-self: flex-start;
            margin: 5px 0;
        }
        .message-container {
            display: flex;
            flex-direction: column;
        }
        /* Fixed Input Box at Bottom */
        .input-container {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            width: 600px;
            display: flex;
            gap: 10px;
            background: #121212;
            padding: 10px;
            border-radius: 10px;
        }
        .stTextInput>div>div>input {
            flex: 1;
            padding: 12px;
            border-radius: 20px;
            border: 1px solid #444;
            background: #333;
            color: white;
        }
        .stButton>button {
            background: linear-gradient(to right, #007bff, #0056b3);
            color: white;
            border: none;
            border-radius: 20px;
            padding: 12px 20px;
            cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)

# Chatbot Header
st.markdown("<h1 style='text-align: center;'>💰 FinTech Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Ask me anything about loans, interest rates, CIBIL, and more!</p>", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat Box
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='message-container' style='align-items: flex-end;'><div class='user-bubble'>👤 {msg['content']}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='message-container' style='align-items: flex-start;'><div class='bot-bubble'>🤖 {msg['content']}</div></div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Fixed Input Box & Send Button Next to Each Other
st.markdown("<div class='input-container'>", unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])  # Adjust column widths for input & button

with col1:
    user_input = st.text_input("", key="user_input", label_visibility="collapsed", placeholder="Enter your question...")

with col2:
    if st.button("Send"):
        if user_input:
            # Append user message
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Get chatbot response
            try:
                response = model.generate_content(user_input)
                bot_reply = response.text if response else "Sorry, I couldn't understand that."
            except Exception as e:
                bot_reply = f"Error: {e}"

            # Append bot response
            st.session_state.messages.append({"role": "bot", "content": bot_reply})

            # Rerun script to refresh UI
            st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
