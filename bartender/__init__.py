import pandas as pd

__version__ = '0.1.0'

test_df = pd.DataFrame({
    'group': [
        'mighty ducks', 'mighty ducks', 'ordinary dinosaurs',
        'ordinary dinosaurs', 'hot dogs', 'hot dogs',
        'mighty ducks', 'ordinary dinosaurs', 'mighty ducks'
    ],
    'metric': range(9),
    'bins': pd.Categorical(['small', 'small', 'small',
                            'medium', 'medium', 'medium',
                            'large', 'large', 'large'],
                           ordered=True,
                           categories=['small', 'medium', 'large'])
})


columns = pd.CategoricalIndex(['small', 'medium', 'large'],
                              ordered=True,
                              categories=['small', 'medium', 'large'])

test_agg = pd.DataFrame([
    (0.0, 2 / 3, 1 / 3),
    (1 / 3, 1 / 3, 1 / 3),
    (2 / 3, 0.0, 1 / 3),
], index=list('cba'), columns=columns)

test_agg.index.name = 'group'
test_agg.columns.name = 'bins'
