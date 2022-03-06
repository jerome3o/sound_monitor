import math
from typing import Callable
import pyaudio
import numpy as np

# PyAudio INIT:
CHUNK = 1024 * 4  # Samples: 1024,  512, 256, 128
RATE = 44100  # Equivalent to Human Hearing at 40 kHz
FREQ = np.arange((CHUNK / 2) + 1) / (float(CHUNK) / RATE)
TIME_STEP = CHUNK / RATE

BREAK_POINTS = np.logspace(math.log10(20), 5, 12 * 3 + 1)
BREAK_POINTS = BREAK_POINTS[: sum(BREAK_POINTS <= np.max(FREQ)) + 1]

WAVE_MAX = 2**16


def init_stream(cb: Callable[[np.array], None]) -> pyaudio.Stream:
    def _cb(in_data, *_args):
        cb(np.frombuffer(in_data, dtype=np.int16))
        return (in_data, pyaudio.paContinue)

    pa = pyaudio.PyAudio()

    return pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
        stream_callback=_cb,
    )


def calculate_psd(data: np.array, win: np.array = None):

    if win is None:
        win = np.hanning(len(data))

    # normalized, windowed frequencies in data chunk
    spec = np.fft.rfft(data * win) / CHUNK

    # get magnitude
    psd = abs(spec)

    # convert to dB scale
    psd = 20 * np.log10(psd)

    output = []
    value = 1.0
    for f_0, f_1 in zip(np.concatenate([[0], BREAK_POINTS[:-1]]), BREAK_POINTS):
        if sum((FREQ >= f_0) & (FREQ < f_1)) > 0:
            value = np.max(psd[(FREQ >= f_0) & (FREQ < f_1)])
            
        output.append(value)
    return output
        

def calculate_max_amplitude(data: np.array):
    return np.mean(abs(data)) / WAVE_MAX
