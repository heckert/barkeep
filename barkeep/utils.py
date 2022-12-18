from collections.abc import Mapping


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
