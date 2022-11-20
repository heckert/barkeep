import matplotlib.pyplot as plt
import pandas as pd

from bartender.aggregate import Aggregator
from bartender.grid import GridConfig


def adjust_gridconf(gridconf: GridConfig,
                    aggregator: Aggregator) -> GridConfig:
    # TODO
    # Figure out best way to adjust gridconf based on aggregator

    pass


class GridPlot:
    def __init__(self,
                 aggregator: Aggregator,
                 gridconf: GridConfig,
                 include_overall=True):

        self.aggregator = aggregator

        self.fig, self.axes = self._setup_grid(gridconf)

    @staticmethod
    def _setup_grid(gridconf: GridConfig):
        fig, axes = plt.subplots(**gridconf.get_dict())

        return fig, axes

    def show(self):

        self.aggregator.group_percents.plot(kind='barh',
                                            stacked=True,
                                            ax=self.axes)

        plt.show()


def main():

    df = pd.DataFrame({
        'group': list('aabbccabc'),
        'metric': range(1, 10),
        'bins': pd.Categorical(['small', 'small', 'small',
                                'medium', 'medium', 'medium',
                                'large', 'large', 'large'],
                               ordered=True,
                               categories=['small', 'medium', 'large'])
    })

    agg = Aggregator(
        df,
        groupby='group',
        count='bins',
        average='metric'
    )

    gridconf = GridConfig()

    gp = GridPlot(agg, gridconf)

    gp.show()


if __name__ == '__main__':
    main()
