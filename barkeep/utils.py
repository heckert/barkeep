import math
import matplotlib
import matplotlib.pyplot as plt

from collections.abc import Mapping
from typing import Optional, Tuple


def get_longest_item(array: list) -> str:
    candidate = str(array[0])

    for i in array:
        if len(str(i)) > len(candidate):
            candidate = str(i)

    return candidate


class MappableDataClass(Mapping):
    """Base class for allowing to unpack dataclasses via ** like dicts."""

    # https://stackoverflow.com/questions/8601268/class-that-acts-as-mapping-for-unpacking
    def __iter__(self):
        return iter(self.__dict__)

    def __getitem__(self, x):
        return self.__dict__[x]

    def __len__(self):
        return len(self.__dict__)


def get_cmap_colors(length: Optional[int] = None,
                    n_colors_in_cmap: Optional[int] = None,
                    indices_to_select: Optional[list] = None,
                    name='tab10') -> list:
    """Get an array of colors for coloring bar segments.

    See https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html
    for available colormaps.

    Pass only length parameter to utilize the full cmap.
    When choosing a discrete (i.e. not continuous) map and you want to select
    colors instead of using of the whole range, pass the total number of colors
    in the cmap as ``n_colors_in_cmap``, and pass a list of which indices to
    select via ``select_cats``.

    Args:
        length (int): Number of colors to return.
        n_colors_in_cmap (int, optional): Number of colors in the map.
        indices_to_select (list, optional): Indices of colors to select.
        name (str, optional): Name of matplotlib colormap. Defaults to 'tab10'.

    Returns:
        list: An array of length `length`
    """

    if indices_to_select is None:
        indices_to_select = range(length)
    else:
        length = max(indices_to_select) + 1

    if n_colors_in_cmap is None:
        norm = plt.Normalize(vmin=0, vmax=length - 1)
    else:
        norm = plt.Normalize(vmin=0, vmax=n_colors_in_cmap - 1)

    cmap = matplotlib.colormaps[name]

    result = list(
        map(lambda x: cmap(norm(x)), indices_to_select)
    )

    # Round each tuple item in result list to 4 decimal places.
    result = [tuple(map(lambda x: round(x, 4), tup)) for tup in result]

    return result


def normalize_rgb(rgb: Tuple[int, int, int],
                  alpha: Optional[float] = None) -> Tuple[float]:
    """Normalize 255-based RGB scores to values between 0 and 1.

    Matplotlib expects colors in this format.
    Optional fourth element in the tuple indicates opacity.

    Args:
        rgb (tuple): Tuple indicating rgb scores between 0 and 255.
        alpha (float, optional): Reduces opacity. Defaults to None.

    Returns:
        tuple: Normalized RGB scores with optional opacity.
    """

    color = tuple(
        map(lambda x: round(x/255, 4), rgb)
    )

    if alpha:
        color = (*color, alpha)

    return color


def select_from_center(n: int, length: int) -> list:
    """Given an array of ``length``, pick `n` elements from its center.

    Args:
        n (int): Number of items to select.
        length (int): Length of the array to select from

    Returns:
        list: Indices of items to select
    """

    array = list(range(length))
    dif = length - n

    if dif < 0:
        raise ValueError('`n` must be <= `length`')

    return array[math.floor(dif/2):]