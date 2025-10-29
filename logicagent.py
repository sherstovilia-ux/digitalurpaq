import streamlit as st
from google.cloud import texttospeech
from io import BytesIO

st.set_page_config(page_title="Digital Urpaq Support Bot", layout="wide")

# ---- Session ----
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "bot",
        "text": "Привет! Я помощник Digital Urpaq. Задайте вопрос о кабинетах, контактах или записи."
    }]
if "tts_enabled" not in st.session_state:
    st.session_state.tts_enabled = True
if "last_audio" not in st.session_state:
    st.session_state.last_audio = None

# ---- TTS Function ----
def make_tts(text: str, lang_code: str):
    client = texttospeech.TextToSpeechClient()
    if lang_code == "kk":
        language = "kk-KZ"
        voice_name = "kk-KZ-Standard-A"
    else:
        language = "ru-RU"
        voice_name = "ru-RU-Standard-D"

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice_params = texttospeech.VoiceSelectionParams(
        language_code=language,
        name=voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=synthesis_input, voice=voice_params, audio_config=audio_config)
    return BytesIO(response.audio_content)  # используем буфер

# ---- Simple Chat ----
st.title("🤖 Digital Urpaq Support Bot")

for msg in st.session_state.messages:
    role = "User" if msg["role"] == "user" else "Bot"
    st.markdown(f"**{role}:** {msg['text']}")

user_input = st.text_input("Ваш вопрос:")
if st.button("Отправить") and user_input:
    st.session_state.messages.append({"role": "user", "text": user_input})
    
    # ---- Simple reply logic ----
    reply = ""
    if "кабинет" in user_input.lower():
        reply = "Уточните, пожалуйста, какой кабинет?"
    else:
        reply = "Простите, я не понял команду."

    st.session_state.messages.append({"role": "bot", "text": reply})

    # ---- TTS ----
    if st.session_state.tts_enabled:
        audio_bytes = make_tts(reply, "ru")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)
        st.session_state.last_audio = audio_bytes

