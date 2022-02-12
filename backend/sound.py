from typing import Callable
import pyaudio
import numpy as np

# PyAudio INIT:
CHUNK = 1024  # Samples: 1024,  512, 256, 128
RATE = 44100  # Equivalent to Human Hearing at 40 kHz
INTERVAL = 1  # Sampling Interval in Seconds ie Interval to listen


def init_stream(cb: Callable[[np.array], None]) -> pyaudio.Stream:
    def _cb(in_data, *_args):
        cb(np.frombuffer(in_data, dtype=np.int32))
        return (in_data, pyaudio.paContinue)

    pa = pyaudio.PyAudio()
    return pa.open(
        format=pyaudio.paInt32,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
        stream_callback=_cb,
    )
