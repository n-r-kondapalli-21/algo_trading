# -*- coding: utf-8 -*-
"""
Created on Sat Aug 23 16:53:13 2025

@author: NARAYANA
"""
"""
function name: calculate_PL
this function calculates the profit or loss (P&L) for a completed trade 
based on entry price, exit price, trade quantity, transaction costs, 
and trade type (BUY or SELL).

Parameters:
entry_price : float
    The price at which the trade was entered.
exit_price : float, optional (default = None)
    The price at which the trade was closed. If None, the trade is considered still open.
quantity : int, optional (default = 1)
    The number of units traded.
transaction_cost : float, optional (default = 0)
    The total transaction cost (brokerage, taxes, charges) for the trade.
trade_type : str, optional (default = "BUY")
    The type of trade: "BUY" for long positions, "SELL" for short positions.

Returns:
float or None or dict
    - Returns the profit/loss value when the trade is closed.
    - Returns None if the trade is still open.
    - Returns a dictionary with an error message if an invalid trade_type is passed.
"""

def calculate_PL(entry_price, exit_price=None, quantity=1, transaction_cost=0, trade_type="BUY"):   
    """
    Calculates Profit or Loss only when trade is closed.
    - For a BUY trade, profit = (Sell - Buy) * qty - costs
    - For a SELL trade, profit = (Sell - Buy) * qty - costs
    """
    if trade_type=="BUY" or trade_type=="SELL":
        if exit_price is None:
            # Trade is still open, no P&L yet
            return None
    
        # Trade closed → calculate P&L
        if trade_type == "BUY":   # Long
            PL = (exit_price - entry_price) * quantity - transaction_cost
        elif trade_type == "SELL":  # Short
            PL = (entry_price - exit_price) * quantity - transaction_cost
        else:
            return {"error": "Invalid trade_type. Use BUY or SELL."}
        
        # return {"status": "CLOSED", "Profit/loss": PL}
        return PL
    
    else:
        return None
        
    



# # Closed Long trade (Buy at 100, Sell at 110)
# print(calculate_PL(entry_price=397.9, exit_price=398.6, quantity=75, transaction_cost=66.0639, trade_type="SELL"))


# # Closed Short trade (Sell at 110, Buy at 100)
# print(calculate_PL(entry_price=110, exit_price=100, quantity=50, transaction_cost=20, trade_type="SELL"))


# # Open Long trade (No exit yet)
# print(calculate_PL(entry_price=100, quantity=50, transaction_cost=20, trade_type="BUY"))

