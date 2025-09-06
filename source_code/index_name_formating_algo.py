# -*- coding: utf-8 -*-
"""
Created on Tue Aug 26 14:15:03 2025

@author: NARAYANA
"""
from login import initialize_session,get_ticker_data

def name_formating(session, ticker_data, index_name, expiry, strike, option_type):
   
    # Build option symbol
    symbol = f"{index_name}{expiry}{strike}{option_type}"
    
    # Find token in ticker_data
    option_row = ticker_data[(ticker_data['symbol'] == symbol) & (ticker_data['exch_seg'] == "NFO")]
    
    if option_row.empty:
        print(f"Option {symbol} not found in ticker data")
        return None
    
    token = option_row.iloc[0]['token']
    print(symbol)
    print(token)
    
# session,_ = initialize_session()
# ticker_data = get_ticker_data()
# name_formating(session, ticker_data, "NIFTY","28AUG25" ,24800, "CE")
