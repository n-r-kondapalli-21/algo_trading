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

previous_buy_price = None
previous_sell_price = None
last_action = None  

def buy_sell_prices(action, ltp, default_buy_price=480):  # <- you can pass test value
    global previous_buy_price, previous_sell_price, last_action

    if action == "BUY":
        buy_price = ltp
        sell_price = None
        previous_buy_price = buy_price
        last_action = "BUY"

    elif action == "SELL":
        if previous_buy_price is None:  # First SELL case
            previous_buy_price = default_buy_price  # use test value
        buy_price = previous_buy_price
        sell_price = ltp
        previous_sell_price = sell_price
        last_action = "SELL"

    elif action == "HOLD":
        if last_action == "BUY":
            buy_price = previous_buy_price
            sell_price = None
        elif last_action == "SELL":
            buy_price = previous_buy_price
            sell_price = previous_sell_price
        else:
            raise ValueError("HOLD not valid without a previous BUY/SELL")
    else:
        raise ValueError("Invalid action")

    return buy_price, sell_price
