import pyqtgraph as pg
import numpy as np

from sound import init_stream


# Data config
DATA_SIZE = 1000

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)


def main():
    app = pg.mkQApp()
    plot = pg.PlotWidget(title="Updating plot")
    curve = plot.plot(pen="y")

    data = np.zeros(DATA_SIZE)
    i = 0

    def update(data_in: np.array):
        nonlocal i
        data[i] = np.max(data_in)
        curve.setData(data)
        i = (i + 1) % DATA_SIZE

    stream = init_stream(update)

    plot.show()

    stream.start_stream()
    app.exec()


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
