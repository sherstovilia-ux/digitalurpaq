import streamlit as st
import edge_tts
import asyncio
import os

st.set_page_config(page_title="Text-to-Speech App", page_icon="🗣️")

st.title("Text-to-Speech с edge-tts 🗣️")
st.write("Введите текст, выберите голос и нажмите кнопку, чтобы услышать озвучку.")

# Список доступных голосов (можно расширять)
voices = [
    "en-US-AriaNeural",
    "en-US-GuyNeural",
    "en-GB-LibbyNeural",
    "en-GB-RyanNeural",
    "ru-RU-DariyaNeural",
    "ru-RU-IlyaNeural"
]

text = st.text_area("Введите текст для озвучивания:")
voice = st.selectbox("Выберите голос:", voices)
output_file = "speech.mp3"

# Функция для TTS
def speak(text: str, voice: str = "en-US-AriaNeural", output_file: str = "speech.mp3"):
    async def tts():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
    asyncio.run(tts())
    return output_file

if st.button("Произнести"):
    if not text.strip():
        st.warning("Введите текст!")
    else:
        with st.spinner("Генерация речи..."):
            speak(text, voice, output_file)
        st.success("Готово! Слушайте ниже:")
        st.audio(output_file, format="audio/mp3")



