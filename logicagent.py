import streamlit as st
from google.cloud import texttospeech
import base64

# ---- Page setup ----
st.set_page_config(page_title="Digital Urpaq Support Bot", layout="wide")

# ---- CSS ----
st.markdown("""
<style>
header, footer, #MainMenu {visibility: hidden;}
.banner img {width: 100%; max-height: 250px; object-fit: cover; border-radius: 10px;}
.chat-bubble {border-radius: 20px; padding: 10px 15px; margin: 8px 0; max-width: 80%; word-wrap: break-word;}
.user-bubble {background-color: #DCF8C6; align-self: flex-end;}
.bot-bubble {background-color: #F1F0F0; align-self: flex-start;}
.chat-container {display: flex; flex-direction: column;}
#mic-indicator {text-align: center; font-size: 18px; margin-top: 10px;}
.mic {display: inline-block; margin-left: 10px; animation: pulse 1s infinite;}
@keyframes pulse {0% {transform: scale(1); opacity: 1;} 50% {transform: scale(1.3); opacity: 0.5;} 100% {transform: scale(1); opacity: 1;}}
</style>
""", unsafe_allow_html=True)

# ---- Banner ----
st.markdown("""
<div class="banner">
    <img src="https://s12.gifyu.com/images/b36xz.gif" alt="Banner">
</div>
""", unsafe_allow_html=True)

# ---- Session ----
if "lang" not in st.session_state:
    st.session_state.lang = "ru"
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "bot", "text": "Привет! Я помощник Digital Urpaq. Задайте вопрос о кабинетах, контактах или записи."}]
if "tts_enabled" not in st.session_state:
    st.session_state.tts_enabled = True
if "pending_audio" not in st.session_state:
    st.session_state.pending_audio = None

# ---- Language Switcher ----
col1, col2 = st.columns([4,1])
with col2:
    if st.button("Қаз / Рус"):
        st.session_state.lang = "kk" if st.session_state.lang == "ru" else "ru"
        st.session_state.messages.append({
            "role":"bot",
            "text":"Тіл қазақ тіліне ауыстырылды." if st.session_state.lang=="kk" else "Язык переключён на русский."
        })
        st.rerun()

# ---- Responses ----
responses_ru = {
    "контакты": "Адрес: ул. Жамбыла Жабаева 55А, Петропавловск. Телефон: 8 7152 34-02-40. Также смотрите сайт: https://digitalurpaq.edu.kz/ru/kkbajlanysrukontakty.html",
    "актовый зал": "В здании три актовых зала: первый — над лобби, второй — в левом крыле, третий — в учебном блоке рядом с IT-кабинетами.",
    "помощь": "Доступные команды: кабинет <название>, контакты, актовый зал, запись, помощь.",
    "запись": "Онлайн-форма: https://docs.google.com/forms/d/e/1FAIpQLSc5a5G0CY5XuOCpVHcg7qTDBdEGGkyVEjuBwihpfHncDCqv2A/viewform"
}
responses_kk = {
    "байланыс": "Мекенжай: Жамбыл Жабаев көш., 55А, Петропавл. Телефон: 8 7152 34-02-40. Толығырақ: https://digitalurpaq.edu.kz/kk/kkbajlanysrukontakty.html",
    "акт залы": "Ғимаратта үш акт залы бар: біріншісі — вестибюль үстінде, екіншісі — сол қанатта, үшіншісі — IT кабинеттерінің жанындағы оқу блогында.",
    "көмек": "Қолжетімді командалар: кабинет <атауы>, байланыс, акт залы, жазылу, көмек.",
    "жазылу": "Онлайн нысан: https://docs.google.com/forms/d/e/1FAIpQLSc5a5G0CY5XuOCpVHcg7qTDBdEGGkyVEjuBwihpfHncDCqv2A/viewform"
}
cabinet_map_ru = {
    "лего": "Кабинет LEGO-конструирования — 1 этаж, правое крыло, третий справа от входа.",
    "физика": "Кабинет Физики — левое крыло, 3 этаж, рядом с Астрономией.",
    "робототехника": "Кабинет Робототехники — 2 этаж, левое крыло, конец коридора."
}
cabinet_map_kk = {
    "лего": "LEGO-құрастыру кабинеті — 1 қабат, оң жақ қанат, кіреберістен үшінші есік.",
    "физика": "Физика кабинеті — сол жақ қанат, 3 қабат, Астрономия кабинетімен қатар.",
    "робототехника": "Робототехника кабинеті — 2 қабат, сол жақ қанат, дәліздің соңында."
}

