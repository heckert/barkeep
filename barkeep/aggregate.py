import pandas as pd
from typing import Union, Iterable


# TODO:
# * implement ordering for counts and groups

class Aggregator:
    """Provides all aggregates for the plot"""

    VALID_AVG_TYPES = {
        'mean',
        'median'
    }

    VALID_ORDER_COUNT_BY = {
        'value',
        'index'
    }

    def __init__(self,
                 df: pd.DataFrame, *,
                 groupby: str,
                 count: str,
                 average: str = None,
                 average_type: str = 'mean',
                 overall: bool = True,
                 index_ascending: bool = False,
                 order_count_by: Union[str, Iterable] = 'value',
                 order_count_asc: bool = False):

        self.df = df
        self.grouper = df.groupby(groupby)
        self.count = count
        self.average = average

        if average_type not in self.VALID_AVG_TYPES:
            raise ValueError(
                'average_type not in '
                f'{", ".join(self.VALID_AVG_TYPES)}'
            )

        self.average_type = average_type
        self.overall = overall
        self.index_ascending = index_ascending
        self.ordering = df[self.count].value_counts(normalize=True).index

    @property
    def overall_pct(self) -> pd.DataFrame:

        if not self.overall:
            return

        result = pd.DataFrame(
            self.df[self.count].value_counts(normalize=True)
        ).transpose()

        result.index = ['Overall']

        return result

    @property
    def overall_avg(self) -> pd.DataFrame:
        if not self.overall:
            return

        if self.average is None:
            return

        avg_method = self.df[self.average] \
            .__getattr__(self.average_type)

        return pd.DataFrame({
            self.average_type: [avg_method()]
        }, index=['Overall'])

    @property
    def group_pct(self) -> pd.DataFrame:

        result = self.grouper[self.count] \
            .value_counts(normalize=True) \
            .unstack() \
            .fillna(0) \
            .sort_index(ascending=self.index_ascending)

        result.index.name = None

        return result

    @property
    def group_avg(self) -> pd.DataFrame:
        if self.average is None:
            return

        return self.grouper.agg(**{
            self.average_type: (self.average, self.average_type)
        }).sort_index(ascending=self.index_ascending)

    @property
    def n_groups(self) -> int:
        return len(self.group_pct)

    @property
    def n_count_categories(self) -> int:
        return len(self.group_pct.columns)
