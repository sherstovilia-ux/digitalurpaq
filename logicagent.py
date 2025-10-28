import streamlit as st
import pyttsx3
import tempfile
import os
import base64

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
.chat-bubble {border-radius: 20px; padding: 10px 15px; margin: 8px 0; max-width: 80%; word-wrap: break-word;}
.user-bubble {background-color: #DCF8C6; align-self: flex-end;}
.bot-bubble {background-color: #F1F0F0; align-self: flex-start;}
.chat-container {display: flex; flex-direction: column;}
</style>
""", unsafe_allow_html=True)

# ---- Responses ----
responses = {
    "контакты": "📞 Адрес: ул. Жамбыла Жабаева 55А, Петропавловск. Телефон: 8 7152 34-02-40. Также смотрите сайт: https://digitalurpaq.edu.kz/ru/kkbajlanysrukontakty.html",
    "актовый зал": "🎭 В здании три актовых зала: первый — над лобби, второй — в левом крыле, третий — в учебном блоке рядом с IT-кабинетами.",
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
    st.session_state.messages = [{"role": "bot", "text": "Привет! 🤖 Я ваш помощник Digital Urpaq. Голос включён. Скажите 'выключи голос', чтобы отключить звук."}]

if "voice_enabled" not in st.session_state:
    st.session_state.voice_enabled = True

# ---- Initialize pyttsx3 ----
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # speed
engine.setProperty("volume", 1.0)  # volume 0-1

# Select a Russian voice if available
voices = engine.getProperty("voices")
for v in voices:
    if "ru" in v.languages[0].decode().lower() or "russian" in v.name.lower():
        engine.setProperty("voice", v.id)
        break

# ---- Chat UI ----
st.title("🤖 Digital Urpaq Support Bot")
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

    # Voice control
    if "выключи голос" in message:
        st.session_state.voice_enabled = False
        reply = "🔇 Голос робота выключен."
    elif "включи голос" in message:
        st.session_state.voice_enabled = True
        reply = "🔊 Голос робота включен."
    elif "кабинет" in message:
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

    # ---- Speak ----
    if st.session_state.voice_enabled:
        try:
            # Save temporary audio file
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tmp_file.close()
            engine.save_to_file(reply, tmp_file.name)
            engine.runAndWait()

            # Play in browser
            with open(tmp_file.name, "rb") as f:
                audio_bytes = f.read()
                b64_audio = base64.b64encode(audio_bytes).decode()
            st.markdown(f"""
                <audio autoplay>
                    <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
                </audio>
            """, unsafe_allow_html=True)
            os.unlink(tmp_file.name)
        except Exception as e:
            st.warning(f"⚠️ Не удалось воспроизвести голос: {e}")

    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()


