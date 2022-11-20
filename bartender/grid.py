import hydra

from dataclasses import dataclass, field
from omegaconf import DictConfig
from typing import List


hydra.initialize(config_path="conf", version_base=None)
cfg = hydra.compose(config_name="config")


@dataclass
class GridConfig:
    figconfig: DictConfig = cfg.figsize
    nrows: int = 1
    ncols: int = 1
    height_ratios: List[int] = field(default_factory=lambda: [1])
    width_ratios: List[int] = field(default_factory=lambda: [5])

    @property
    def gridspec_kw(self):
        return dict(
            height_ratios=self.height_ratios,
            width_ratios=self.width_ratios
        )

    @property
    def figsize(self):
        return tuple(self.figconfig.regular.values())

    def get_dict(self):
        return dict(
            figsize=self.figsize,
            nrows=self.nrows,
            ncols=self.ncols,
            gridspec_kw=self.gridspec_kw
        )
