# -*- coding: utf-8 -*-
"""
Created on Sat Aug 23 16:09:26 2025

@author: NARAYANA
"""

from login import initialize_session

"""
function name: transaction_cost_of_ticker
this function calculates the transaction charges (brokerage, taxes, etc.) 
for BUY, SELL, and HOLD actions of a given ticker using the broker API.

Parameters:
session : object
    An authenticated trading session object (e.g., SmartAPI session).
buy_sell : str
    The trade action: "BUY", "SELL", or "HOLD".
quantity : int
    The number of units in the trade.
buy_price : float
    The entry price of the trade.
sell_price : float
    The exit price of the trade.
ticker_name : str
    The name of the instrument/ticker.
token_num : str or int
    The token number of the instrument (as required by the broker API).
exchange : str, optional (default = "NFO")
    The exchange where the trade is executed.
ltp : float, optional (default = None)
    The latest traded price (used only if action is HOLD).

Returns:
float
    The estimated total transaction charges for the given trade.
"""
def transaction_cost_of_ticker(session, buy_sell, quantity, buy_price, sell_price, ticker_name, token_num, exchange="NFO", ltp=None):
    """
    Calculate transaction costs (brokerage, taxes, etc.) for BUY, SELL, and HOLD.
    
    - BUY/SELL → returns actual transaction charges
    - HOLD     → estimates unrealized charges using LTP
    """
    
    if buy_sell in ["BUY", "SELL"]:
        price = buy_price if buy_sell == "BUY" else sell_price

    elif buy_sell == "HOLD":
        # For unrealized P&L, we need LTP to estimate charges
        if ltp is None:
            return 0   # No LTP provided, can't estimate
        price = ltp
        # Assume SELL for estimating charges (exit position)
        buy_sell = "SELL"

    else:
        return 0

    params = {
        "orders": [{
            "product_type": "INTRADAY",
            "transaction_type": buy_sell,
            "quantity": quantity,
            "price": price,
            "exchange": exchange,
            "symbol_name": ticker_name,
            "token": token_num
        }]
    }

    response = session.estimateCharges(params)
    summary_total = response["data"]["summary"]["total_charges"]
    return summary_total

"""
function name: transaction_cost_on_HOLD
this function calculates the transaction charges (brokerage, taxes, etc.) 
only for BUY and SELL actions of a given ticker. 
It does not handle HOLD scenarios.

Parameters:
session : object
    An authenticated trading session object (e.g., SmartAPI session).
buy_sell : str
    The trade action: must be either "BUY" or "SELL".
quantity : int
    The number of units in the trade.
buy_price : float
    The entry price of the trade.
sell_price : float
    The exit price of the trade.
ticker_name : str
    The name of the instrument/ticker.
token_num : str or int
    The token number of the instrument (as required by the broker API).
exchange : str, optional (default = "NFO")
    The exchange where the trade is executed.

Returns:
float
    The estimated total transaction charges for the trade.
    Returns 0 if the action is not "BUY" or "SELL".
"""

def transaction_cost_on_HOLD(session,buy_sell,quantity,buy_price,sell_price,ticker_name,token_num,exchange="NFO"):
    
    if buy_sell=="BUY" or buy_sell=="SELL":
        
        if buy_sell=="BUY":
           price=buy_price
        elif buy_sell=="SELL":
           price=sell_price
            
            
        params={"orders": [{"product_type": "INTRADAY",
                            "transaction_type": buy_sell,
                            "quantity": quantity,
                            "price":price ,
                            "exchange": exchange,
                            "symbol_name": ticker_name,
                            "token": token_num}]} 
        response=session.estimateCharges(params)
        summary_total = response["data"]["summary"]["total_charges"]
        return summary_total
    
    else:
        return 0
    
    

    
    

    
# session,_ = initialize_session()
# print(transaction_cost_of_ticker(session,"BUY",75,397.9,398.6,"NIFTY",60465,"NFO"))

    