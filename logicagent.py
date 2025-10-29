import streamlit as st
import edge_tts
import asyncio
from pathlib import Path

st.set_page_config(page_title="Text-to-Speech Demo", page_icon="🔊")

st.title("🔊 Text-to-Speech Demo with edge-tts")

# Ввод текста пользователем
text_input = st.text_area("Введите текст для озвучивания:")

voice_options = [
    "en-US-AriaNeural",
    "en-US-GuyNeural",
    "en-GB-LibbyNeural",
    "ru-RU-DariyaNeural"
]

voice_choice = st.selectbox("Выберите голос:", voice_options)

output_file = Path("output.mp3")

async def tts(text, voice, filename):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(filename)

if st.button("Сгенерировать речь"):
    if not text_input.strip():
        st.warning("Введите текст для озвучивания!")
    else:
        st.info("Генерируем речь...")
        asyncio.run(tts(text_input, voice_choice, output_file))
        st.success("Готово! 🎉")
        st.audio(str(output_file), format="audio/mp3")
