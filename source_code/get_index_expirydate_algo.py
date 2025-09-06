# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 11:06:53 2025

@author: NARAYANA
"""



import datetime
import pandas as pd
from pull_livedata import getLtp
from login import initialize_session, get_ticker_data

"""
function name: indexOptionData
this function filters the ticker data to return instruments of a given index 
from a specific exchange, separating futures contracts from options contracts.

Parameters:
ticker_data : DataFrame
    The instrument list containing all tradable symbols with details.
Index : str
    The name of the index (e.g., "NIFTY", "BANKNIFTY").
exchange : str
    The exchange segment (e.g., "NFO").

Returns:
tuple
    A tuple (futureOptions, result) where:
        - futureOptions : DataFrame containing futures contracts for the given index.
        - result : DataFrame containing all option and future contracts for the given index.
"""

def indexOptionData(ticker_data, Index, exchange):
    result = ticker_data[
        (ticker_data['symbol'].str.contains(Index, na=False)) &
        (ticker_data['exch_seg'] == exchange)
    ].reset_index(drop=True)

    futureOptions = result[result['symbol'].str.contains('FUT', na=False)]
    return futureOptions, result

"""
function name: get_expiry_date
this function determines the nearest or user-specified expiry date for index options, 
and retrieves the corresponding index LTP (spot price) and futures LTP.  

Parameters:
session : object
    An authenticated trading session object (e.g., SmartAPI session).
ticker_data : DataFrame
    The instrument list containing all tradable symbols with details.
user_trading_index : str, optional (default = "NIFTY")
    The index to trade (e.g., "NIFTY", "BANKNIFTY").
target_year : int, optional (default = None)
    The target year of expiry. If None, nearest available expiry is used.
target_month : int, optional (default = None)
    The target month of expiry. If None, nearest available expiry is used.

Returns:
tuple
    A tuple (last_month_expiry, index_ltp, future_ltp) where:
        - last_month_expiry : str, the expiry date string (raw format from ticker_data).
        - index_ltp : float, the current spot index price (LTP).
        - future_ltp : float, the current futures contract price (LTP).
    Returns (None, None, None) if no valid expiry or index data is found.
"""

def get_expiry_date(session, ticker_data, user_trading_index="NIFTY", target_year=None, target_month=None):
    # --- Step 1: Filter instrument list for index ---
    future_options, index_options_data = indexOptionData(ticker_data, user_trading_index, 'NFO')

    # --- Step 2: Parse expiry dates ---
    expiry_str = index_options_data['expiry'].astype(str).str.upper().str.strip()
    parsed = pd.Series(pd.NaT, index=index_options_data.index)

    iso_mask  = expiry_str.str.match(r"^\d{4}-\d{2}-\d{2}$", na=False)
    dmy2_mask = expiry_str.str.match(r"^\d{1,2}[A-Z]{3}\d{2}$", na=False)
    dmy4_mask = expiry_str.str.match(r"^\d{1,2}[A-Z]{3}\d{4}$", na=False)

    parsed.loc[iso_mask]  = pd.to_datetime(expiry_str.loc[iso_mask],  format='%Y-%m-%d', errors='coerce')
    parsed.loc[dmy2_mask] = pd.to_datetime(expiry_str.loc[dmy2_mask], format='%d%b%y', errors='coerce')
    parsed.loc[dmy4_mask] = pd.to_datetime(expiry_str.loc[dmy4_mask], format='%d%b%Y', errors='coerce')

    index_options_data['parsed_expiry'] = parsed
    index_options_data = index_options_data.dropna(subset=['parsed_expiry'])

    # --- Step 3: Get available expiries ---
    today = pd.to_datetime(datetime.date.today())
    available_expiries = sorted(index_options_data.loc[index_options_data['parsed_expiry'] >= today, 'parsed_expiry'].unique())
    if not available_expiries:
        return None, None, None

    # --- Step 4: If no input, pick nearest ---
    if target_year is None or target_month is None:
        nearest_dt = available_expiries[0]
        target_year = nearest_dt.year
        target_month = nearest_dt.month

    # --- Step 5: Monthly expiries ---
    monthly_expiries = [d for d in available_expiries if d.month == target_month and d.year == target_year]
    if not monthly_expiries:
        return None, None, None

    # --- Step 6: Get last expiry actual symbol from master script ---
    last_expiry_date = monthly_expiries[-1]
    expiry_row = index_options_data[index_options_data['parsed_expiry'] == last_expiry_date]
    if expiry_row.empty:
        return None, None, None
    last_month_expiry = expiry_row.iloc[0]['expiry']   # <-- take raw expiry string from ticker_data

    # --- Step 7: Spot Index LTP ---
    idx_row = ticker_data[(ticker_data['symbol'] == user_trading_index) & (ticker_data['exch_seg'] == "NSE")]
    if idx_row.empty:
        return last_month_expiry, None, None
    index_token = idx_row.iloc[0]['token']
    index_ltp = getLtp(session, user_trading_index, index_token, "NSE")

    # --- Step 8: Futures LTP ---
    fut_row = ticker_data[
    (ticker_data['symbol'].str.contains(user_trading_index, na=False)) &
    (ticker_data['symbol'].str.contains("FUT", na=False)) &
    (ticker_data['exch_seg'] == "NFO") &
    (ticker_data['expiry'] == last_month_expiry)   # match by expiry column, not string inside symbol
                                               ]

    future_ltp = None
    if not fut_row.empty:
        fut_symbol = fut_row.iloc[0]['symbol']
        fut_token = fut_row.iloc[0]['token']
        future_ltp = getLtp(session, fut_symbol, fut_token, "NFO")


    return last_month_expiry, index_ltp, future_ltp




# if __name__ == "__main__":
#     # Initialize session
#     session, _ = initialize_session()

#     # Load ticker data (instrument list)
#     ticker_data = get_ticker_data()

#     # Run algo processing for NIFTY
#     print(get_expiry_date(session, ticker_data, "NIFTY"))
    
    
#     # get_expiry_date(session, ticker_data, "NIFTY", target_year=2025, target_month=9)
#     # get_expiry_date(session, ticker_data, "NIFTY", target_year=2025, target_month=10)
    