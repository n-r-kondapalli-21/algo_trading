# -*- coding: utf-8 -*-
"""
Created on Sat Aug 30 16:20:59 2025

@author: NARAYANA
"""
"""
function name: delta_diff
this function calculates the difference between the current delta value 
and the previously stored delta value across function calls.

Parameters:
new_delta : float or str
    The latest delta value (can be a number or string that can be converted to float).

Returns:
float or None or dict
    - Returns the delta difference (rounded to 6 decimals) if a previous delta exists.
    - Returns None if it is the first call (no previous delta stored).
    - Returns a dictionary with an error message if the input cannot be converted to float.
"""

def delta_diff(new_delta):
    """
    Stores the previous delta internally.
    Returns the difference between current and previous delta.
    Converts inputs to float if they are strings.
    """
    # Convert to float if needed
    try:
        new_delta = float(new_delta)
    except (TypeError, ValueError):
        return {"error": f"Invalid delta value: {new_delta}"}

    if not hasattr(delta_diff, "prev_delta"):
        delta_diff.prev_delta = None

    if delta_diff.prev_delta is None:
        delta_diff.prev_delta = new_delta
        return None  # No difference for the first call

    diff = new_delta - delta_diff.prev_delta
    delta_diff.prev_delta = new_delta  # Update stored value
    return round(diff,6)



