import pandas as pd
import pytest
from bartender.aggregate import Aggregator


@pytest.fixture
def df():
    df = pd.DataFrame({
        'group': list('aabbccabc'),
        'metric': range(1, 10),
        'bins': pd.Categorical(['small', 'small', 'small',
                                'medium', 'medium', 'medium',
                                'large', 'large', 'large'],
                               ordered=True,
                               categories=['small', 'medium', 'large'])
    })

    return df


@pytest.fixture
def agg(df):
    return Aggregator(
        df,
        groupby='group',
        count='bins',
        average='metric'
    )


def test_group_percents(agg):

    columns = pd.CategoricalIndex(['small', 'medium', 'large'],
                                  ordered=True,
                                  categories=['small', 'medium', 'large'])

    expected = pd.DataFrame([
        (0.0, 2 / 3, 1 / 3),
        (1 / 3, 1 / 3, 1 / 3),
        (2 / 3, 0.0, 1 / 3),
    ], index=list('cba'), columns=columns)

    expected.index.name = 'group'
    expected.columns.name = 'bins'

    assert agg.group_percents.equals(expected)
