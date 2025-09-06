# -*- coding: utf-8 -*-
"""
Created on Tue Aug 26 14:15:03 2025

@author: NARAYANA
"""
from login import initialize_session,get_ticker_data


"""
function name: indexGreeks
this function fetches the latest traded price (LTP) and open interest (OI) 
for a given option or futures instrument using the broker API.

Parameters:
session : object
    An authenticated trading session object (e.g., SmartAPI session).
token : str or int
    The token number of the instrument (as required by the broker API).

Returns:
tuple
    A tuple (ltp, open_interest) where:
        - ltp is the latest traded price of the instrument.
        - open_interest is the current open interest of the instrument.
"""

def indexGreeks(session,token):
 
    mode= "FULL"
    exchangeTokens= {"NFO":[token]}
    response = session.getMarketData(mode,exchangeTokens)
    return response['data']['fetched'][0]['ltp'],response['data']['fetched'][0]['opnInterest']
 

"""
function name: format_expiry_for_symbol
this function converts an expiry string from Angel One’s format 
(e.g., "30SEP2025") into a shorter tradable format ("30SEP25").

Parameters:
expiry_str : str
    The expiry date string in broker format.

Returns:
str
    The formatted expiry string in tradable format.
"""
   
def format_expiry_for_symbol(expiry_str):
    """
    Convert Angel One expiry (e.g., 30SEP2025) into tradable format (30SEP25).
    """
    if len(expiry_str) == 9:  # e.g., 30SEP2025
        # keep day + month + last 2 digits of year
        return expiry_str[:5] + expiry_str[-2:]
    return expiry_str  # if already short format (30SEP25)



"""
function name: name_formatting
this function builds the option symbol for a given index, expiry, strike, 
and option type, then fetches its token, lot size, LTP, and open interest.

Parameters:
session : object
    An authenticated trading session object (e.g., SmartAPI session).
ticker_data : DataFrame
    The instrument list containing symbol, token, and lot size information.
index_name : str
    The name of the index (e.g., NIFTY, BANKNIFTY).
expiry : str
    The expiry date in Angel One format (e.g., 30SEP2025).
strike : int or float
    The strike price of the option.
option_type : str
    The type of option ("CE" for Call, "PE" for Put).

Returns:
tuple or None
    - Returns (symbol, token, lot_size, ltp, open_interest) if the option is found.
    - Returns None if the option symbol is not found in the ticker data.
"""

def name_formatting(session, ticker_data, index_name, expiry, strike, option_type):
    """
    Returns option symbol, token, lot size, and current LTP.
    """
    # Build option symbol
    expiry_for_symbol = format_expiry_for_symbol(expiry)
    
    symbol = f"{index_name}{expiry_for_symbol}{strike}{option_type}"
    
    # Find token in ticker_data
    option_row = ticker_data[(ticker_data['symbol'] == symbol) & (ticker_data['exch_seg'] == "NFO")]
    
    if option_row.empty:
        print(f"Option {symbol} not found in ticker data")
        return None
    
    token = option_row.iloc[0]['token']
    lot_size = option_row.iloc[0]['lotsize']   # Extract lot size
    
    ltp,openinterest=indexGreeks(session,token)
    
    return symbol, token, lot_size, ltp, openinterest

    
# session,_ = initialize_session()
# ticker_data = get_ticker_data()
# print(name_formatting(session, ticker_data, "NIFTY","30SEP2025" ,24800, "CE"))
