import hydra

from dataclasses import dataclass, field
from omegaconf import DictConfig
from typing import List, Tuple, Dict

from bartender.aggregate import Aggregator
from bartender.utils import _MappableDataClass


hydra.initialize(config_path="conf", version_base=None)
cfg = hydra.compose(config_name="config")


@dataclass
class GridConfig(_MappableDataClass):
    figsize: Tuple[int, int]
    nrows: int
    ncols: int
    gridspec_kw: Dict[str, List[int]]


@dataclass
class GridConfigFactory:
    figconfig: DictConfig = cfg.figsize
    height_ratios: List[int] = field(default_factory=lambda: [1])
    width_ratios: List[int] = field(default_factory=lambda: [5])

    def fit_aggregator(self, aggregator: Aggregator) -> None:
        """Depending on the aggregator's attributes, the grid is adjusted."""
        # TODO
        pass

    @property
    def figsize(self) -> tuple:
        return tuple(self.figconfig.regular.values())

    @property
    def nrows(self) -> int:
        return len(self.height_ratios)

    @property
    def ncols(self) -> int:
        return len(self.width_ratios)

    @property
    def gridspec_kw(self) -> dict:
        return dict(
            height_ratios=self.height_ratios,
            width_ratios=self.width_ratios
        )

    def build(self) -> GridConfig:
        return GridConfig(
            figsize=self.figsize,
            nrows=self.nrows,
            ncols=self.ncols,
            gridspec_kw=self.gridspec_kw
        )
