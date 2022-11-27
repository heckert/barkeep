import matplotlib.pyplot as plt

from bartender import test_df
from bartender._axparse import _parse_axs
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
        self.fig, axs = plt.subplots(**gridconf)

        # Extract axsSubplots from np.ndarray
        # and map them to Aggregator attributes.
        self.axs_map = _parse_axs(axs, self.nrows, self.ncols)

    def show(self):
        for key, ax in self.axs_map.items():
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
        average_type='median',
        overall=True
    )

    recipe = get_grid_recipe(agg, legend_out=False)
    factory = GridConfigFactory(recipe)
    gridconf = factory.build()

    gp = GridPlot(agg, gridconf)
    gp.show()


if __name__ == '__main__':
    main()
