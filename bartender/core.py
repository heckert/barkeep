import hydra

from dataclasses import dataclass
from typing import List


hydra.initialize(config_path="conf", version_base=None)
cfg = hydra.compose(config_name="config")

print(cfg)


@dataclass
class GridConfig:
    nrows: int = 1
    ncols: int = 1
    height_ratios: List[int] = [1]
    width_rations: List[int] = [5]


class GridPlot:
    def __init__(
        self, *,
        groupby: str,
        count: str,
        mean: str
    ):
        pass
