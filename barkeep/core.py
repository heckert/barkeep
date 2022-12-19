import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import pathlib

from typing import Optional

from barkeep.axparse import LegendOutAxparser, AxMap
from barkeep.aggregate import Aggregator
from barkeep.grid import GridConfigFactory, get_grid_recipe
from barkeep.colors import get_cmap_colors
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

        # Extract greatest avg for xlim on avg plot
        if aggregator.group_avg is not None:
            self.greatest_avg = round(aggregator.group_avg.iloc[:, 0].max(), 1)

    def show(self,
             save_path: str | pathlib.Path = None,
             **kwargs):

        for key, ax in self.axmap.items():
            if ax is not None:
                data = self.aggregator.__getattribute__(key)
                if 'pct' in key:
                    percent.plot(data, ax=ax, **kwargs)
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

        self._label_axes()

        legend.plot(handles=handles, labels=labels, ax=self.legend_ax)

        plt.tight_layout(pad=2)
        if save_path is not None:
            plt.savefig(save_path)
        plt.show()

    def _label_axes(self):
        # self.axmap['group_pct'].set_xlabel('% of group', fontstyle='italic')

        avg_ax = self.axmap.get('group_avg')
        if avg_ax is not None:
            avg_ax.set_xlabel(self.aggregator.average_type, fontstyle='italic')


def plot(df: pd.DataFrame, *,
         groupby: str,
         count: str,
         average: str = None,
         average_type: str = 'mean',
         overall: bool = True,
         save_path: str | pathlib.Path = None,
         cmap: str = 'Pastel2',
         n_colors_in_cmap: Optional[int] = 8,
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

    if colors is not None:
        gp.show(save_path, color=colors)

    elif n_colors_in_cmap is not None:
        colors = get_cmap_colors(length=gp.aggregator.n_count_categories,
                                 n_colors_in_cmap=n_colors_in_cmap,
                                 name=cmap)
        gp.show(save_path, color=colors)

    else:
        gp.show(save_path, cmap=cmap)


def main():

    path = pathlib.Path(__file__)
    save_path = path.parents[1] / 'images' / 'output.png'

    plot(test_df,
         groupby='group',
         count='bins',
         average='metric',
         average_type='median',
         overall=True,
         save_path=save_path)


if __name__ == '__main__':
    main()
