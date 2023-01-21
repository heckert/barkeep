import hydra
import matplotlib
import pandas as pd


with hydra.initialize(config_path="../conf", version_base=None):
    cfg = hydra.compose(config_name="config")


def plot(df: pd.DataFrame,
         ax: matplotlib.axes.Axes,
         x_lim: float) -> None:


    df.plot.barh(ax=ax, color=cfg.style.average.color)
    ax.set_xlim(0, x_lim)
    ax.set_yticks([])
    ax.set_ylabel('')

    for bars in ax.containers:
        ax.bar_label(bars, padding=5, fmt='%.1f')
