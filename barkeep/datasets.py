import numpy as np
import pandas as pd


test_df = pd.DataFrame({
    'group': [
        'mighty ducks', 'mighty ducks', 'ordinary dinosaurs',
        'ordinary dinosaurs', 'hot dogs', 'hot dogs',
        'mighty ducks', 'ordinary dinosaurs', 'mighty ducks'
    ],
    'metric': range(9)
})

test_df['bins'] = pd.cut(test_df['metric'],
                         np.arange(0, 10, 3),
                         right=False,
                         labels=[
                            'small\n[0,3)',
                            'medium\n[3,6)',
                            'large\n[6,9)'])


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
