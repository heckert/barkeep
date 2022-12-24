import pandas as pd


class Aggregator:
    """Provides all aggregates for the plot."""

    VALID_AVG_TYPES = {
        'mean',
        'median'
    }

    VALID_ORDER_PCT_BYS = {
        'index',
        'values'
    }

    def __init__(self,
                 df: pd.DataFrame, *,
                 groupby: str,
                 count: str,
                 average: str = None,
                 average_type: str = 'mean',
                 overall: bool = True,
                 index_ascending: bool = False,
                 order_pct_by: str = 'index',
                 order_pct_ascending: bool = True):

        self.df = df
        self.grouper = df.groupby(groupby)
        self.count = count
        self.average = average
        self.average_type = average_type
        self.overall = overall
        self.index_ascending = index_ascending
        self.ordered_columns = self._set_pct_ordering(
            by=order_pct_by,
            ascending=order_pct_ascending)

        for input_, valids in {
            average_type: self.VALID_AVG_TYPES,
            order_pct_by: self.VALID_ORDER_PCT_BYS
        }.items():
            self._check_inputs(input_, valids)

    @staticmethod
    def _check_inputs(input_, valids: set) -> None:
        if input_ not in valids:
            raise ValueError(
                f'{input_} not in '
                f'({", ".join(valids)})')

    def _set_pct_ordering(self, by: str, ascending: bool) -> pd.Index:

        overall_value_counts = self.df[self.count].value_counts(normalize=True)

        if by == "index":
            return overall_value_counts \
                    .sort_index(ascending=ascending) \
                    .index

        if by == "values":
            return overall_value_counts \
                    .sort_values(ascending=ascending) \
                    .index

    @property
    def overall_pct(self) -> pd.DataFrame:

        if not self.overall:
            return

        result = pd.DataFrame(
            self.df[self.count].value_counts(normalize=True)
        ).transpose()

        result = result[self.ordered_columns]

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

        result = result[self.ordered_columns]

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
