import matplotlib
import matplotlib.pyplot as plt
from typing import Protocol

from bartender import test_df
from bartender.axparse import LegendOutAxparser, AxMap
from bartender.aggregate import Aggregator
from bartender.grid import (GridConfigFactory,
                            get_grid_recipe)
from bartender.components import percent, average, legend


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

        if aggregator.group_avg is not None:
            self.greatest_avg = round(aggregator.group_avg.iloc[:, 0].max(), 1)

    def show(self):

        for key, ax in self.axmap.items():
            if ax is not None:
                data = self.aggregator.__getattribute__(key)
                if 'pct' in key:
                    percent.plot(data, ax=ax)
                    # Extract legend handles & labels from group_pct
                    if 'group' in key:
                        handles, labels = ax.get_legend_handles_labels()

                if 'avg' in key:
                    x_lim = round(self.greatest_avg * 1.3, 1)
                    average.plot(data,
                                 ax=ax,
                                 n_rows=self.aggregator.n_groups,
                                 x_lim=x_lim)

                # Remove default legend
                ax.get_legend().remove()

        legend.plot(handles=handles, labels=labels, ax=self.legend_ax)

        plt.show()


def main():

    agg = Aggregator(
        test_df,
        groupby='group',
        count='bins',
        average='metric',
        # average_type='median',
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
