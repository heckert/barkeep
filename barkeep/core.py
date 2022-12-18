import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import pathlib

from barkeep.axparse import LegendOutAxparser, AxMap
from barkeep.aggregate import Aggregator
from barkeep.grid import GridConfigFactory, get_grid_recipe
from barkeep.colors import get_colors
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
        self.colors = None

        if aggregator.group_avg is not None:
            self.greatest_avg = round(aggregator.group_avg.iloc[:, 0].max(), 1)

    def set_colors_by_cmap(self, cmap: str) -> None:
        self.colors = get_colors(
            n_colors=self.aggregator.n_count_categories,
            cmap=cmap
        )

    def show(self, save_path: str | pathlib.Path = None):

        for key, ax in self.axmap.items():
            if ax is not None:
                data = self.aggregator.__getattribute__(key)
                if 'pct' in key:
                    percent.plot(data, ax=ax, color=self.colors)
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

        plt.tight_layout(pad=2)
        if save_path is not None:
            plt.savefig(save_path)
        plt.show()


def plot(df: pd.DataFrame, *,
         groupby: str,
         count: str,
         average: str = None,
         average_type: str = 'mean',
         overall: bool = True,
         save_path: str | pathlib.Path = None,
         cmap: str = 'Pastel1',
         colors: list = None):

    agg = Aggregator(
        df,
        groupby=groupby,
        count=count,
        average=average,
        average_type=average_type,
        overall=overall,
    )

    recipe = get_grid_recipe(agg)
    factory = GridConfigFactory()
    gridconf = factory.build(recipe)

    parser = LegendOutAxparser(gridconf)

    gp = GridPlot(aggregator=agg,
                  axmap=parser.get_axmap(),
                  figure=parser.get_figure(),
                  legend_ax=parser.get_legend_ax())

    if cmap is not None:
        gp.set_colors_by_cmap(cmap)
    if colors is not None:
        gp.colors = colors

    gp.show(save_path)


def main():

    path = pathlib.Path(__file__)
    save_path = path.parents[1] / 'images' / 'output.png'

    plot(test_df,
         groupby='group',
         count='bins',
         average='metric',
         # average_type='median',
         overall=True,
         save_path=save_path)


if __name__ == '__main__':
    main()
