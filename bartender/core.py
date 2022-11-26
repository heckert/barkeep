import matplotlib.pyplot as plt
import numpy as np

from bartender import test_df
from bartender.aggregate import Aggregator
from bartender.arrange import get_arrangement
from bartender.grid import (GridConfig,
                            GridConfigFactory,
                            get_grid_recipe)


class GridPlot:
    def __init__(self,
                 arrangement: list,
                 gridconf: GridConfig):

        self.arrangement = arrangement
        # Set up grid based on gridconf
        self.fig, self.axes = plt.subplots(**gridconf)
        self.nrows = gridconf.nrows
        self.ncols = gridconf.ncols

    def show(self):
        if isinstance(self.axes, np.ndarray):
            print('Axes is array')
            print(self.axes.shape)

            print(self.axes)
            for i in range(self.nrows):
                for j in range(self.ncols):

                    self.arrangement[i][j].plot(kind='barh',
                                                stacked=True,
                                                ax=self.axes[i, j])
        else:
            print('Axes is no array')
            # TODO: fix for None dimensions
            self.arrangement[0][0].plot(kind='barh',
                                        stacked=True,
                                        ax=self.axes)

        print(self.axes)
        print(self.arrangement)

        # for dataset, ax in zip(self.arrangement, self.axes):
        #     dataset.plot(kind='barh', stacked=True, ax=ax)

        plt.show()


def main():

    agg = Aggregator(
        test_df,
        groupby='group',
        count='bins',
        average='metric',
        overall=True
    )

    recipe = get_grid_recipe(agg, legend_out=False)
    factory = GridConfigFactory(recipe)
    gridconf = factory.build()

    arranged_data = get_arrangement(agg, gridconf.nrows, gridconf.ncols)

    gp = GridPlot(arranged_data, gridconf)

    gp.show()


if __name__ == '__main__':
    main()
