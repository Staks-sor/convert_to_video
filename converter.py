import os
import shutil
import asyncio
from collections import defaultdict
from video_creator import VideoCreator
from utils import collect_image_sequences


class ImageSequenceConverter:
    def __init__(self, input_directory, output_directory):
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.video_creator = VideoCreator(output_directory)

    async def convert(self, progress_callback):
        sequences = collect_image_sequences(self.input_directory)
        total_sequences = len(sequences)

        # Используем asyncio.gather для параллельной обработки
        tasks = [self.process_sequence(seq_name, files) for seq_name, files in sequences.items()]
        results = await asyncio.gather(*tasks)

        for i in range(total_sequences):
            progress_callback(i + 1, total_sequences)  # Обновляем прогресс

    async def process_sequence(self, seq_name, files):
        base_name = seq_name.strip()
        temp_folder = os.path.join(os.getcwd(), f"{base_name}_temp")
        os.makedirs(temp_folder, exist_ok=True)

        # Копирование файлов в временную папку
        await asyncio.gather(
            *[asyncio.to_thread(shutil.copy, file, os.path.join(temp_folder, os.path.basename(file))) for file in files]
        )

        await self.video_creator.create_video(temp_folder, base_name)
        shutil.rmtree(temp_folder)
