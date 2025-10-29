import streamlit as st
from google.cloud import texttospeech
from io import BytesIO

st.set_page_config(page_title="Digital Urpaq Support Bot", layout="wide")

# ---- CSS ----
st.markdown("""
<style>
header, footer, #MainMenu {visibility: hidden;}
.banner img {
    width: 100%;
    max-height: 250px;
    object-fit: cover;
    border-radius: 10px;
}
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
#mic-indicator {
    text-align: center;
    font-size: 18px;
    margin-top: 10px;
}
.mic {
    display: inline-block;
    margin-left: 10px;
    animation: pulse 1s infinite;
}
@keyframes pulse {
    0% {transform: scale(1); opacity: 1;}
    50% {transform: scale(1.3); opacity: 0.5;}
    100% {transform: scale(1); opacity: 1;}
}
</style>
""", unsafe_allow_html=True)

# ---- Banner ----
st.markdown("""
<div class="banner">
    <img src="https://s12.gifyu.com/images/b36xz.gif" alt="Banner">
</div>
""", unsafe_allow_html=True)

# ---- Session State ----
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "bot", "text": "Привет! Я помощник Digital Urpaq. Задайте вопрос о кабинетах, контактах или записи."}]
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
    return BytesIO(response.audio_content)

# ---- Chat UI ----
st.title("🤖 Digital Urpaq Support Bot")
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        bubble = "user-bubble" if msg["role"] == "user" else "bot-bubble"
        st.markdown(f'<div class="chat-bubble {bubble}">{msg["text"]}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---- User Input ----
user_input = st.text_input("Ваш вопрос:")
send = st.button("Отправить")

if send and user_input:
    st.session_state.messages.append({"role": "user", "text": user_input})
    
    msg_lower = user_input.lower()
    if "кабинет" in msg_lower:
        reply = "Уточните, пожалуйста, какой кабинет?"
    else:
        reply = "Простите, я не понял команду."
    
    st.session_state.messages.append({"role": "bot", "text": reply})

    # ---- TTS ----
    if st.session_state.tts_enabled:
        audio_bytes = make_tts(reply, "ru")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)
        st.session_state.last_audio = audio_bytes
