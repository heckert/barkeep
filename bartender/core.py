import matplotlib.pyplot as plt
import numpy as np

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

        # Set up grid based on gridconf
        self.fig, axes = plt.subplots(**gridconf)

        self.data2ax_map = self._parse_axes(axes)

    def _parse_axes(self, axes) -> List[tuple]:

        result = []

        if not isinstance(axes, np.ndarray):
            result.append((self.aggregator.group_pct, axes))

        else:
            # TODO
            pass

        return result

    def show(self):
        for data, ax in self.data2ax_map:
            data.plot(kind='barh', stacked=True, ax=ax)

        # for dataset, ax in zip(self.arrangement, self.axes):
        #     dataset.plot(kind='barh', stacked=True, ax=ax)

        plt.show()


def main():

    agg = Aggregator(
        test_df,
        groupby='group',
        count='bins',
        # average='metric',
        overall=False
    )

    recipe = get_grid_recipe(agg, legend_out=False)
    factory = GridConfigFactory(recipe)
    gridconf = factory.build()

    gp = GridPlot(agg, gridconf)

    gp.show()


if __name__ == '__main__':
    main()
