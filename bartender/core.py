import hydra

from dataclasses import dataclass, field
from omegaconf import OmegaConf
from typing import List

from bartender.aggregate import Aggregator


hydra.initialize(config_path="conf", version_base=None)
cfg = hydra.compose(config_name="config")


@dataclass
class GridConfig:
    nrows: int = 1
    ncols: int = 1
    height_ratios: List[int] = field(default_factory=lambda: [1])
    width_rations: List[int] = field(default_factory=lambda: [5])


class GridPlot:
    def __init__(self, *,
                 aggregator: Aggregator,
                 include_overall=True):

        self.aggregator = aggregator


if __name__ == '__main__':
    print(OmegaConf.to_yaml(cfg))
