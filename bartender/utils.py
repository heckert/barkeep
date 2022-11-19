import matplotlib.pyplot as plt

from typing import Tuple, Optional


def normalize_rgb(rgb: Tuple[int, int, int],
                  alpha: float = None) -> Tuple[float]:
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


def get_longest_item(array: list) -> str:
    candidate = str(array[0])
    
    for i in array:
        if len(str(i)) > len(candidate):
            candidate = str(i)
        
    return candidate


def _compose(*funcs):
    # TODO: Implement compose function
    # https://youtube.com/shorts/HIdGoFHHKuw?feature=share
    pass

def get_cmap_colors(length: int, 
                    normalize_to: Optional[int] = None,
                    select_cats: Optional[list] = None,
                    name='tab10') -> list:
    """Get an array of colors for coloring bar segments.

    See https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html
    for available colormaps.

    Pass only length parameter to utilize the full cmap.
    When choosing a discrete (i.e. not continuous) map and you want to select 
    colors instead of using of the whole range, pass the total number of colors
    in the cmap as normalize_to, and pass a list of which indices to select via
    select_cats.

    Args:
        length (int): Number of colors to return.
        normalize_to (int, optional): Number of colors in the map. Defaults to None.
        select_cats (list, optional): Indices of colors to select.
        name (str, optional): Name of matplotlib colormap. Defaults to 'tab10'.

    Returns:
        list: An array of length `length`
    """
    
    cmap = plt.cm.get_cmap(name)
    indices = range(length)
    
    if select_cats:
            indices = select_cats
    
    if normalize_to:
        norm = plt.Normalize(vmin=0, vmax=normalize_to - 1)
    else:
        norm = plt.Normalize(vmin=0, vmax=length - 1)
    
    result = [cmap(norm(i)) for i in indices]

    return result
