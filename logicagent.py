import streamlit as st
from google.cloud import texttospeech
import base64

# ---- Page setup ----
st.set_page_config(page_title="Digital Urpaq Support Bot", layout="wide")

# ---- Session state ----
if "lang" not in st.session_state:
    st.session_state.lang = "ru"
if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"bot","text":"Привет! Я помощник Digital Urpaq."}]
if "tts_enabled" not in st.session_state:
    st.session_state.tts_enabled = True
if "pending_audio" not in st.session_state:
    st.session_state.pending_audio = None

# ---- Language toggle ----
col1, col2 = st.columns([4,1])
with col2:
    if st.button("Қаз / Рус"):
        st.session_state.lang = "kk" if st.session_state.lang=="ru" else "ru"
        st.session_state.messages.append({
            "role":"bot",
            "text": "Тіл қазақ тіліне ауыстырылды." if st.session_state.lang=="kk" else "Язык переключён на русский."
        })

# ---- TTS ----
def make_tts(text, lang_code):
    client = texttospeech.TextToSpeechClient()

    voice_name = "kk-KZ-Standard-A" if lang_code=="kk" else "ru-RU-Standard-D"
    language_code = "kk-KZ" if lang_code=="kk" else "ru-RU"

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    b64 = base64.b64encode(response.audio_content).decode()
    return f"data:audio/mp3;base64,{b64}"

# ---- Chat display ----
st.title("🤖 Digital Urpaq Support Bot")
for msg in st.session_state.messages:
    style = "text-align:right; background:#DCF8C6;padding:10px;border-radius:15px;" if msg["role"]=="user" else "text-align:left; background:#F1F0F0;padding:10px;border-radius:15px;"
    st.markdown(f'<div style="{style}">{msg["text"]}</div>', unsafe_allow_html=True)

# ---- Input ----
placeholder = "Сұрағыңызды жазыңыз..." if st.session_state.lang=="kk" else "Ваш вопрос:"
user_input = st.text_input(placeholder, placeholder=placeholder)
send = st.button("Жіберу" if st.session_state.lang=="kk" else "Отправить")

# ---- Simple responses ----
responses_ru = {
    "контакты": "Адрес: ул. Жамбыла Жабаева 55А, Петропавловск. Телефон: 8 7152 34-02-40.",
    "актовый зал": "В здании три актовых зала.",
    "помощь": "Команды: кабинет <название>, контакты, актовый зал, помощь."
}
responses_kk = {
    "байланыс": "Мекенжай: Жамбыл Жабаев көш., 55А, Петропавл.",
    "акт залы": "Ғимаратта үш акт залы бар.",
    "көмек": "Қол жетімді командалар: кабинет <атауы>, байланыс, акт залы, көмек."
}
cabinet_map_ru = {"физика":"Кабинет Физики — 3 этаж."}
cabinet_map_kk = {"физика":"Физика кабинеті — 3 қабат."}

# ---- Handle user input ----
if send and user_input:
    msg = user_input.strip()
    st.session_state.messages.append({"role":"user","text":msg})
    message = msg.lower()
    reply = None

    responses = responses_kk if st.session_state.lang=="kk" else responses_ru
    cabinet_map = cabinet_map_kk if st.session_state.lang=="kk" else cabinet_map_ru
    lang_code = "kk" if st.session_state.lang=="kk" else "ru"

    if "кабинет" in message:
        found = False
        for k,v in cabinet_map.items():
            if k in message:
                reply = v
                found = True
                break
        if not found:
            reply = "Уточните кабинет?" if lang_code=="ru" else "Қай кабинет екенін нақтылаңызшы?"
    else:
        found = False
        for k,v in responses.items():
            if k in message:
                reply = v
                found = True
                break
        if not found:
            reply = "Не понял команду. Напишите 'помощь'." if lang_code=="ru" else "Түсінбедім. 'Көмек' деп жазыңыз."

    st.session_state.messages.append({"role":"bot","text":reply})
    if st.session_state.tts_enabled:
        st.session_state.pending_audio = make_tts(reply, lang_code)

# ---- Play TTS ----
if st.session_state.pending_audio:
    st.markdown(f"""
        <audio autoplay>
            <source src="{st.session_state.pending_audio}" type="audio/mp3">
        </audio>
    """, unsafe_allow_html=True)
    st.session_state.pending_audio = None


