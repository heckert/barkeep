import matplotlib.pyplot as plt
import pandas as pd

from bartender.aggregate import Aggregator
from bartender.grid import GridConfig, GridConfigFactory


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

    factory = GridConfigFactory()
    # TODO: Fit Factory to aggregator
    gridconf = factory.get_grid_config()

    gp = GridPlot(agg, gridconf)

    gp.show()


if __name__ == '__main__':
    main()
