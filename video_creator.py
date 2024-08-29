import os
import subprocess
import asyncio


class VideoCreator:
    def __init__(self, output_directory):
        self.output_directory = output_directory

    async def create_video(self, seq_folder, base_name):
        os.makedirs(self.output_directory, exist_ok=True)
        output_video_path = os.path.join(self.output_directory, f"{base_name}.mov")
        list_file_path = os.path.join(seq_folder, 'file_list.txt')

        with open(list_file_path, 'w') as list_file:
            for filename in sorted(os.listdir(seq_folder)):
                if filename.endswith('.jpg'):
                    list_file.write(f"file '{os.path.join(seq_folder, filename)}'\n")

        command = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', list_file_path,
            '-c:v', 'mjpeg',
            '-pix_fmt', 'yuvj420p',
            '-r', '24',
            output_video_path
        ]

        try:
            await asyncio.to_thread(subprocess.run, command, check=True)
        except subprocess.CalledProcessError as e:
            return f'Ошибка при создании видео: {str(e)}'
        finally:
            if os.path.exists(list_file_path):
                os.remove(list_file_path)