# ---- TTS Function ----
def make_tts(text: str, lang_code: str):
    try:
        client = texttospeech.TextToSpeechClient()
        if lang_code == "kk":
            language, voice_name = "kk-KZ", "kk-KZ-Standard-A"
        else:
            language, voice_name = "ru-RU", "ru-RU-Standard-D"

        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice_params = texttospeech.VoiceSelectionParams(
            language_code=language,
            name=voice_name,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice_params, audio_config=audio_config
        )
        b64 = base64.b64encode(response.audio_content).decode()
        return f"data:audio/mp3;base64,{b64}"
    except Exception as e:
        print("Ошибка TTS:", e)
        return None

# ---- Chat Display ----
st.title("🤖 Digital Urpaq Support Bot")
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        bubble = "user-bubble" if msg["role"]=="user" else "bot-bubble"
        st.markdown(f'<div class="chat-bubble {bubble}">{msg["text"]}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---- User Input ----
placeholder = "Сұрағыңызды жазыңыз..." if st.session_state.lang=="kk" else "Ваш вопрос:"
user_input = st.text_input(placeholder, placeholder=placeholder)
send = st.button("Жіберу" if st.session_state.lang=="kk" else "Отправить")

# ---- Logic ----
if send and user_input:
    msg = user_input.strip()
    st.session_state.messages.append({"role":"user","text":msg})
    message = msg.lower()
    reply = None

    if st.session_state.lang=="ru":
        responses, cabinet_map, lang_code = responses_ru, cabinet_map_ru, "ru"
    else:
        responses, cabinet_map, lang_code = responses_kk, cabinet_map_kk, "kk"

    if ("выключи голос" in message) or ("дыбысты сөндір" in message):
        st.session_state.tts_enabled = False
        reply = "Голос отключен." if st.session_state.lang=="ru" else "Дыбыс сөндірілді."
    elif ("включи голос" in message) or ("дыбысты қос" in message):
        st.session_state.tts_enabled = True
        reply = "Голос включен." if st.session_state.lang=="ru" else "Дыбыс қосылды."
    elif any(k in message for k in cabinet_map.keys()):
        for k,v in cabinet_map.items():
            if k in message:
                reply = v
                break
    else:
        for k,v in responses.items():
            if k in message:
                reply = v
                break
    if not reply:
        reply = "Простите, я не понял команду. Напишите 'помощь'." if st.session_state.lang=="ru" else "Кешіріңіз, түсінбедім. 'Көмек' деп жазыңыз."

    st.session_state.messages.append({"role":"bot","text":reply})
    st.session_state.pending_audio = make_tts(reply, lang_code) if st.session_state.tts_enabled else None
    st.rerun()

# ---- Audio Playback ----
if st.session_state.pending_audio:
    st.markdown("""
        <div id="mic-indicator">🎤 <span class="mic">Говорю...</span></div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
        <audio id="bot_audio" autoplay>
            <source src="{st.session_state.pending_audio}" type="audio/mp3">
        </audio>
        <script>
            const audio = document.getElementById('bot_audio');
            audio.onended = () => {{
                const mic = document.getElementById('mic-indicator');
                if (mic) mic.style.display = 'none';
            }};
        </script>
    """, unsafe_allow_html=True)
    st.session_state.pending_audio = None
