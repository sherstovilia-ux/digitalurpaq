import streamlit as st
from gtts import gTTS
import io
import base64

# ---- Page setup ----
st.set_page_config(page_title="Digital Urpaq Support Bot", layout="wide")

# ---- CSS ----
st.markdown("""
<style>
header, footer, #MainMenu {visibility: hidden;}
.banner img { width: 100%; max-height: 250px; object-fit: cover; border-radius: 10px; }
.chat-bubble { border-radius: 20px; padding: 10px 15px; margin: 8px 0; max-width: 80%; word-wrap: break-word; display: flex; justify-content: space-between; align-items: center; }
.user-bubble {background-color: #DCF8C6; align-self: flex-end;}
.bot-bubble {background-color: #F1F0F0; align-self: flex-start;}
.chat-container {display: flex; flex-direction: column;}
.tts-icon { cursor: pointer; margin-left: 10px; font-size: 20px; }
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
            "text": "Тіл қазақ тіліне ауыстырылды." if st.session_state.lang=="kk"
                    else "Язык переключён на русский."
        })

# ---- Responses ----
responses_ru = {
    "контакты": "Адрес: ул. Жамбыла Жабаева 55А, Петропавловск. Телефон: 8 7152 34-02-40. Также смотрите сайт: https://digitalurpaq.edu.kz/ru/kkbajlanysrukontakty.html",
    "актовый зал": "В здании три актовых зала: первый — над лобби, второй — в левом крыле, третий — в учебном блоке рядом с IT-кабинетами.",
    "помощь": "Доступные команды: кабинет <название>, контакты, актовый зал, запись, помощь.",
    "запись": "Онлайн-форма: https://docs.google.com/forms/d/e/1FAIpQLSc5a5G0CY5XuOCpVHcg7qTDBdEGGkyVEjuBwihpfHncDCqv2A/viewform",
}
responses_kk = {
    "байланыс": "Мекенжай: Жамбыл Жабаев көш., 55А, Петропавл. Телефон: 8 7152 34-02-40. Толығырақ: https://digitalurpaq.edu.kz/kk/kkbajlanysrukontakty.html",
    "акт залы": "Ғимаратта үш акт залы бар: біріншісі — вестибюль үстінде, екіншісі — сол қанатта, үшіншісі — IT кабинеттерінің жанындағы оқу блокында.",
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

# ---- TTS Function ----
def tts_audio_bytes(text, lang_code="ru"):
    # gTTS не поддерживает казахский
    if lang_code == "kk":
        return None
    tts = gTTS(text=text, lang="ru")
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.read()

def tts_autoplay_html(audio_bytes):
    if not audio_bytes:
        return
    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
    html_code = f"""
    <audio autoplay>
        <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
    </audio>
    """
    st.components.v1.html(html_code, height=50)

# ---- Chat UI ----
st.title("🤖 Digital Urpaq Support Bot")
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for i, msg in enumerate(st.session_state.messages):
        bubble = "user-bubble" if msg["role"] == "user" else "bot-bubble"
        if msg["role"] == "bot" and st.session_state.tts_enabled:
            col1, col2 = st.columns([0.9, 0.1])
            with col1:
                st.markdown(f'<div class="chat-bubble {bubble}">{msg["text"]}</div>', unsafe_allow_html=True)
            with col2:
                if st.button("🔊", key=f"tts_{i}"):
                    lang_code = "ru" if st.session_state.lang=="ru" else "kk"
                    audio_bytes = tts_audio_bytes(msg["text"], lang_code)
                    if audio_bytes:
                        st.audio(audio_bytes, format="audio/mp3")
                    else:
                        st.info("TTS недоступен для казахского / Қазақ тіліне қолжетімді емес")
        else:
            st.markdown(f'<div class="chat-bubble {bubble}">{msg["text"]}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---- Input Form ----
with st.form(key="user_input_form"):
    placeholder = "Сұрағыңызды жазыңыз..." if st.session_state.lang == "kk" else "Ваш вопрос:"
    user_input = st.text_input(placeholder, placeholder=placeholder)
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
    if "кабинет" in message or "кабинеті" in message:
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

    # ---- Try autoplay (may be blocked by browser) ----
    if st.session_state.tts_enabled and reply:
        audio_bytes = tts_audio_bytes(reply, lang_code)
        tts_autoplay_html(audio_bytes)

# ---- TTS Toggle ----
st.checkbox("Включить TTS / TTS қосу", value=st.session_state.tts_enabled, key="tts_enabled")


