import streamlit as st
from gtts import gTTS
from io import BytesIO

# ---- Page setup ----
st.set_page_config(page_title="Digital Urpaq Support Bot", layout="wide")

# ---- Session State ----
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "bot", "text": "Привет! Я помощник Digital Urpaq."}]
if "lang" not in st.session_state:
    st.session_state.lang = "ru"
if "tts_enabled" not in st.session_state:
    st.session_state.tts_enabled = True

# ---- Language Switch ----
col1, col2 = st.columns([4,1])
with col2:
    if st.button("Қаз / Рус"):
        st.session_state.lang = "kk" if st.session_state.lang=="ru" else "ru"
        st.session_state.messages.append({
            "role":"bot",
            "text":"Язык переключён на русский." if st.session_state.lang=="ru" else "Тіл қазақ тіліне ауыстырылды."
        })

# ---- Responses ----
responses = {
    "ru": {
        "контакты": "Адрес: ул. Жамбыла Жабаева 55А, Петропавловск...",
        "помощь": "Доступные команды: кабинет <название>, контакты, актовый зал, запись, помощь.",
    },
    "kk": {
        "байланыс": "Мекенжай: Жамбыл Жабаев көш., 55А, Петропавл...",
        "көмек": "Қолжетімді командалар: кабинет <атауы>, байланыс, акт залы, жазылу, көмек.",
    }
}

# ---- TTS Function (gTTS) ----
def make_tts(text, lang="ru"):
    tts = gTTS(text=text, lang=lang)
    audio_bytes = BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes

# ---- Display chat ----
st.title("🤖 Digital Urpaq Bot")
for msg in st.session_state.messages:
    st.markdown(f"**{'Вы' if msg['role']=='user' else 'Бот'}:** {msg['text']}")

# ---- User Input ----
user_input = st.text_input("Введите сообщение")
send_button = st.button("Отправить")

if send_button and user_input:
    st.session_state.messages.append({"role":"user","text":user_input})
    
    # ---- Simple response matching ----
    lang = st.session_state.lang
    msg_lower = user_input.lower()
    reply = "Простите, я не понял команду." if lang=="ru" else "Кешіріңіз, түсінбедім."
    
    for key, text in responses[lang].items():
        if key in msg_lower:
            reply = text
            break
    
    st.session_state.messages.append({"role":"bot","text":reply})

    # ---- TTS ----
    if st.session_state.tts_enabled:
        lang_code = "ru" if lang=="ru" else "kk"
        audio = make_tts(reply, lang=lang_code)
        st.audio(audio, format="audio/mp3")
