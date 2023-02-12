import hydra
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import pathlib

from typing import Union

from barkeep.axparse import LegendOutAxparser, AxMap
from barkeep.aggregate import Aggregator
from barkeep.grid import GridConfigFactory, get_grid_recipe
from barkeep.utils import select_from_center
from barkeep.components import percent, average, legend
from barkeep.datasets import test_df


with hydra.initialize(config_path="./conf", version_base=None):
    cfg = hydra.compose(config_name="config", overrides=['style=ice'])


class GridPlot:
    """
    A class for creating horizontally stacked, annotated barplot.

    This class provides a convenient way to visualize a normalized value count
    of a Pandas dataframe grouped by a column and stacked horizontally. The
    value count can be performed on a grouped metric variable, and the
    aggregate value such as mean or median can be visualized on a second axis.
    The plot also includes a legend.

    Attributes:
        aggregator (Aggregator): An instance of the `Aggregator` class
            representing the data to be plotted.
        axmap (AxMap): A dictionary of matplotlib axes objects used for
            plotting.
        fig (matplotlib.figure.Figure): The figure object that holds the
            grid plot.
        legend_ax (matplotlib.axes.Axes): The axis object for the legend.
        greatest_avg (float): The greatest value of the aggregate value
            (mean or median) or setting the x limit of the plot.
    """

    def __init__(self, *,
                 aggregator: Aggregator,
                 axmap: AxMap,
                 figure: matplotlib.figure.Figure,
                 legend_ax: matplotlib.axes.Axes):

        """
        Initialize a new `GridPlot` instance.

        Args:
            aggregator (Aggregator): An instance of the `Aggregator` class
                representing the data to be plotted.
            axmap (AxMap): A dictionary-like object of matplotlib axes
                objects used for plotting.
            figure (matplotlib.figure.Figure): The figure object that holds
                the grid plot.
            legend_ax (matplotlib.axes.Axes): The axis object for the legend.
        """

        self.aggregator = aggregator

        self.axmap = axmap
        self.fig = figure
        self.legend_ax = legend_ax

        # Extract greatest avg for xlim on avg plot
        if aggregator.group_avg is not None:
            self.greatest_avg = round(aggregator.group_avg.iloc[:, 0].max(), 1)

    def show(self,
             save_path: Union[str, pathlib.Path] = None,
             **kwargs):

        """
        Show the grid plot.

        Args:
            save_path (Union[str, pathlib.Path], optional): The path to
                save the plot as an image. If not specified, the plot
                will be displayed but not saved.
            **kwargs: Additional arguments to pass to the plotting functions.

        """

        for key, ax in self.axmap.items():
            if ax is not None:
                data = self.aggregator.__getattribute__(key)
                if 'pct' in key:
                    percent.plot(data, ax=ax, **kwargs)
                    # Extract legend handles & labels from group_pct
                    if 'group' in key:
                        handles, labels = ax.get_legend_handles_labels()

                if 'avg' in key:
                    x_lim = round(self.greatest_avg * 1.5, 1)
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
         save_path: Union[str, pathlib.Path] = None,
         colors: list = cfg.colors.palette,
         index_ascending: bool = False,
         order_pct_by: str = 'index',
         order_pct_ascending: bool = True):

    """
    Plot a grid plot based on the input data.

    Args:
        df (pd.DataFrame): DataFrame to use for plotting.
        groupby (str): Column name to group the data by.
        count (str): Column name to count the data by.
        average (str, optional): Column name to average the data by.
            If None, no averaging is performed. Defaults to None.
        average_type (str, optional): Type of average to calculate.
            Can be 'mean' or 'median'. Defaults to 'mean'.
        overall (bool, optional): If True, include an overall plot.
            Defaults to True.
        save_path (Union[str, pathlib.Path], optional): Path to save the plot.
            If None, the plot is not saved. Defaults to None.
        colors (list, optional): List of colors to use for the plot. Defaults
            to the colors specified in the `cfg.colors.palette` configuration.
        index_ascending (bool, optional): If True, sort index in ascending
            order. Defaults to False.
        order_pct_by (str, optional): Order percentages by index or values.
            Defaults to 'index'.
        order_pct_ascending (bool, optional): If True, sort the percentage in
            ascending order. Defaults to True.
    """

    agg = Aggregator(
        df,
        groupby=groupby,
        count=count,
        average=average,
        average_type=average_type,
        overall=overall,
        index_ascending=index_ascending,
        order_pct_by=order_pct_by,
        order_pct_ascending=order_pct_ascending
    )

    recipe = get_grid_recipe(agg)
    factory = GridConfigFactory()
    gridconf = factory.build(recipe)

    parser = LegendOutAxparser(gridconf)

    gp = GridPlot(aggregator=agg,
                  axmap=parser.get_axmap(),
                  figure=parser.get_figure(),
                  legend_ax=parser.get_legend_ax())

    # Get colors
    color_indices = select_from_center(agg.n_count_categories,
                                       len(colors))
    selected_colors = [colors[i] for i in color_indices]

    gp.show(save_path, color=selected_colors)


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
