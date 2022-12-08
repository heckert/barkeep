import matplotlib
import matplotlib.pyplot as plt
from typing import Protocol

from bartender import test_df
from bartender.axparse import LegendOutAxparser, AxMap
from bartender.aggregate import Aggregator
from bartender.grid import (GridConfigFactory,
                            get_grid_recipe)


class AxParser(Protocol):
    def get_axmap() -> AxMap:
        ...

    def get_figure() -> matplotlib.figure.Figure:
        ...

    def get_legend_ax() -> matplotlib.axes.Axes:
        ...


class GridPlot:

    def __init__(self,
                 aggregator: Aggregator,
                 parser: AxParser):

        self.aggregator = aggregator

        self.axmap = parser.get_axmap()
        self.fig = parser.get_figure()
        self.legend_ax = parser.get_legend_ax()

    def show(self):
        for key, ax in self.axmap.items():
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

    recipe = get_grid_recipe(agg)
    factory = GridConfigFactory()
    gridconf = factory.build(recipe)

    parser = LegendOutAxparser(gridconf)

    gp = GridPlot(agg, parser)
    gp.show()


if __name__ == '__main__':
    main()
