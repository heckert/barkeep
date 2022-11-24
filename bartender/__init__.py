import pandas as pd

__version__ = '0.1.0'

test_df = pd.DataFrame({
    'group': list('aabbccabc'),
    'metric': range(1, 10),
    'bins': pd.Categorical(['small', 'small', 'small',
                            'medium', 'medium', 'medium',
                            'large', 'large', 'large'],
                           ordered=True,
                           categories=['small', 'medium', 'large'])
})
