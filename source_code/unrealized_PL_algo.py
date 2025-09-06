# -*- coding: utf-8 -*-
"""
Created on Thu Aug 28 14:59:12 2025

@author: NARAYANA
"""
from pull_livedata import getLtp
from login import initialize_session, get_ticker_data


"""function_name:calculate_unreal_PL
    Calculate Mark-to-Market (unrealized) Profit or Loss using current LTP.

Parameters:
    entry_price (float): Price at which trade was entered.
    current_ltp (float): Current market price (LTP).
    quantity (int): Number of units (must be positive).
    transaction_cost (float): Brokerage, taxes, etc.
    trade_type (str): "BUY" for long trades, "SELL" for short trades.

Returns:
    dict: {
        "status": "OPEN",
        "unrealized_PL": float
    }

Formula:
    - BUY (long):  (LTP - entry) * qty - costs
    - SELL (short): (entry - LTP) * qty - costs
"""   
def calculate_unreal_PL(entry_price, current_ltp, quantity=1, transaction_cost=0, trade_type="BUY"):   
    
    if quantity <= 0:
        return {"error": "Quantity must be positive."}
    
    trade_type = trade_type.upper()
    
    if trade_type == "BUY" or trade_type == "HOLD":   # Long
        pnl = (current_ltp - entry_price) * quantity - transaction_cost
    elif trade_type == "SELL":  # Short
        pnl = (entry_price - current_ltp) * quantity - transaction_cost
    else:
        return {"error": "Invalid trade_type. Use BUY or SELL."}
    
    # return {"status": "OPEN", "unrealized_PL": pnl}
    return round(pnl,6)    



# session,_= initialize_session()       #Initialize session and get login data   
# ltp=getLtp(session,'NIFTY30SEP2524550CE',60451,'NFO')
# # Long trade, still open
# print(calculate_unreal_PL(37, ltp, 50,26.566, trade_type="HOLD"))
# # {'status': 'OPEN', 'realized_PL': None, 'unrealized_PL': 6000.0}



