import streamlit as st
import time
from streamlit_lottie import st_lottie
import requests
import json
import os

# ---- Page setup ----
st.set_page_config(
    page_title="Digital Urpaq Support Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---- CSS ----
st.markdown("""
<style>
header {visibility: hidden;}
footer {visibility: hidden;}
#MainMenu {visibility: hidden;}
.block-container {padding-top: 1rem; padding-bottom: 1rem;}
.chat-bubble {border-radius: 20px; padding: 10px 15px; margin: 8px 0; max-width: 80%; word-wrap: break-word;}
.user-bubble {background-color: #DCF8C6; align-self: flex-end;}
.bot-bubble {background-color: #F1F0F0; align-self: flex-start;}
.chat-container {display: flex; flex-direction: column; position: relative;}
.background-lottie {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 120px;
    z-index: 10;
    opacity: 0.7;
}
</style>
""", unsafe_allow_html=True)

# ---- Load Lottie animation ----
def load_lottie_url(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

def load_lottie_local(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

# Try network first, fallback to local
lottie_robot = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_q5pk6p1k.json")
if not lottie_robot:
    lottie_robot = load_lottie_local("robot.json")  # Make sure this file exists

# ---- Responses ----
responses = {
    "контакты": "📞 Адрес: ул. Жамбыла Жабаева 55А, Петропавловск. Телефон: 8 7152 34-02-40. Сайт: https://digitalurpaq.edu.kz/ru/kkbajlanysrukontakty.html",
    "актовый зал": "🎭 В здании три актовых зала: первый над лобби, второй в левом крыле, третий в учебном блоке рядом с IT-кабинетами.",
    "помощь": "🧭 Доступные команды: кабинет <название>, контакты, актовый зал, запись, помощь.",
    "запись": "🗓️ Онлайн-форма: https://docs.google.com/forms/d/e/1FAIpQLSc5a5G0CY5XuOCpVHcg7qTDBdEGGkyVEjuBwihpfHncDCqv2A/viewform",
}

cabinet_map = {
    "лего": "🧩 Кабинет LEGO-конструирования — 1 этаж, правое крыло, третий справа от входа.",
    "физика": "⚛️ Кабинет Физики — левое крыло, 3 этаж, рядом с Астрономией.",
    "шахматы": "♟️ Кабинет Шахмат — правое крыло, 1 этаж, рядом с Лего.",
    "биология": "🧬 Кабинет Биологии — 3 этаж, центральная часть, блок Д1.",
    "электрика": "💡 Кабинет Электротехники — 2 этаж, правое крыло.",
    "дроны": "🚁 Кабинет Дронов — 2 этаж, правое крыло.",
    "3д моделирования": "🖨️ Кабинет 3D-моделирования — 2 этаж, IT-блок, правое крыло.",
    "роботы": "🤖 Кабинет Робототехники — 2 этаж, левое крыло, конец коридора.",
    "вр": "🕶️ VR-кабинет — 2 этаж, правое крыло.",
    "програмирование": "💻 Кабинет Программирования — 2 этаж, дальнее правое крыло.",
    "анимирование": "🎞️ Кабинет Анимирования — 2 этаж, правое крыло.",
    "экономика": "💰 Кабинет Экономики — 2 этаж, правое крыло.",
    "рисование": "🎨 Кабинет Рисования — 3 этаж, правое крыло.",
}

# ---- Session state ----
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "bot", "text": "Привет! 🤖 Я ваш помощник Digital Urpaq. Задайте вопрос о кабинетах, контактах или записи."}]

# ---- Chat UI ----
st.title("🤖 Digital Urpaq Support Bot")
chat_placeholder = st.empty()

def render_chat():
    chat_placeholder.empty()
    with chat_placeholder.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            bubble_class = "user-bubble" if msg["role"] == "user" else "bot-bubble"
            st.markdown(f'<div class="chat-bubble {bubble_class}">{msg["text"]}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

render_chat()

# ---- Input area ----
st.markdown("---")
user_input = st.text_input("✏️ Ваш вопрос:", key="input", placeholder="Напишите сообщение...")
col1, col2 = st.columns([5, 1])
with col2:
    send = st.button("📩")

# ---- Render robot animation safely ----
if lottie_robot:
    st_lottie(lottie_robot, height=120, key="background_robot")
else:
    st.warning("🤖 Robot animation failed to load. Please check your 'robot.json' file.")

# ---- Chat logic ----
if send and user_input:
    user_msg = user_input.strip()
    st.session_state.messages.append({"role": "user", "text": user_msg})

    # Simulate thinking
    time.sleep(1.5)

    # Determine reply
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
    render_chat()

