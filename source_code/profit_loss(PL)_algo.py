# -*- coding: utf-8 -*-
"""
Created on Sat Aug 23 16:53:13 2025

@author: NARAYANA
"""
from pull_livedata import getLtp
from login import initialize_session, get_ticker_data
session, logindata = initialize_session()        #Initialize session and get login data
ticker_data = get_ticker_data()                  #Get instrument list and create dataframe
 
def calculate_PL(entry_price, exit_price=None, quantity=1, transaction_cost=0, trade_type="BUY"):   
    """
    Calculates Profit or Loss only when trade is closed.
    - For a BUY trade, profit = (Sell - Buy) * qty - costs
    - For a SELL trade, profit = (Sell - Buy) * qty - costs
    """
    
    if exit_price is None:
        # Trade is still open, no P&L yet
        return {"status": "OPEN", "Profit/loss": None}

    # Trade closed → calculate P&L
    if trade_type == "BUY":   # Long
        PL = (exit_price - entry_price) * quantity - transaction_cost
    elif trade_type == "SELL":  # Short
        PL = (entry_price - exit_price) * quantity - transaction_cost
    else:
        return {"error": "Invalid trade_type. Use BUY or SELL."}
    
    return {"status": "CLOSED", "Profit/loss": PL}


# Closed Long trade (Buy at 100, Sell at 110)
# print(calculate_PL(entry_price=37.05, exit_price=40, quantity=75, transaction_cost=27.8613, trade_type="SELL"))


# # Closed Short trade (Sell at 110, Buy at 100)
# print(calculate_PL(entry_price=110, exit_price=100, quantity=50, transaction_cost=20, trade_type="SELL"))


# # Open Long trade (No exit yet)
# print(calculate_PL(entry_price=100, quantity=50, transaction_cost=20, trade_type="BUY"))


def calculate_MML(entry_price, ltp_list, quantity=1, trade_type="BUY"):
    """
    Calculates Maximum Market Loss (worst loss during trade).
    ltp_list: list of observed market prices until now
    """
    trade_type = trade_type.upper()
    mtm_values = []
    
    for ltp in ltp_list:
        if trade_type == "BUY":
            mtm = (ltp - entry_price) * quantity
        elif trade_type == "SELL":
            mtm = (entry_price - ltp) * quantity
        mtm_values.append(mtm)
    
    return min(mtm_values) if mtm_values else 0
ltp_history = [] 
ltp=getLtp(session,'NIFTY28AUG2524800CE',71966,'NFO')
ltp_history.append(ltp)

mml = calculate_MML(37.05, ltp_history, 75, "BUY")
print(mml)
print(ltp_history)


def calculate_MMP(entry_price, ltp_list, quantity=1, trade_type="BUY"):
    """
    Calculates Maximum Market Profit (best profit during trade).
    ltp_list: list of observed market prices until now
    """
    trade_type = trade_type.upper()
    mtm_values = []
    
    for ltp in ltp_list:
        if trade_type == "BUY":
            mtm = (ltp - entry_price) * quantity
        elif trade_type == "SELL":
            mtm = (entry_price - ltp) * quantity
        mtm_values.append(mtm)
    
    return max(mtm_values) if mtm_values else 0

























