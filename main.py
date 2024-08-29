import os
import streamlit as st
import asyncio
from converter import ImageSequenceConverter


def main():
    st.title("Конвертер изображений в видео")

    # Уникальные ключи для текстовых полей
    input_dir = st.text_input("Введите путь к директории с изображениями", key="input_dir")
    output_dir = st.text_input("Введите путь к директории для сохранения видео", key="output_dir")

    if st.button("Конвертировать"):
        if os.path.isdir(input_dir) and os.path.isdir(output_dir):
            progress_bar = st.progress(0)

            async def run_conversion():
                converter = ImageSequenceConverter(input_dir, output_dir)

                def progress_callback(current, total):
                    progress_bar.progress(current / total)  # обновляем прогресс

                await converter.convert(progress_callback)
                st.success("Конвертация завершена успешно!")

            asyncio.run(run_conversion())  # Запускаем асинхронную задачу
        else:
            st.error("Пожалуйста, убедитесь, что обе директории действительны.")


if __name__ == "__main__":
    main()
