import pandas as pd


class Aggregator:
    def __init__(self,
                 df: pd.DataFrame, *,
                 groupby: str,
                 count: str,
                 average: str = None,
                 index_ascending: bool = True):

        self.df = df
        self.grouper = df.groupby(groupby)
        self.count = count
        self.average = average
        self.index_ascending = index_ascending

    @property
    def value_counts(self) -> pd.DataFrame:

        return self.grouper[self.count] \
            .value_counts(normalize=True) \
            .unstack() \
            .fillna(0) \
            .sort_index(ascending=self.index_ascending)

    @property
    def means(self) -> pd.DataFrame:

        if self.average is None:
            return

        return self.grouper[self.average] \
            .mean() \
            .sort_index(ascending=self.index_ascending)
