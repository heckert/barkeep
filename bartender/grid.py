import hydra

from collections.abc import Mapping
from dataclasses import dataclass, field
from omegaconf import DictConfig
from typing import List, Tuple, Dict

from bartender.aggregate import Aggregator


hydra.initialize(config_path="conf", version_base=None)
cfg = hydra.compose(config_name="config")


@dataclass
class GridConfig(Mapping):
    figsize: Tuple[int, int]
    nrows: int
    ncols: int
    gridspec_kw: Dict[str, List[int]]

    # These dunder methods allow to
    # unpack the dataclass like a dict
    # https://stackoverflow.com/questions/8601268/class-that-acts-as-mapping-for-unpacking
    def __iter__(self):
        return iter(self.__dict__)

    def __getitem__(self, x):
        return self.__dict__[x]

    def __len__(self):
        return len(self.__dict__)


@dataclass
class GridConfigFactory:
    figconfig: DictConfig = cfg.figsize
    nrows: int = 1
    ncols: int = 1
    height_ratios: List[int] = field(default_factory=lambda: [1])
    width_ratios: List[int] = field(default_factory=lambda: [5])

    def fit_aggregator(self, aggregator: Aggregator) -> None:
        """Depending on the aggregator's attributes, the grid is adjusted."""
        # TODO
        pass

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
