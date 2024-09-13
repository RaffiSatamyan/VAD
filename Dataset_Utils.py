import io
import wave
import zipfile

import scipy.signal as ss
import soundfile as sf
import tensorflow as tf


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

    def process_NoTensor(self, path):
        data, samplerate = sf.read(path)
        for i, j in enumerate(data):
            if j != 0.:
                pass
                # print(i, j)
        data = data[8000:32000]
        _, _, spectogram = ss.spectrogram(data, samplerate, nperseg=128, nfft=256)
        return spectogram

    def load_wav_16k_mono(self, path):
        # tf.io.read_file(path)
        # wav, sample_rate = tf.audio.decode_wav
        wav, sample_rate = sf.read(path)
        wav = tf.convert_to_tensor(wav, dtype=tf.float32)
        # wav = tf.squeeze(wav, axis=-1)
        # semple_rate = tf.cast(sample_rate, tf.int64)
        # wav = tfio.audio.resample(wav, rate=semple_rate, rate_out=16000)
        return wav

    def process(self, path):
        wav = self.load_wav_16k_mono(path)
        wav = wav[:32000]
        spectogram = tf.signal.stft(wav, frame_length=512, frame_step=128)
        spectogram = tf.abs(spectogram)
        spectogram = tf.expand_dims(spectogram, axis=2)
        print(spectogram.shape, type(spectogram))
        spectogram = spectogram.numpy()
        return spectogram
d = Data('/content/folder.zip')  # folder contains wav files
d.splitted_audios(50)
