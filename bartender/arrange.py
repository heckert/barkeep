import numpy as np

from bartender import test_df
from bartender.aggregate import Aggregator


def get_arrangement(aggregator: Aggregator,
                    nrows: int, ncols: int) -> np.ndarray:

    """Arrange aggragator's data to match grid prduced by plt.subplots."""

    datasets = [
        aggregator.overall_pct, aggregator.overall_avg,
        aggregator.group_pct, aggregator.group_avg
    ]

    # Remove Nones
    datasets = [dataset for dataset in datasets if dataset is not None]

    return datasets


def main():

    from bartender.grid import get_grid_recipe, GridConfigFactory

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

    get_arrangement(agg, gridconf.nrows, gridconf.ncols)


if __name__ == '__main__':
    main()
