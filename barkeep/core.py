import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from barkeep.axparse import LegendOutAxparser, AxMap
from barkeep.aggregate import Aggregator
from barkeep.grid import GridConfigFactory, get_grid_recipe
from barkeep.components import percent, average, legend
from barkeep.datasets import test_df


class GridPlot:

    def __init__(self, *,
                 aggregator: Aggregator,
                 axmap: AxMap,
                 figure: matplotlib.figure.Figure,
                 legend_ax: matplotlib.axes.Axes):

        self.aggregator = aggregator

        self.axmap = axmap
        self.fig = figure
        self.legend_ax = legend_ax

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
                    x_lim = round(self.greatest_avg * 1.35, 1)
                    average.plot(data,
                                 ax=ax,
                                 x_lim=x_lim)

                if 'overall' in key:
                    # ax.get_xaxis().set_ticks([])
                    pass

                # Remove default legend
                ax.get_legend().remove()

        legend.plot(handles=handles, labels=labels, ax=self.legend_ax)

        plt.show()


def plot(df: pd.DataFrame, *,
         groupby: str,
         count: str,
         average: str = None,
         average_type: str = 'mean',
         overall: bool = True):

    agg = Aggregator(
        df,
        groupby=groupby,
        count=count,
        average=average,
        average_type=average_type,
        overall=overall
    )

    recipe = get_grid_recipe(agg)
    factory = GridConfigFactory()
    gridconf = factory.build(recipe)

    parser = LegendOutAxparser(gridconf)

    gp = GridPlot(aggregator=agg,
                  axmap=parser.get_axmap(),
                  figure=parser.get_figure(),
                  legend_ax=parser.get_legend_ax())
    gp.show()


def main():

    plot(test_df,
         groupby='group',
         count='bins',
         average='metric',
         # average_type='median',
         overall=True)


if __name__ == '__main__':
    main()
