import numpy as np

from bartender import test_df
from bartender.aggregate import Aggregator


def get_arrangement(aggregator: Aggregator,
                    nrows: int, ncols: int) -> np.ndarray:

    """Arrange aggragator's data to match grid prduced by plt.subplots."""

    # array = np.zeros([nrows, ncols])
    datasets = [
        aggregator.overall_percent, aggregator.overall_mean,
        aggregator.group_percents, aggregator.group_means
    ]

    datasets = [dataset for dataset in datasets if dataset is not None]

    array = np.array(datasets)
    if sum([nrows, ncols]) > 2:
        array = array.reshape((nrows, ncols))

    print(array)
    print(array.shape)


def main():

    from bartender.grid import get_grid_recipe, GridConfigFactory

    agg = Aggregator(
        test_df,
        groupby='group',
        count='bins',
        # average='metric',
        overall=False
    )

    recipe = get_grid_recipe(agg, has_overall=False, legend_out=False)
    factory = GridConfigFactory(recipe)
    gridconf = factory.build()

    get_arrangement(agg, gridconf.nrows, gridconf.ncols)


if __name__ == '__main__':
    main()
