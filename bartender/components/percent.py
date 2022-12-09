import hydra
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd


# hydra.initialize(config_path="../conf", version_base=None)
cfg = hydra.compose(config_name="config")


def annotate_bars(
    ax: matplotlib.axes.Axes,
    annotation_threshold: float = cfg.annotation_threshold
) -> None:

    for p in ax.patches:
        width, height = p.get_width(), p.get_height()
        if width < annotation_threshold:
            continue
        x, y = p.get_xy()

        ax.text(x + width / 2,
                y + height / 2,
                '{:.1f}'.format(width * 100),
                horizontalalignment='center',
                verticalalignment='center',
                fontname=cfg.font.name,
                fontsize=cfg.font.size.s)


def plot(df: pd.DataFrame,
         ax: matplotlib.axes.Axes = None) -> None:

    df.plot(kind='barh', stacked=True, ax=ax)

    # If no ax is passed as parameter,
    # get Axes object manually.
    if ax is None:
        ax = plt.gca()

    annotate_bars(ax)

    ax.set_xlim(0, 1)


if __name__ == '__main__':

    from bartender import test_agg

    plot(test_agg)

    plt.show()
