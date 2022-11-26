import hydra

from dataclasses import dataclass
from omegaconf import DictConfig
from typing import List, Tuple, Dict

from bartender.aggregate import Aggregator
from bartender.utils import _MappableDataClass


hydra.initialize(config_path="conf", version_base=None)
cfg = hydra.compose(config_name="config")


@dataclass
class GridRecipe(_MappableDataClass):
    """Semantic description of grid structure"""
    n_groups: int
    has_mean: bool
    has_overall: bool
    legend_out: bool


def get_grid_recipe(aggregator: Aggregator,
                    legend_out: bool = False) -> GridRecipe:
    """Translates shape of Aggregator into a GridRecipe.

    Args:
        aggregator (Aggregator): Aggregator instance.
        legend_out (bool, optional): Put legend outside of plot.
            Defaults to False.

    Returns:
        GridRecipe: A semantic description of the strucure of the plot.
    """

    return GridRecipe(
        n_groups=aggregator.n_groups,
        has_mean=aggregator.group_means is not None,
        has_overall=aggregator.overall,
        legend_out=legend_out
    )


@dataclass
class GridConfig(_MappableDataClass):
    """Contains all numeric specifications for the grid.

    The class attributes serve as kwargs for `plt.subplots`.
    """
    figsize: Tuple[int, int]
    nrows: int
    ncols: int
    gridspec_kw: Dict[str, List[int]]


class GridConfigFactory:
    """Translates the semantic GridRecipe into the numeric GridConfig."""

    def __init__(self, recipe: GridRecipe):

        self.recipe = recipe
        self.figconfig: DictConfig = cfg.figsize
        self.height_ratios = [1]
        self.width_ratios = [5]

        self._parse_recipe()

    def _parse_recipe(self):
        if self.recipe.has_overall:
            self.height_ratios += [self.recipe.n_groups]

        if self.recipe.has_mean:
            self.width_ratios += [1]

        if self.recipe.legend_out:
            self.width_ratios += [1]

        # If both has mean and legend out,
        # shorten the main part of the plot.
        if len(self.width_ratios) == 3:
            self.width_ratios[0] = 4

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
