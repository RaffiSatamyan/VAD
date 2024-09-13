from pydub import AudioSegment
from pydub.playback import play
import zipfile
import tempfile
import wave
import os
import io

class Data:
    def __init__(self, zip_path):
        self.zip_path = zip_path
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            self.file_names = zip_ref.namelist()  # List of files inside the zip archive

    def open_file_from_zip(self, file_name):
        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            file_data = zip_ref.read(file_name)  # Read the file's binary content
            # print(type(file_data))
            return io.BytesIO(file_data)  # Wrap it in BytesIO for wave module compatibility

    def splitted_audios(self, count_of_frames):
        self.final_splitted = []
        for file_name in self.file_names:
            with self.open_file_from_zip(file_name) as file_like:
                with wave.open(file_like, 'rb') as audio_file:
                    # print(f'type(file_like) {type(file_like)}')
                    # print(f'type(audio_file) {type(audio_file)}')
                    n_frames = audio_file.getnframes()
                    for i in range(0, n_frames, count_of_frames):
                        audio_file.setpos(i)
                        frames = audio_file.readframes(count_of_frames)
                        # print(f'type(frames) {type(frames)}')
                        self.final_splitted.append(frames)


d = Data('/content/folder.zip')  # folder contains wav files
d.splitted_audios(50)
