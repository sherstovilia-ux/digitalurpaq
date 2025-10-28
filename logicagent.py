import streamlit as st
from gtts import gTTS
import base64
from io import BytesIO

# ---- Page setup ----
st.set_page_config(
    page_title="Digital Urpaq Support Bot",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---- Banner ----
st.markdown("""
<div class="banner">
    <img src="https://s12.gifyu.com/images/b36xz.gif" alt="Robot Banner">
</div>
<style>
.banner img {
    width: 100%;
    max-height: 280px;
    object-fit: cover;
    border-radius: 10px;
}
header, footer, #MainMenu {visibility: hidden;}
.chat-bubble {
    border-radius: 20px;
    padding: 10px 15px;
    margin: 8px 0;
    max-width: 80%;
    word-wrap: break-word;
}
.user-bubble {background-color: #DCF8C6; align-self: flex-end;}
.bot-bubble {background-color: #F1F0F0; align-self: flex-start;}
.chat-container {display: flex; flex-direction: column;}
</style>
""", unsafe_allow_html=True)

# ---- Ответы ----
responses = {
    "контакты": "Адрес: ул. Жамбыла Жабаева 55А, Петропавловск. Телефон: 8 7152 34-02-40. Также смотрите сайт: https://digitalurpaq.edu.kz/ru/kkbajlanysrukontakty.html",
    "актовый зал": "В здании три актовых зала: первый — над лобби, второй — в левом крыле, третий — в учебном блоке рядом с IT-кабинетами.",
    "помощь": "Доступные команды: кабинет <название>, контакты, актовый зал, запись, помощь.",
    "запись": "Онлайн-форма: https://docs.google.com/forms/d/e/1FAIpQLSc5a5G0CY5XuOCpVHcg7qTDBdEGGkyVEjuBwihpfHncDCqv2A/viewform",
}

cabinet_map = {
    "лего": "Кабинет LEGO-конструирования — 1 этаж, правое крыло, третий справа от входа.",
    "физика": "Кабинет Физики — левое крыло, 3 этаж, рядом с Астрономией.",
    "шахматы": "Кабинет Шахмат — правое крыло, 1 этаж, рядом с Лего.",
    "биология": "Кабинет Биологии — 3 этаж, центральная часть, блок Д1.",
    "электрика": "Кабинет Электротехники — 2 этаж, правое крыло.",
    "дроны": "Кабинет Дронов — 2 этаж, правое крыло.",
    "3д моделирования": "Кабинет 3D-моделирования — 2 этаж, IT-блок, правое крыло.",
    "роботы": "Кабинет Робототехники — 2 этаж, левое крыло, конец коридора.",
    "вр": "VR-кабинет — 2 этаж, правое крыло.",
    "програмирование": "Кабинет Программирования — 2 этаж, дальнее правое крыло.",
    "анимирование": "Кабинет Анимирования — 2 этаж, правое крыло.",
    "экономика": "Кабинет Экономики — 2 этаж, правое крыло.",
    "рисование": "Кабинет Рисования — 3 этаж, правое крыло.",
}

# ---- Session ----
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "bot", "text": "Привет! Я помощник Digital Urpaq. Задайте вопрос о кабинетах, контактах или записи."}]
if "tts_enabled" not in st.session_state:
    st.session_state.tts_enabled = True
if "last_audio" not in st.session_state:
    st.session_state.last_audio = None

# ---- Заголовок ----
st.title("🤖 Digital Urpaq Support Bot")

# ---- Отображение чата ----
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        bubble = "user-bubble" if msg["role"] == "user" else "bot-bubble"
        st.markdown(f'<div class="chat-bubble {bubble}">{msg["text"]}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---- Ввод ----
user_input = st.text_input("Ваш вопрос:", placeholder="Напишите сообщение...")
send = st.button("Отправить")

# ---- Функция TTS ----
def speak(text):
    tts = gTTS(text=text, lang='ru', tld='com', slow=False)
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    audio_bytes = fp.read()
    b64 = base64.b64encode(audio_bytes).decode()
    st.session_state.last_audio = f"data:audio/mp3;base64,{b64}"

# ---- Логика ----
if send and user_input:
    message = user_input.strip().lower()
    st.session_state.messages.append({"role": "user", "text": user_input})

    reply = None
    if "выключи голос" in message:
        st.session_state.tts_enabled = False
        reply = "Голос отключен."
    elif "включи голос" in message:
        st.session_state.tts_enabled = True
        reply = "Голос включен."
    elif "актовый зал" in message:
        reply = responses["актовый зал"]
    elif "кабинет" in message:
        for name, location in cabinet_map.items():
            if name in message:
                reply = location
                break
        if not reply:
            reply = "Уточните название кабинета."
    else:
        for k, v in responses.items():
            if k in message:
                reply = v
                break
    if not reply:
        reply = "Простите, я не понял команду. Напишите 'помощь'."

    st.session_state.messages.append({"role": "bot", "text": reply})

    if st.session_state.tts_enabled:
        speak(reply)

    st.rerun()

# ---- Воспроизведение аудио ----
if st.session_state.last_audio and st.session_state.tts_enabled:
    st.markdown(f"""
        <audio autoplay controls style="width: 100%; margin-top:10px;">
            <source src="{st.session_state.last_audio}" type="audio/mp3">
        </audio>
    """, unsafe_allow_html=True)

