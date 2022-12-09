import hydra
import matplotlib
import pandas as pd

from decimal import Decimal
from typing import Tuple

# hydra.initialize(config_path="../conf", version_base=None)
cfg = hydra.compose(config_name="config")


def extract_spacing_from_ax(ax: matplotlib.axes.Axes,
                            n_rows: int) -> Tuple:
    # X SPACE DEPENDS ON SCALE OF X-AXIS
    # the smaller the max val, the smaller the space
    max_val = float(ax.get_xlim()[1])
    ten_to_str = '{:2E}'.format(Decimal(max_val))
    ten_to = int(ten_to_str.split('E')[1])
    x_spc_fctr = 10 ** ten_to

    # Y SPACE DEPENDS ON NUMBER OF ROWS
    # the more rows, the smaller the space
    y_spc_fctr = (n_rows * .25) ** -1

    x_space = .15 * x_spc_fctr
    y_space = .15 * y_spc_fctr

    return (x_space, y_space)


def plot(df: pd.DataFrame,
         ax: matplotlib.axes.Axes,
         n_rows: int,
         x_lim: float) -> None:

    df.plot(kind='barh', stacked=True, ax=ax)
    ax.set_xlim(0, x_lim)
    ax.set_yticks([])
    ax.set_ylabel('')

    for p in ax.patches:

        text = str(round(p.get_width(), 1))
        x_space, y_space = extract_spacing_from_ax(ax, n_rows=n_rows)

        if p.get_width() < 0:
            # increase space for multiple digit negative values
            x = p.get_width() - 15 * len(str(int(round(p.get_width(), 0))))
        else:
            x = p.get_width() + x_space

        y = p.get_y() + y_space

        ax.text(x, y,
                text,
                fontname=cfg.font.name,
                fontsize=cfg.font.size.s)
