import streamlit as st

st.set_page_config(
    page_title="Digital Urpaq Support Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Hide Streamlit UI elements ---
st.markdown("""
    <style>
        #MainMenu, footer, header, [data-testid="stToolbar"] {visibility: hidden !important;}
        .block-container {padding-top: 1rem; padding-bottom: 1rem;}
        
        /* Chat bubble styles */
        .chat-bubble {
            padding: 10px 16px;
            border-radius: 18px;
            margin: 5px 0;
            max-width: 85%;
            word-wrap: break-word;
        }
        .bot {
            background-color: #f1f0f0;
            color: #000;
            text-align: left;
            border-top-left-radius: 0;
            margin-right: auto;
        }
        .user {
            background-color: #0078ff;
            color: white;
            text-align: right;
            border-top-right-radius: 0;
            margin-left: auto;
        }
        .chat-container {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        input, textarea {
            font-size: 16px !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center;'>🤖 Digital Urpaq Support Bot</h2>", unsafe_allow_html=True)
st.write("💬 Задайте вопрос о кабинетах, контактах или записи:")

# --- Responses ---
responses = {
    "контакты": "📞 Адрес: ул. Жамбыла Жабаева 55А, Петропавловск. Телефон: 8 7152 34-02-40. Также смотрите сайт: https://digitalurpaq.edu.kz/ru/kkbajlanysrukontakty.html",
    "актовый зал": "🎭 В здании три актовых зала: первый — над лобби (через правые или левые лестницы), второй — в левом крыле, где раздевалка, третий — в учебном блоке рядом с IT-кабинетами.",
    "помощь": "🧭 Доступные команды: кабинет <название>, контакты, актовый зал, запись, помощь.",
    "запись": "🗓️ Онлайн-форма: https://docs.google.com/forms/d/e/1FAIpQLSc5a5G0CY5XuOCpVHcg7qTDBdEGGkyVEjuBwihpfHncDCqv2A/viewform",
}

cabinet_map = {
    "лего": "🧩 Кабинет LEGO-конструирования — 1 этаж, правое крыло, третий справа от входа.",
    "физика": "⚛️ Кабинет Физики — левое крыло, 3 этаж, рядом с Астрономией.",
    "шахматы": "♟️ Кабинет Шахмат — правое крыло, 1 этаж, рядом с Лего.",
    "биология": "🧬 Кабинет Биологии — 3 этаж, центральная часть, блок Д1.",
    "электрика": "💡 Кабинет Электротехники — 2 этаж, правое крыло.",
    "дроны": "🚁 Кабинет Дронов — 2 этаж, правое крыло.",
    "3д моделирования": "🖨️ Кабинет 3D-моделирования — 2 этаж, IT-блок, правое крыло.",
    "роботы": "🤖 Кабинет Робототехники — 2 этаж, левое крыло, конец коридора.",
    "вр": "🕶️ VR-кабинет — 2 этаж, правое крыло.",
    "програмирование": "💻 Кабинет Программирования — 2 этаж, дальнее правое крыло.",
    "анимирование": "🎞️ Кабинет Анимирования — 2 этаж, правое крыло.",
    "экономика": "💰 Кабинет Экономики — 2 этаж, правое крыло.",
    "рисование": "🎨 Кабинет Рисования — 3 этаж, правое крыло.",
}

# --- Chat memory (keeps messages during the session) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display chat history ---
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for msg in st.session_state.messages:
    role_class = "user" if msg["is_user"] else "bot"
    st.markdown(f"<div class='chat-bubble {role_class}'>{msg['text']}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- Input box ---
user_input = st.text_input("✏️ Ваш вопрос:")

if st.button("Отправить"):
    if user_input.strip():
        message = user_input.lower()
        st.session_state.messages.append({"text": user_input, "is_user": True})
        reply = None

        if "кабинет" in message:
            for name, location in cabinet_map.items():
                if name in message:
                    reply = location
                    break
            if not reply:
                reply = "🏢 Уточните название кабинета."
        else:
            for k, v in responses.items():
                if k in message:
                    reply = v
                    break

        if not reply:
            reply = "❓ Простите, я не понял команду. Напишите 'помощь'."

        st.session_state.messages.append({"text": reply, "is_user": False})
        st.experimental_rerun()

