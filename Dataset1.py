
import matplotlib.pyplot as plt
import scipy.signal as ss
import soundfile as sf
import tensorflow as tf

path1 = "C:\\Users\\User\\PycharmProjects\\VAD\\Data\\dev-clean\\LibriSpeech\\dev-clean\\84\\121123\\84-121123-0003.flac"
path2 = "C:\\Users\\User\\PycharmProjects\\VAD\\Data\\dev-other\\LibriSpeech\\dev-other\\116\\288045\\116-288045-0001.flac"


def process_NoTensor(path):
    data, samplerate = sf.read(path2)
    for i, j in enumerate(data):
        if j != 0.:
            pass
            # print(i, j)
    data = data[8000:32000]
    _, _, spectogram = ss.spectrogram(data, samplerate, nperseg=128, nfft=256)
    return spectogram


# plt.imshow(spectogram)
# plt.show()

def load_wav_16k_mono(path):
    # tf.io.read_file(path)
    # wav, sample_rate = tf.audio.decode_wav
    wav, sample_rate = sf.read(path)
    wav = tf.convert_to_tensor(wav, dtype=tf.float32)
    # wav = tf.squeeze(wav, axis=-1)
    # semple_rate = tf.cast(sample_rate, tf.int64)
    # wav = tfio.audio.resample(wav, rate=semple_rate, rate_out=16000)
    return wav


def process(path):
    wav = load_wav_16k_mono(path)
    wav = wav[:32000]
    spectogram = tf.signal.stft(wav, frame_length=512, frame_step=128)
    spectogram = tf.abs(spectogram)
    spectogram = tf.expand_dims(spectogram, axis=2)
    print(spectogram.shape, type(spectogram))
    # spectogram = spectogram.numpy()
    return spectogram


spectogram1 = process_NoTensor(path2)
spectogram2 = process(path2)
plt.figure(figsize=(60, 40))
# plt.imshow(tf.transpose(spectogram)[0])

plt.imshow(spectogram1)
plt.show()
plt.imshow(spectogram2)
plt.show()
