import streamlit as st
from gtts import gTTS
import io
import base64

# ---- Page setup ----
st.set_page_config(page_title="Digital Urpaq Support Bot", layout="wide")

# ---- Session State ----
if "lang" not in st.session_state:
    st.session_state.lang = "ru"
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "bot",
        "text": "Привет! Я помощник Digital Urpaq. Задайте вопрос о кабинетах, контактах или записи."
    }]
if "tts_enabled" not in st.session_state:
    st.session_state.tts_enabled = True

# ---- Responses ----
responses_ru = {
    "контакты": "Адрес: ул. Жамбыла Жабаева 55А, Петропавловск. Телефон: 8 7152 34-02-40.",
    "актовый зал": "В здании три актовых зала.",
    "помощь": "Доступные команды: кабинет <название>, контакты, актовый зал, запись, помощь.",
    "запись": "Онлайн-форма: https://docs.google.com/forms/..."
}
responses_kk = {
    "байланыс": "Мекенжай: Жамбыл Жабаев көш., 55А, Петропавл.",
    "акт залы": "Ғимаратта үш акт залы бар.",
    "көмек": "Қолжетімді командалар: кабинет <атауы>, байланыс, акт залы, жазылу, көмек.",
    "жазылу": "Онлайн нысан: https://docs.google.com/forms/..."
}

# ---- Helper: TTS ----
def tts_audio_bytes(text, lang_code):
    tts = gTTS(text=text, lang=lang_code)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp

# ---- Chat UI ----
st.title("🤖 Digital Urpaq Support Bot")
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**Вы:** {msg['text']}")
    else:
        # Иконка динамика для TTS
        speaker_icon = "🔊" if st.session_state.tts_enabled else ""
        st.markdown(f"**Бот:** {msg['text']} {speaker_icon}")
        if st.session_state.tts_enabled:
            lang = "ru" if st.session_state.lang=="ru" else "kk"
            audio_bytes = tts_audio_bytes(msg['text'], lang)
            st.audio(audio_bytes, format="audio/mp3", start_time=0)

# ---- Input Form ----
with st.form(key="user_input_form"):
    placeholder = "Ваш вопрос:" if st.session_state.lang=="ru" else "Сұрағыңызды жазыңыз..."
    user_input = st.text_input(placeholder)
    submit_button = st.form_submit_button("Отправить")

# ---- Logic ----
if submit_button and user_input:
    st.session_state.messages.append({"role": "user", "text": user_input})
    message = user_input.lower()
    if st.session_state.lang == "ru":
        responses = responses_ru
        lang_code = "ru"
    else:
        responses = responses_kk
        lang_code = "kk"
    
    reply = None
    for k, v in responses.items():
        if k in message:
            reply = v
            break
    if not reply:
        reply = "Простите, я не понял команду. Напишите 'помощь'." if lang_code=="ru" else "Кешіріңіз, түсінбедім. 'Көмек' деп жазыңыз."
    
    st.session_state.messages.append({"role": "bot", "text": reply})

# ---- TTS Toggle ----
st.checkbox("Включить TTS / TTS қосу", value=st.session_state.tts_enabled, key="tts_enabled")
