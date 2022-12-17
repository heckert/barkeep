import pandas as pd
import pytest
from barkeep.aggregate import Aggregator


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


def test_group_pct(agg):

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

    assert agg.group_pct.equals(expected)


def test_group_mean(agg):

    expected = pd.DataFrame({
        'mean': [6 + 2/3, 5, 3 + 1/3]
    })

    expected.index = list('cba')
    expected.index.name = 'group'

    assert agg.group_avg.equals(expected)


def test_group_median(agg):

    expected = pd.DataFrame({
        'median': [6., 4., 2.]
    })

    expected.index = list('cba')
    expected.index.name = 'group'

    agg.average_type = 'median'

    assert agg.group_avg.equals(expected)


def test_overall_pct(agg):

    expected = pd.DataFrame([
        [1 / 3, 1 / 3, 1 / 3]
    ], columns=['small', 'medium', 'large'], index=['Overall'])

    assert agg.overall_pct.equals(expected)


def test_n_groups(agg):

    assert agg.n_groups == 3


def test_n_count_categories(agg):

    assert agg.n_count_categories == 3


def test_wrong_avg(df):

    with pytest.raises(ValueError):
        Aggregator(
            df,
            groupby='group',
            count='bins',
            average='metric',
            average_type='foo'
        )
