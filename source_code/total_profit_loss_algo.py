# -*- coding: utf-8 -*-
"""
Created on Sat Aug 23 17:30:00 2025

@author: NARAYANA
"""
"""
function name: calculate_tpl
this function maintains and updates the cumulative total profit/loss (PL) 
across multiple calls by storing values internally.

Parameters:
pl_value : float or int or None
    The profit/loss value to be added to the cumulative total.
    - If None, no update is made and the last cumulative value is returned.

Returns:
float
    The cumulative total profit/loss including all values passed so far.
"""

def calculate_tpl(pl_value):
    """
    Stores all PL values across multiple calls and returns the cumulative total.
    """
    if not hasattr(calculate_tpl, "cumulative"):
        calculate_tpl.cumulative = 0   # first time setup

    if pl_value is None:
        return calculate_tpl.cumulative  # no update, just return last value

    # Add the new PL value to stored total
    calculate_tpl.cumulative += pl_value
    return calculate_tpl.cumulative


# pl = -249.1113,-245.678,857.4774
# pl_values = [pl]   # ✅ put float into a list
# print(calculate_tpl(pl_values))



