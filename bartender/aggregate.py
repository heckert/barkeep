import pandas as pd


class Aggregator:
    def __init__(self,
                 df: pd.DataFrame, *,
                 groupby: str,
                 count: str,
                 average: str = None,
                 overall: bool = True,
                 index_ascending: bool = False):

        self.df = df
        self.grouper = df.groupby(groupby)
        self.count = count
        self.average = average
        self.overall = overall
        self.index_ascending = index_ascending

    @property
    def overall_percent(self) -> pd.DataFrame:
        if not self.overall:
            return

        result = pd.DataFrame(
            self.df[self.count].value_counts(normalize=True)
        ).transpose()

        result.index = ['Overall']

        return result

    @property
    def overall_mean(self) -> pd.DataFrame:
        if not self.overall:
            return

        if self.average is None:
            return

        return pd.DataFrame({
            'Mean': [self.df[self.average].mean()]
        }, index=['Overall'])

    @property
    def group_percents(self) -> pd.DataFrame:
        return self.grouper[self.count] \
            .value_counts(normalize=True) \
            .unstack() \
            .fillna(0) \
            .sort_index(ascending=self.index_ascending)

    @property
    def group_means(self) -> pd.DataFrame:
        if self.average is None:
            return

        return self.grouper[self.average] \
            .mean() \
            .sort_index(ascending=self.index_ascending)

    @property
    def n_groups(self) -> int:
        return len(self.group_percents)
