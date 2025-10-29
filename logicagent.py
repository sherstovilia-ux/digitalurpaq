import streamlit as st
import pyttsx3
import tempfile
import os

# ---- Page setup ----
st.set_page_config(page_title="Digital Urpaq Support Bot", layout="wide")

# ---- Session State ----
if "lang" not in st.session_state:
    st.session_state.lang = "ru"
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "bot","text": "Привет! Я помощник Digital Urpaq. Задайте вопрос о кабинетах, контактах или записи."}]
if "tts_enabled" not in st.session_state:
    st.session_state.tts_enabled = True

# ---- Responses ----
responses_ru = {"контакты":"Адрес: ул. Жамбыла Жабаева 55А, Петропавловск.","помощь":"Доступные команды: кабинет <название>, контакты, помощь."}
responses_kk = {"байланыс":"Мекенжай: Жамбыл Жабаев көш., 55А, Петропавл.","көмек":"Қолжетімді командалар: кабинет <атауы>, байланыс, көмек."}

# ---- Offline TTS ----
engine = pyttsx3.init()

def tts_streamlit_bytes(text, lang):
    """Генерирует mp3-байты для Streamlit через pyttsx3"""
    # Выбор голоса по языку
    voices = engine.getProperty('voices')
    voice_set = False
    for voice in voices:
        if lang=="ru" and "ru" in voice.id.lower():
            engine.setProperty('voice', voice.id)
            voice_set = True
            break
        elif lang=="kk" and "kz" in voice.id.lower():
            engine.setProperty('voice', voice.id)
            voice_set = True
            break
    if not voice_set:
        engine.setProperty('voice', voices[0].id)  # fallback

    # Генерация временного файла
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        engine.save_to_file(text, f.name)
        engine.runAndWait()
        f.seek(0)
        data = f.read()
    os.remove(f.name)
    return data

# ---- Chat UI ----
st.title("🤖 Digital Urpaq Support Bot")
for msg in st.session_state.messages:
    bubble = "user" if msg["role"]=="user" else "bot"
    st.markdown(f"**{msg['role']}**: {msg['text']}")

# ---- Input Form ----
with st.form(key="user_input_form"):
    placeholder = "Ваш вопрос:" if st.session_state.lang=="ru" else "Сұрағыңызды жазыңыз..."
    user_input = st.text_input(placeholder)
    submit_button = st.form_submit_button("Отправить")

if submit_button and user_input:
    msg = user_input.strip()
    st.session_state.messages.append({"role":"user","text":msg})
    
    # ---- Logic ----
    message = msg.lower()
    lang = st.session_state.lang
    responses = responses_ru if lang=="ru" else responses_kk
    
    reply = None
    for k,v in responses.items():
        if k in message:
            reply = v
            break
    if not reply:
        reply = "Простите, не понял." if lang=="ru" else "Кешіріңіз, түсінбедім."
    st.session_state.messages.append({"role":"bot","text":reply})

    # ---- TTS ----
    if st.session_state.tts_enabled and reply:
        audio_bytes = tts_streamlit_bytes(reply, lang)
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

# ---- TTS Toggle ----
st.checkbox("Включить TTS / TTS қосу", value=st.session_state.tts_enabled, key="tts_enabled")



