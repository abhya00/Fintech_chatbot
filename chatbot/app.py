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

# Custom CSS for chat bubbles
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .chat-container {
            max-width: 600px;
            margin: auto;
        }
        .user-bubble {
            background: linear-gradient(to right, #007bff, #0056b3);
            color: white;
            padding: 12px;
            border-radius: 15px;
            max-width: 75%;
            text-align: right;
            align-self: flex-end;
        }
        .bot-bubble {
            background: linear-gradient(to right, #d4edda, #a8e6cf);
            color: black;
            padding: 12px;
            border-radius: 15px;
            max-width: 75%;
            text-align: left;
            align-self: flex-start;
        }
        .message-container {
            display: flex;
            flex-direction: column;
        }
        .stButton>button {
            background: linear-gradient(to right, #007bff, #0056b3);
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
        }
        .stTextInput>div>div>input {
            border-radius: 10px;
            padding: 10px;
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
st.markdown("<div class='chat-box'>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='message-container' style='align-items: flex-end;'><div class='user-bubble'>👤 {msg['content']}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='message-container' style='align-items: flex-start;'><div class='bot-bubble'>🤖 {msg['content']}</div></div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# **Input Box & Send Button in a Single Row**
col1, col2 = st.columns([5, 1])  # Input takes more space, button takes less

with col1:
    user_input = st.text_input("Enter your question:", key="user_input", label_visibility="collapsed", placeholder="Ask your question...")

with col2:
    send_clicked = st.button("Send")

# Process input when the button is clicked
if send_clicked and user_input:
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
