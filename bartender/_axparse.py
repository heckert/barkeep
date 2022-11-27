import matplotlib
import numpy as np

from typing import Dict, Union


def _parse_axs(
    axs: Union[matplotlib.axes.Axes, np.ndarray],
    nrows: int,
    ncols: int
) -> Dict[str, matplotlib.axes.Axes]:
    """Parse `plt.subplots` result and assign keys to the AxesSubplots.

    Depending on number of rows and columns, plt.subplots returns
    either a single AxesSubplot or a numpy ndarray containing multiple
    subplot objects. This function parses the return object and maps it
    to keys, refering to the corresponding `Aggregator` attributes.
    For details see
    https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots.html

    Arguments:
        axs: Second output elemeent of `plt.subplots`.
        nrows (int): Number of rows in desired plot.
        ncols (int): Number of columns in desired plot.

    Returns:
        dict: A dictionary mapping string keys to the AxesSubplots.
    """

    axs_map = {
        'overall_pct': None,
        'overall_avg': None,
        'group_pct': None,
        'group_avg': None
    }

    if not isinstance(axs, np.ndarray):
        axs_map['group_pct'] = axs

    else:
        if sum([nrows, ncols]) < 4:
            if nrows > 1:
                axs = axs.reshape((2, 1))

            if ncols > 1:
                axs = axs.reshape((1, 2))

        group_axs = axs[-1, ]

        if len(group_axs) > 1:
            axs_map['group_pct'] = group_axs[0]
            axs_map['group_avg'] = group_axs[1]
        else:
            axs_map['group_pct'] = group_axs[0]

        if nrows > 1:
            overall_axs = axs[0, ]

            if len(overall_axs) > 1:
                axs_map['overall_pct'] = overall_axs[0, ]
                axs_map['overall_avg'] = overall_axs[1, ]
            else:
                axs_map['overall_pct'] = overall_axs[0]

    return axs_map
