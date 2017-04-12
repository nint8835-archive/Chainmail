from typing import List, TypeVar

t = TypeVar("t")


def get_item_from_list(parent_list: List[t], item_index: int, default: t) -> t:
    """
    Returns an item for the list, or the default if the item does not exist.
    :param parent_list: The list to get the item from
    :param item_index: The index of the item to get
    :param default: The default item to return if the specified item could not be found
    :return: The item
    """
    try:
        return parent_list[item_index]
    except KeyError:
        return default
