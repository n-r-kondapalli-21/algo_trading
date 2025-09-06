# -*- coding: utf-8 -*-
"""
Created on Mon Sep  1 14:27:48 2025

@author: NARAYANA
"""
"""
function name: buy_sell_prices
this function manages buy, sell, and hold actions by recording the latest buy price 
and tracking corresponding sell prices for trades.

Parameters:
action : str
    The trade action to perform. It must be one of "BUY", "SELL", or "HOLD".
ltp : float
    The latest traded price of the stock or instrument.

Returns:
tuple
    A tuple (buy_price, sell_price) where:
        - buy_price is the price at which the stock was bought or carried forward.
        - sell_price is the price at which the stock was sold, or None if not applicable.
"""

# Global variable to store the last buy price
previous_buy_price = None  

def buy_sell_prices(action, ltp):
    global previous_buy_price  # so it survives across calls

    if action == "BUY":
        buy_price = ltp
        sell_price = None
        previous_buy_price = buy_price  # update stored buy price

    elif action == "HOLD":
        buy_price = previous_buy_price
        sell_price = None

    elif action == "SELL":
        buy_price = previous_buy_price
        sell_price = ltp

    else:
        raise ValueError("Invalid action")

    return buy_price, sell_price



# print(buy_sell_prices("BUY", 350))   # (350, None)
# print(buy_sell_prices("HOLD", 360))  # (350, None)
# print(buy_sell_prices("SELL", 370))  # (350, 370)
# print(buy_sell_prices("HOLD", 380))  # (350, None) 
