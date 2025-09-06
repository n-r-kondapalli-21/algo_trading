# -*- coding: utf-8 -*-
"""
Created on Sat Aug 23 16:09:26 2025

@author: NARAYANA
"""

from login import initialize_session



    
"""
function_name: estimate_b_charges
    Calculate brokerage and other applicable charges for the given trades using SmartAPI.

Parameters:
    session : SmartConnect
        An active SmartAPI session object created after logging in.

Returns:
    dict
        A dictionary containing the calculated brokerage, taxes, and other charges.
        If the request fails, returns a dictionary with error information.

Description:
    This function sends a request to Angel Broking's `estimateCharges` API to calculate
    the brokerage, taxes, and other applicable charges for a list of trade orders.
    The orders must include details such as product type, transaction type, quantity,
    price, exchange, symbol name, and token.
"""
def transaction_cost_of_ticker(session,buy_sell,quantity,price,ticker_name,token_num,exchange="NFO"):
    params={"orders": [{"product_type": "INTRADAY",
                        "transaction_type": buy_sell,
                        "quantity": quantity,
                        "price":price ,
                        "exchange": exchange,
                        "symbol_name": ticker_name,
                        "token": token_num}]} 
    response=session.estimateCharges(params)
    summary_total = response["data"]["summary"]["total_charges"]
    print(f"total charges:{summary_total}")
    
    
# session,_ = initialize_session()
# transaction_cost_of_ticker(session,"SELL",75,40,"NIFTY",71966,"NFO")

    