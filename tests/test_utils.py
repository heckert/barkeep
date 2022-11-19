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
    inp = dict(length=5, name='tab10')
    exp = [
        (0.1216, 0.4667, 0.7059, 1.0),
        (0.1725, 0.6275, 0.1725, 1.0),
        (0.549, 0.3373, 0.2941, 1.0),
        (0.498, 0.498, 0.498, 1.0),
        (0.0902, 0.7451, 0.8118, 1.0)
    ]

    assert get_cmap_colors(**inp) == exp
