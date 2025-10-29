import streamlit as st
import pyttsx3
import tempfile
import os

# Инициализация движка pyttsx3
engine = pyttsx3.init()

st.title("Тест синтеза речи с pyttsx3")

# Ввод текста пользователем
text = st.text_area("Введите текст для синтеза речи:")

# Кнопка для генерации речи
if st.button("Синтезировать"):
    if text.strip() == "":
        st.warning("Введите текст для озвучивания!")
    else:
        # Создаем временный файл
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tmp_file_name = tmp_file.name
        tmp_file.close()

        # Сохраняем речь в файл
        engine.save_to_file(text, tmp_file_name)
        engine.runAndWait()

        # Проигрываем в Streamlit
        audio_file = open(tmp_file_name, "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3")

        # Удаляем временный файл
        os.remove(tmp_file_name)

