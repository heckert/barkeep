import numpy as np
import pandas as pd


test_df = pd.DataFrame({
    'group': [
        'mighty ducks', 'mighty ducks', 'ordinary dinosaurs',
        'ordinary dinosaurs', 'hot dogs', 'hot dogs',
        'mighty ducks', 'ordinary dinosaurs', 'mighty ducks',
        'mighty ducks', 'ordinary dinosaurs', 'mighty ducks'
    ],
    'metric': list(range(12))
})

test_df['bins'] = pd.cut(test_df['metric'],
                         np.arange(0, 13, 3),
                         right=False,
                         labels=[
                            'small',
                            'medium',
                            'large',
                            'xlarge'])

