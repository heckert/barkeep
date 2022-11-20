import hydra

from dataclasses import dataclass, field, asdict
from omegaconf import DictConfig
from typing import List, Tuple, Dict


hydra.initialize(config_path="conf", version_base=None)
cfg = hydra.compose(config_name="config")


@dataclass
class GridConfig:
    figsize: Tuple[int, int]
    nrows: int
    ncols: int
    gridspec_kw: Dict[str, int]

    def asdict(self) -> dict:
        return asdict(self)


@dataclass
class GridConfigFactory:
    figconfig: DictConfig = cfg.figsize
    nrows: int = 1
    ncols: int = 1
    height_ratios: List[int] = field(default_factory=lambda: [1])
    width_ratios: List[int] = field(default_factory=lambda: [5])

    @property
    def gridspec_kw(self) -> dict:
        return dict(
            height_ratios=self.height_ratios,
            width_ratios=self.width_ratios
        )

    @property
    def figsize(self) -> tuple:
        return tuple(self.figconfig.regular.values())

    def get_grid_config(self) -> GridConfig:
        return GridConfig(
            figsize=self.figsize,
            nrows=self.nrows,
            ncols=self.ncols,
            gridspec_kw=self.gridspec_kw
        )
