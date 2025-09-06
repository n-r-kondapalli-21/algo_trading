# -*- coding: utf-8 -*-
"""
Created on Thu Aug 28 16:12:58 2025

@author: NARAYANA
"""
"""
function name: update_MML_MMP
this function tracks and updates the Maximum Market Loss (MML) 
and Maximum Market Profit (MMP) over multiple calls by storing values internally.

Parameters:
unreal_pl_value : float or int
    The unrealized profit/loss value from the current trade or position.

Returns:
tuple
    A tuple (mml, mmp) where:
        - mml is the lowest unrealized P/L observed so far (Maximum Market Loss).
        - mmp is the highest unrealized P/L observed so far (Maximum Market Profit).
"""

def update_MML_MMP(unreal_pl_value):
    """
    Update Maximum Market Loss (MML) and Maximum Market Profit (MMP)
    and store them across multiple calls automatically.
    """
    if not hasattr(update_MML_MMP, "mml"):
        update_MML_MMP.mml = None
        update_MML_MMP.mmp = None

    # Update MML
    if update_MML_MMP.mml is None:
        update_MML_MMP.mml = unreal_pl_value
    else:
        update_MML_MMP.mml = min(update_MML_MMP.mml, unreal_pl_value)

    # Update MMP
    if update_MML_MMP.mmp is None:
        update_MML_MMP.mmp = unreal_pl_value
    else:
        update_MML_MMP.mmp = max(update_MML_MMP.mmp, unreal_pl_value)

    return update_MML_MMP.mml, update_MML_MMP.mmp



# # pl_values = [25.0, 50.0, -50.0, -100.0, 150.0, 110.0]

# mml, mmp = update_MML_MMP(pl_values)
# print(mml, mmp)
