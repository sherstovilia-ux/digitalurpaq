import streamlit as st
import asyncio
from pathlib import Path
import edge_tts

# ---------------------------
# Функция синтеза речи
# ---------------------------
async def text_to_speech(text: str, filename: str = "output.mp3", language: str = "ru"):
    """
    text: текст для озвучки
    filename: имя файла для сохранения
    language: 'ru' для русского, 'en' для английского
    """
    if language == "ru":
        voice = "ru-RU-SvetlanaNeural"
    else:
        voice = "en-US-AriaNeural"

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(filename)

# ---------------------------
# Streamlit интерфейс
# ---------------------------
st.set_page_config(page_title="Text-to-Speech TTS", page_icon="🔊")

st.title("🔊 Text-to-Speech (TTS)")

st.markdown("""
Введите текст в поле ниже и выберите язык озвучки.  
После нажатия кнопки аудио будет сгенерировано и проиграно прямо в браузере.
""")

# Ввод текста
user_text = st.text_area("Введите текст для озвучки:")

# Выбор языка
language_option = st.radio("Выберите язык озвучки:", ("Русский", "Английский"))

# Кнопка генерации
if st.button("Сгенерировать"):
    if user_text.strip() == "":
        st.warning("⚠️ Пожалуйста, введите текст!")
    else:
        st.info("⏳ Генерация аудио...")
        audio_file = Path("output.mp3")
        lang_code = "ru" if language_option == "Русский" else "en"
        try:
            # Асинхронный вызов TTS
            asyncio.run(text_to_speech(user_text, str(audio_file), language=lang_code))
            st.success("✅ Аудио готово!")
            st.audio(str(audio_file))
        except Exception as e:
            st.error(f"Произошла ошибка при генерации аудио: {e}")
