import streamlit as st
from gtts import gTTS
import base64
import os

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
    </style>
""", unsafe_allow_html=True)

# ---- Responses ----
responses = {
    "контакты": "📞 Адрес: ул. Жамбыла Жабаева 55А, Петропавловск. Телефон: 8 7152 34-02-40. Также смотрите сайт: https://digitalurpaq.edu.kz/ru/kkbajlanysrukontakty.html",
    "актовый зал": "🎭 В здании три актовых зала: первый — над лобби (через правые или левые лестницы), второй — в левом крыле, где раздевалка, третий — в учебном блоке рядом с IT-кабинетами.",
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
if "voice_enabled" not in st.session_state:
    st.session_state.voice_enabled = False

# ---- Chat UI ----
st.title("🤖 Digital Urpaq Support Bot")

# Voice toggle in sidebar
st.sidebar.header("⚙️ Настройки")
st.session_state.voice_enabled = st.sidebar.toggle("🔊 Включить голос робота", value=st.session_state.voice_enabled)

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

    # Add bot message
    st.session_state.messages.append({"role": "bot", "text": reply})

    # ---- Voice (if enabled) ----
    if st.session_state.voice_enabled:
        tts = gTTS(text=reply, lang="ru")
        tts.save("bot_voice.mp3")

        with open("bot_voice.mp3", "rb") as f:
            audio_bytes = f.read()
            b64_audio = base64.b64encode(audio_bytes).decode()

        audio_html = f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
            </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)

    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()

