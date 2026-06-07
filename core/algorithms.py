# core/algorithms.py
from typing import List, Callable, TypeVar, Optional

T = TypeVar("T")

def quick_sort(arr: List[T], key: Callable[[T], any] = lambda x: x, depth: int = 0) -> List[T]:
    """Return a new list sorted using the quick‑sort algorithm with detailed step-by-step trace logging of all recursion levels."""
    if len(arr) <= 1:
        return arr[:]
    
    pivot = arr[len(arr) // 2]
    pivot_key = key(pivot)
    
    left = [x for x in arr if key(x) < pivot_key]
    middle = [x for x in arr if key(x) == pivot_key]
    right = [x for x in arr if key(x) > pivot_key]
    
    # Helper to format food items nicely with name and price
    def format_food(item) -> str:
        if hasattr(item, 'name') and hasattr(item, 'price'):
            return f"{item.name} (Rs. {item.price})"
        return str(item)
        
    # Print the detailed intermediate state at this recursion level
    indent = "  " * depth
    print(f"\n[QuickSort Depth {depth}] (Pivot Selected: {format_food(pivot)})")
    print(f"{indent}├── Unsorted list: {[format_food(x) for x in arr]}")
    print(f"{indent}├── Left partition (< pivot): {[format_food(x) for x in left]}")
    print(f"{indent}├── Middle partition (= pivot): {[format_food(x) for x in middle]}")
    print(f"{indent}└── Right partition (> pivot): {[format_food(x) for x in right]}")
    
    return quick_sort(left, key, depth + 1) + middle + quick_sort(right, key, depth + 1)


def binary_search(sorted_list: List[T], target: T, key: Callable[[T], any] = lambda x: x) -> Optional[int]:
    """Perform binary search on *sorted_list* and return the index of *target* with detailed step-by-step trace logging of all steps."""
    low, high = 0, len(sorted_list) - 1
    step = 1
    
    print(f"\n--- BINARY SEARCH TRACE ---")
    print(f"Searching For: '{target}'")
    print(f"Sorted Space : {[key(x) for x in sorted_list]}")
    
    while low <= high:
        mid = (low + high) // 2
        mid_val = key(sorted_list[mid])
        
        # Print the detailed intermediate state for this search step
        print(f"  Step {step}: low={low}, high={high}, mid={mid} | Mid Value = '{mid_val}'")
        step += 1
        
        if mid_val == target:
            print(f"  └── Success: Target matched '{mid_val}' at index {mid}!")
            return mid
        elif mid_val < target:
            print(f"  └── Info: Target > '{mid_val}', searching RIGHT half.")
            low = mid + 1
        else:
            print(f"  └── Info: Target < '{mid_val}', searching LEFT half.")
            high = mid - 1
            
    print("  └── Result: Target not found in the list.")
    return None
