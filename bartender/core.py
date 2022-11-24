import matplotlib.pyplot as plt
import pandas as pd

from bartender import test_df
from bartender.aggregate import Aggregator
from bartender.grid import (GridConfig,
                            GridConfigFactory,
                            get_grid_recipe)


class GridPlot:
    def __init__(self,
                 aggregator: Aggregator,
                 gridconf: GridConfig,
                 include_overall=True):

        self.aggregator = aggregator
        # Set up grid based on gridconf
        self.fig, self.axes = plt.subplots(**gridconf)

    def show(self):

        self.aggregator.group_percents.plot(kind='barh',
                                            stacked=True,
                                            ax=self.axes)

        plt.show()


def main():

    agg = Aggregator(
        test_df,
        groupby='group',
        count='bins',
        # average='metric'
    )

    recipe = get_grid_recipe(agg, has_overall=False, legend_out=False)
    factory = GridConfigFactory(recipe)
    gridconf = factory.build()

    gp = GridPlot(agg, gridconf)

    gp.show()


if __name__ == '__main__':
    main()
