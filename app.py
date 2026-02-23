import streamlit as st
import os
from backend.chatbot import CareerChatbot
from backend.memory_manager import MemoryManager
from backend.logger import setup_logger

# ------------------ Setup Logger ------------------
logger = setup_logger()
logger.info("Application started.")

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="AI Career Advisor",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ------------------ Safe Asset Paths ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

logo_path = os.path.join(ASSETS_DIR, "imageeee.webp")
user_avatar = os.path.join(ASSETS_DIR, "user.png")
bot_avatar = os.path.join(ASSETS_DIR, "chatbot.png")

# ------------------ PREMIUM DARK THEME ------------------
st.markdown("""
<style>

/* Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #000000 0%, #0f172a 100%);
}

/* Remove Header */
[data-testid="stHeader"] {
    background: transparent;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #000000;
    border-right: 1px solid #1f2937;
}

/* Force all text white */
html, body, p, span, div, label {
    color: white !important;
}

/* Chat Bubbles */
[data-testid="stChatMessage"] {
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 14px;
    font-size: 15px;
    backdrop-filter: blur(12px);
}

[data-testid="stChatMessage-user"] {
    background: rgba(37, 99, 235, 0.15);
    border: 1px solid rgba(37, 99, 235, 0.4);
}

[data-testid="stChatMessage-assistant"] {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
}

/* ---------------- PURE BLACK CHAT INPUT ---------------- */

[data-testid="stChatInput"] > div {
    background: #000000 !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
}

[data-testid="stChatInput"] textarea {
    background: #000000 !important;
    color: white !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: rgba(255,255,255,0.5) !important;
}

/* Remove red focus */
textarea:focus {
    outline: none !important;
    box-shadow: none !important;
}

/* Button Glow */
.stButton>button {
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    color: white;
    border-radius: 10px;
    padding: 8px 18px;
    border: none;
    transition: 0.3s ease;
}

.stButton>button:hover {
    box-shadow: 0 0 15px rgba(255,255,255,0.4);
    transform: translateY(-2px);
}

hr {
    border: 0.5px solid rgba(255,255,255,0.1);
}

</style>
""", unsafe_allow_html=True)

# ------------------ Sidebar ------------------
with st.sidebar:

    st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.06);
        padding: 22px;
        border-radius: 18px;
        box-shadow: 0 0 30px rgba(255, 255, 255, 0.18);
        border: 1px solid rgba(255,255,255,0.15);
        margin-bottom: 25px;
    ">
    """, unsafe_allow_html=True)

    if os.path.exists(logo_path):
        st.image(logo_path, width=130)

    st.markdown("""
    <h2 style="color: white; font-weight: 600; margin-top: 10px;">
    🚀 AI Career Advisor
    </h2>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="color: rgba(255,255,255,0.85); font-size: 14px;">
    Empowering your future with AI-driven guidance.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h4 style="color: white; margin-top: 18px;">
    ✨ FEATURES
    </h4>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex; flex-direction:column; gap:10px;">
        <div style="background: rgba(255,255,255,0.08); padding:8px 12px; border-radius:10px;">
            🚀 Career Suggestions
        </div>
        <div style="background: rgba(255,255,255,0.08); padding:8px 12px; border-radius:10px;">
            📊 Skill Gap Analysis
        </div>
        <div style="background: rgba(255,255,255,0.08); padding:8px 12px; border-radius:10px;">
            📝 Resume Advice
        </div>
        <div style="background: rgba(255,255,255,0.08); padding:8px 12px; border-radius:10px;">
            📚 Learning Roadmap
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ------------------ Initialize Session ------------------
MemoryManager.initialize_session()

# ------------------ Header ------------------
st.markdown("""
<h1 style='
font-size:36px; 
font-weight:600; 
background: linear-gradient(90deg, #2563eb, #7c3aed);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
text-align:center;
'>
🚀 AI Career Advisor
</h1>
""", unsafe_allow_html=True)

st.divider()

# ------------------ Initialize Chatbot ------------------
if "chatbot" not in st.session_state:
    st.session_state.chatbot = CareerChatbot()

# ------------------ Display Chat History ------------------
for msg in MemoryManager.get_history():
    avatar = user_avatar if msg["role"] == "user" else bot_avatar
    with st.chat_message(msg["role"], avatar=avatar if os.path.exists(avatar) else None):
        st.markdown(msg["content"])

# ------------------ Chat Input ------------------
user_input = st.chat_input("Ask your career question...")

if user_input:
    with st.chat_message("user", avatar=user_avatar if os.path.exists(user_avatar) else None):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar=bot_avatar if os.path.exists(bot_avatar) else None):
        with st.spinner("Analyzing your career path..."):
            response = st.session_state.chatbot.get_response(user_input)
        st.markdown(response)

# ------------------ Clear Button ------------------
st.divider()

if st.button("🔄 Start New Conversation"):
    MemoryManager.clear()
    st.rerun()