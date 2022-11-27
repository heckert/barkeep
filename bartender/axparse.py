import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from dataclasses import dataclass

from bartender.grid import GridConfig
from bartender.utils import _MappableDataClass


@dataclass
class AxMap(_MappableDataClass):
    overall_pct: matplotlib.axes.Axes = None
    overall_avg: matplotlib.axes.Axes = None
    group_pct: matplotlib.axes.Axes = None
    group_avg: matplotlib.axes.Axes = None


class AxParser:
    def __init__(self,
                 gridconf: GridConfig,
                 legend_out: bool):

        self.fig, self.axs = plt.subplots(**gridconf)
        self.nrows = gridconf.nrows
        self.ncols = gridconf.ncols
        self.legend_out = legend_out

        self._axs_is_nparray = isinstance(self.axs, np.ndarray)

    def _reshape_axs(self):
        self.axs = self.axs.reshape(self.nrows, self.ncols)

    def _pop_legend_ax(self) -> matplotlib.axes.Axes:
        gs = self.axs[0, -1].get_gridspec()

        self.legend_ax = self.fig.add_subplot(gs[0:, -1])

        # Remove legend ax
        for ax in self.axs[:, -1]:
            ax.remove()
        self.axs = self.axs[:, :-1]

        # We reserve the AxesSubplot on the right side
        # for the legend, so we treat from now on as
        # if there were one colun less.
        self.ncols -= 1

    def _get_axmap(self) -> AxMap:
        """Parse AxesSubplots from return object of `plt.subplots`.

        Depending on number of rows and columns, plt.subplots returns
        either a single AxesSubplot or a numpy ndarray containing multiple
        subplot objects. This function parses the return object and maps it
        to keys, refering to the corresponding `Aggregator` attributes.
        For details see
        https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots.html
        """

        axmap = {}

        if not isinstance(self.axs, np.ndarray):
            axmap['group_pct'] = self.axs

        else:
            group_axs = self.axs[-1, ]

            if len(group_axs) > 1:
                # axmap['group_pct'] = group_axs[0]
                axmap['group_avg'] = group_axs[1]

            axmap['group_pct'] = group_axs[0]

            if self.nrows > 1:
                overall_axs = self.axs[0, ]

                if len(overall_axs) > 1:
                    # axmap['overall_pct'] = overall_axs[0]
                    axmap['overall_avg'] = overall_axs[1]

                axmap['overall_pct'] = overall_axs[0]

        return AxMap(**axmap)

    def parse(self):
        if self._axs_is_nparray:
            self._reshape_axs()

        if self.legend_out:
            self._pop_legend_ax()
        else:
            self.legend_ax = None

        self.axmap = self._get_axmap()
