from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

from eltypes import log_data, plot_dimensions


def plot(data: log_data, filename: Path, dimensions: plot_dimensions) -> None:
    sns.set_theme("talk", "darkgrid")
    current_palette = sns.color_palette("bright")

    WIDTH, HEIGHT = dimensions
    _, (ax1, ax2) = plt.subplots(1, 2, figsize=(WIDTH, HEIGHT))

    temperature_series = data.iloc[:, 1]
    humidity_series = data.iloc[:, 2]

    sns.lineplot(
        data=temperature_series,
        ax=ax1,
        drawstyle="steps-pre",
        color=current_palette[0]
    )
    sns.lineplot(
        data=humidity_series,
        ax=ax2,
        drawstyle="steps-pre",
        color=current_palette[1]
    )

    plt.savefig(filename)
