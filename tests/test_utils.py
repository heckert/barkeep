from barkeep.utils import get_longest_item


def test_get_longest_item():
    inp = ['foo', 'baar', 'baaaz']
    exp = 'baaaz'

    assert get_longest_item(inp) == exp
