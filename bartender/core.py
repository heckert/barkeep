import matplotlib.pyplot as plt

from bartender import test_df
from bartender.axparse import AxParser
from bartender.aggregate import Aggregator
from bartender.grid import (GridConfig,
                            GridConfigFactory,
                            get_grid_recipe)


class GridPlot:

    def __init__(self,
                 aggregator: Aggregator,
                 gridconf: GridConfig):

        self.aggregator = aggregator

        axparser = AxParser(gridconf)

        self.axmap = axparser.get_axmap()
        self.fig = axparser.get_figure()

    def show(self):
        for key, ax in self.axmap.items():
            if ax is not None:
                data = self.aggregator.__getattribute__(key)
                data.plot(kind='barh', stacked=True, ax=ax)

        plt.show()


def main(legend_out=False):

    agg = Aggregator(
        test_df,
        groupby='group',
        count='bins',
        average='metric',
        average_type='median',
        overall=True
    )

    recipe = get_grid_recipe(agg, legend_out=legend_out)
    factory = GridConfigFactory()
    gridconf = factory.build(recipe)

    gp = GridPlot(agg, gridconf)
    gp.show()


if __name__ == '__main__':
    main()
