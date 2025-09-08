# -*- coding: utf-8 -*-
"""
Created on Sat Aug 30 16:44:02 2025

@author: NARAYANA
"""
from datetime import datetime


last_action = None
sno = 0 

def buy_sell_action(buy_sell_quantity, delta, initial_action="BUY", threshold_buy=41.9, threshold_sell=41.8):
    """
    Flexible BUY/SELL logic:
    
    Parameters
    ----------
    buy_sell_quantity : int or float
        The trade quantity used in the condition check.
    delta : float
        The delta value (sensitivity factor).
    initial_action : str ("BUY" or "SELL")
        The very first action (set manually).
    threshold_buy : float
        Threshold for moving from BUY → SELL.
    threshold_sell : float
        Threshold for moving from SELL → BUY.

    Rules
    -----
    1. First action = given by initial_action
    2. After BUY → SELL only when (quantity * delta > threshold_buy)
    3. After SELL → BUY only when (quantity * delta > threshold_sell)
    4. If condition not met → HOLD
    """
    global last_action, sno

    sno += 1
    condition = buy_sell_quantity * delta

    if last_action is None:
        # Manual first action
        action = initial_action

    elif last_action == "BUY":
        if condition > threshold_buy:
            action = "SELL"
        else:
            action = "HOLD"

    elif last_action == "SELL":
        if condition > threshold_sell:
            action = "BUY"
        else:
            action = "HOLD"

    # Timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Update last_action only when action is BUY or SELL
    if action in ["BUY", "SELL"]:
        last_action = action

    return sno, timestamp, action











