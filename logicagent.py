import streamlit as st
from google.cloud import texttospeech
import io

# ---- Page setup ----
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
.chat-container {display: flex; flex-direction: column; max-height: 500px; overflow-y: auto;}
</style>
""", unsafe_allow_html=True)

# ---- Banner ----
st.markdown("""
<div class="banner">
    <img src="https://s12.gifyu.com/images/b36xz.gif" alt="Banner">
</div>
""", unsafe_allow_html=True)

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

# ---- Language Switcher ----
col1, col2 = st.columns([4, 1])
with col2:
    if st.button("Қаз / Рус"):
        st.session_state.lang = "kk" if st.session_state.lang == "ru" else "ru"
        st.session_state.messages.append({
            "role": "bot",
            "text": "Тіл қазақ тіліне ауыстырылды." if st.session_state.lang == "kk"
            else "Язык переключён на русский."
        })
        st.experimental_rerun()

# ---- Responses ----
responses_ru = {
    "контакты": "Адрес: ул. Жамбыла Жабаева 55А, Петропавловск. Телефон: 8 7152 34-02-40. Также смотрите сайт: https://digitalurpaq.edu.kz/ru/kkbajlanysrukontakty.html",
    "актовый зал": "В здании три актовых зала: первый — над лобби, второй — в левом крыле, третий — в учебном блоке рядом с IT-кабинетами.",
    "помощь": "Доступные команды: кабинет <название>, контакты, актовый зал, запись, помощь.",
    "запись": "Онлайн-форма: https://docs.google.com/forms/d/e/1FAIpQLSc5a5G0CY5XuOCpVHcg7qTDBdEGGkyVEjuBwihpfHncDCqv2A/viewform",
}
responses_kk = {
    "байланыс": "Мекенжай: Жамбыл Жабаев көш., 55А, Петропавл. Телефон: 8 7152 34-02-40. Толығырақ: https://digitalurpaq.edu.kz/kk/kkbajlanysrukontakty.html",
    "акт залы": "Ғимаратта үш акт залы бар: біріншісі — вестибюль үстінде, екіншісі — сол қанатта, үшіншісі — IT кабинеттерінің жанындағы оқу блогында.",
    "көмек": "Қолжетімді командалар: кабинет <атауы>, байланыс, акт залы, жазылу, көмек.",
    "жазылу": "Онлайн нысан: https://docs.google.com/forms/d/e/1FAIpQLSc5a5G0CY5XuOCpVHcg7qTDBdEGGkyVEjuBwihpfHncDCqv2A/viewform",
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

# ---- Google Cloud TTS ----
def make_tts_bytes(text: str, lang_code: str):
    client = texttospeech.TextToSpeechClient()
    language = "kk-KZ" if lang_code=="kk" else "ru-RU"
    voice_name = "kk-KZ-Standard-A" if lang_code=="kk" else "ru-RU-Standard-D"
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
    return io.BytesIO(response.audio_content)

# ---- Chat UI с автопрокруткой ----
st.title("🤖 Digital Urpaq Support Bot")
chat_placeholder = st.empty()

with chat_placeholder.container():
    st.markdown('<div class="chat-container" id="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        bubble = "user-bubble" if msg["role"] == "user" else "bot-bubble"
        st.markdown(f'<div class="chat-bubble {bubble}">{msg["text"]}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("""
        <script>
            var chatDiv = document.getElementById("chat-container");
            if (chatDiv) { chatDiv.scrollTop = chatDiv.scrollHeight; }
        </script>
    """, unsafe_allow_html=True)

# ---- Input Form ----
placeholder = "Сұрағыңызды жазыңыз..." if st.session_state.lang == "kk" else "Ваш вопрос:"
with st.form(key="chat_form"):
    user_input = st.text_input(" ", placeholder=placeholder, key="user_input")
    submit_button = st.form_submit_button("Отправить")

# ---- Logic ----
if submit_button and user_input:
    msg = user_input.strip()
    st.session_state.messages.append({"role": "user", "text": msg})
    message = msg.lower()
    reply = None

    if st.session_state.lang == "ru":
        responses = responses_ru
        cabinet_map = cabinet_map_ru
        lang_code = "ru"
    else:
        responses = responses_kk
        cabinet_map = cabinet_map_kk
        lang_code = "kk"

    # Кабинеты
    if "кабинет" in message:
        found = False
        for k, v in cabinet_map.items():
            if k in message:
                reply = v
                found = True
                break
        if not found:
            reply = "Уточните, пожалуйста, какой кабинет?" if lang_code=="ru" else "Қай кабинетті қажет ететінін нақтылаңыз?"
    else:
        found = False
        for k, v in responses.items():
            if k in message:
                reply = v
                found = True
                break
        if not found:
            reply = "Простите, я не понял команду. Напишите 'помощь'." if lang_code=="ru" else "Кешіріңіз, түсінбедім. 'Көмек' деп жазыңыз."

    st.session_state.messages.append({"role": "bot", "text": reply})

    # ---- Авто-TTS ----
    if st.session_state.tts_enabled:
        audio_bytes = make_tts_bytes(reply, lang_code)
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

    st.session_state.user_input = ""
    st.experimental_rerun()

