from typing import Callable
import pyaudio
import numpy as np
import pyqtgraph as pg
import numpy as np

# PyAudio INIT:
CHUNK = 1024  # Samples: 1024,  512, 256, 128
RATE = 44100  # Equivalent to Human Hearing at 40 kHz
INTERVAL = 1  # Sampling Interval in Seconds ie Interval to listen

# Data config
DATA_SIZE = 1000

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)


def _init_stream(cb: Callable[[np.array], None]) -> pyaudio.Stream:

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


def main():
    app = pg.mkQApp()
    plot = pg.PlotWidget(title="Updating plot")
    curve = plot.plot(pen='y')

    data = np.zeros(DATA_SIZE)
    i = 0
    def update(data_in: np.array):
        nonlocal i
        data[i] = np.max(data_in)
        curve.setData(data)
        i = (i + 1) % DATA_SIZE

    stream = _init_stream(update)

    plot.show()

    stream.start_stream()
    app.exec()


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    main()
