from bartender.utils import (normalize_rgb,
                             get_longest_item,
                             get_cmap_colors)


def test_normalize_rgb():
    inp = (255, 0, 255)
    exp = (1., 0., 1.)

    assert normalize_rgb(inp) == exp

    exp = (1., 0., 1., 0.9)

    assert normalize_rgb(inp, alpha=.9) == exp


def test_get_longest_item():
    inp = ['foo', 'baar', 'baaaz']
    exp = 'baaaz'

    assert get_longest_item(inp) == exp


def test_get_cmap_colors():
    pass
