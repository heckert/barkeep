import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from typing import List

from bartender import test_df
from bartender.aggregate import Aggregator
from bartender.grid import (GridConfig,
                            GridConfigFactory,
                            get_grid_recipe)


class GridPlot:

    def __init__(self,
                 aggregator: Aggregator,
                 gridconf: GridConfig):

        self.aggregator = aggregator
        self.nrows = gridconf.nrows
        self.ncols = gridconf.ncols

        # Set up grid based on gridconf.
        self.fig, axes = plt.subplots(**gridconf)

        # Extract AxesSubplots from np.ndarray
        # and map them to Aggregator attributes.
        self.axes_map = self._parse_axes(axes, self.nrows, self.ncols)

    @staticmethod
    def _parse_axes(axes, nrows, ncols) -> None:
        """Map keys to AxesSubplots returned by `plt.subplots`"""

        axes_map = {
            'overall_pct': None,
            'overall_avg': None,
            'group_pct': None,
            'group_avg': None
        }

        if not isinstance(axes, np.ndarray):
            axes_map['group_pct'] = axes

        else:
            if sum([nrows, ncols]) < 4:
                if nrows > 1:
                    axes = axes.reshape((2, 1))

                if ncols > 1:
                    axes = axes.reshape((1, 2))

            group_axes = axes[-1, ]

            if len(group_axes) > 1:
                axes_map['group_pct'] = group_axes[0]
                axes_map['group_avg'] = group_axes[1]
            else:
                axes_map['group_pct'] = group_axes[0]

            if nrows > 1:
                overall_axes = axes[0, ]

                if len(overall_axes) > 1:
                    axes_map['overall_pct'] = overall_axes[0, ]
                    axes_map['overall_avg'] = overall_axes[1, ]
                else:
                    axes_map['overall_pct'] = overall_axes[0]

        return axes_map

    def show(self):
        for key, ax in self.axes_map.items():
            if ax is not None:
                data = self.aggregator.__getattribute__(key)
                data.plot(kind='barh', stacked=True, ax=ax)

        plt.show()


def main():

    agg = Aggregator(
        test_df,
        groupby='group',
        count='bins',
        average='metric',
        overall=True
    )

    recipe = get_grid_recipe(agg, legend_out=False)
    factory = GridConfigFactory(recipe)
    gridconf = factory.build()

    gp = GridPlot(agg, gridconf)
    gp.show()


if __name__ == '__main__':
    main()
