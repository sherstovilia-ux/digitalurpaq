import streamlit as st
import requests
from streamlit_lottie import st_lottie

# ---- Page setup ----
st.set_page_config(
    page_title="Digital Urpaq Support Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---- Clean UI ----
st.markdown("""
    <style>
        header {visibility: hidden;}
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        .block-container {padding-top: 1rem; padding-bottom: 1rem;}
        .chat-bubble {
            border-radius: 20px;
            padding: 10px 15px;
            margin: 8px 0;
            max-width: 80%;
            word-wrap: break-word;
        }
        .user-bubble {
            background-color: #DCF8C6;
            align-self: flex-end;
        }
        .bot-bubble {
            background-color: #F1F0F0;
            align-self: flex-start;
        }
        .chat-container {
            display: flex;
            flex-direction: column;
        }
        .robot-animation {
            display: flex;
            justify-content: center;
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# ---- Load Lottie ----
def load_lottie_url(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except:
        return None

def load_lottie_local(filepath: str):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return None

# Try online first, fallback to local
lottie_robot = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_jqz7l0di.json")
if not lottie_robot:
    lottie_robot = load_lottie_local("robot.json")

# ---- Responses ----
responses = {
    "контакты": "📞 Адрес: ул. Жамбыла Жабаева 55А, Петропавловск. Телефон: 8 7152 34-02-40.",
    "актовый зал": "🎭 В здании три актовых зала...",
    "помощь": "🧭 Доступные команды: кабинет <название>, контакты, актовый зал, запись, помощь.",
    "запись": "🗓️ Онлайн-форма: https://docs.google.com/forms/...",
}

cabinet_map = {
    "лего": "🧩 Кабинет LEGO-конструирования — 1 этаж, правое крыло...",
    "роботы": "🤖 Кабинет Робототехники — 2 этаж, левое крыло, конец коридора.",
}

# ---- Session state ----
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "bot", "text": "Привет! 🤖 Я ваш помощник Digital Urpaq."}]

# ---- Chat UI ----
st.title("🤖 Digital Urpaq Support Bot")

# Robot animation
if lottie_robot:
    st_lottie(lottie_robot, height=150, key="robot_animation", speed=1)

chat_placeholder = st.empty()
with chat_placeholder.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        bubble_class = "user-bubble" if msg["role"] == "user" else "bot-bubble"
        st.markdown(f'<div class="chat-bubble {bubble_class}">{msg["text"]}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---- Input area ----
st.markdown("---")
user_input = st.text_input("✏️ Ваш вопрос:", key="input", placeholder="Напишите сообщение...")
col1, col2 = st.columns([5, 1])
with col2:
    send = st.button("📩")

# ---- Logic ----
if send and user_input:
    user_msg = user_input.strip()
    st.session_state.messages.append({"role": "user", "text": user_msg})

    message = user_msg.lower()
    reply = None

    if "кабинет" in message:
        for name, location in cabinet_map.items():
            if name in message:
                reply = location
                break
        if not reply:
            reply = "🏢 Уточните название кабинета."
    else:
        for k, v in responses.items():
            if k in message:
                reply = v
                break

    if not reply:
        reply = "❓ Простите, я не понял команду. Напишите 'помощь'."

    st.session_state.messages.append({"role": "bot", "text": reply})
    st.experimental_rerun()

