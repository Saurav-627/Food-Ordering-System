# core/algorithms.py
from typing import List, Callable, TypeVar, Optional

T = TypeVar("T")

def quick_sort(arr: List[T], key: Callable[[T], any] = lambda x: x) -> List[T]:
    """Return a new list sorted using the quick‑sort algorithm.

    Parameters
    ----------
    arr: List[T]
        The list to sort.
    key: Callable[[T], any]
        Function that extracts a comparable value from each element.

    Returns
    -------
    List[T]
        A new list containing the elements of *arr* in sorted order.
    """
    if len(arr) <= 1:
        return arr[:]
    pivot = arr[len(arr) // 2]
    pivot_key = key(pivot)
    left = [x for x in arr if key(x) < pivot_key]
    middle = [x for x in arr if key(x) == pivot_key]
    right = [x for x in arr if key(x) > pivot_key]
    return quick_sort(left, key) + middle + quick_sort(right, key)


def binary_search(sorted_list: List[T], target: T, key: Callable[[T], any] = lambda x: x) -> Optional[int]:
    """Perform binary search on *sorted_list* and return the index of *target*.

    The list must be sorted according to ``key``.  If the target is not
    found, ``None`` is returned.
    """
    low, high = 0, len(sorted_list) - 1
    while low <= high:
        mid = (low + high) // 2
        mid_val = key(sorted_list[mid])
        if mid_val == target:
            return mid
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1
    return None
