# -*- coding: utf-8 -*-
"""
Created on Sat Aug 30 16:44:02 2025

@author: NARAYANA
"""
from datetime import datetime


"""
function name: buy_sell_action
this function decides whether to take a BUY, SELL, or HOLD action 
based on the last action taken and the condition (quantity * delta).

Parameters:
buy_sell_quantity : int or float
    The trade quantity used in the condition check.
delta : float
    The delta value (sensitivity of option price to underlying asset changes).

Returns:
tuple
    A tuple (sno, timestamp, action) where:
        - sno is a sequential number for each decision step.
        - timestamp is the date and time when the action was decided.
        - action is one of "BUY", "SELL", or "HOLD" based on the trading logic.
"""

# Initialize
last_action = None
sno = 0 

def buy_sell_action(buy_sell_quantity, delta):
    """
    1. First action = BUY
    2. After BUY, wait until (quantity * delta > 20) → SELL
    3. After SELL, next action = BUY again (no condition)
    """
    global last_action, sno

    sno += 1
    condition = buy_sell_quantity * delta

    if last_action is None:
        # First action
        action = "BUY"

    elif last_action == "BUY":
        # After BUY → SELL only when condition is met
        if condition > 41.9:
            action = "SELL"
        else:
            action = "HOLD"

    elif last_action == "SELL":
        # After SELL → always BUY again
        action = "BUY"

    # Timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Update last_action only when action is BUY or SELL
    if action in ["BUY", "SELL"]:
        last_action = action

    return sno, timestamp, action
