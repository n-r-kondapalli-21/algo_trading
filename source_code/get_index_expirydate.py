# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 2025
@author: NARAYANA
"""

import datetime
import pandas as pd
from pull_livedata import getLtp
from login import initialize_session, get_ticker_data


# Returns future and index option data
def indexOptionData(ticker_data, Index, exchange):
    result = ticker_data[
        (ticker_data['symbol'].str.contains(Index, na=False)) &
        (ticker_data['exch_seg'] == exchange)
    ].reset_index(drop=True)

    futureOptions = result[result['symbol'].str.contains('FUT', na=False)]
    return futureOptions, result


def niftyAlgoProcessing(session, ticker_data, user_trading_index="NIFTY"):
    # --- Step 1: Filter instrument list for index ---
    future_options, index_options_data = indexOptionData(ticker_data, user_trading_index, 'NFO')

    # --- Step 2: Parse expiry dates safely ---
    expiry_str = index_options_data['expiry'].astype(str).str.upper().str.strip()

    iso_mask  = expiry_str.str.match(r"^\d{4}-\d{2}-\d{2}$", na=False)
    dmy2_mask = expiry_str.str.match(r"^\d{1,2}[A-Z]{3}\d{2}$", na=False)
    dmy4_mask = expiry_str.str.match(r"^\d{1,2}[A-Z]{3}\d{4}$", na=False)

    parsed = pd.Series(pd.NaT, index=index_options_data.index)
    if iso_mask.any():
        parsed.loc[iso_mask]  = pd.to_datetime(expiry_str.loc[iso_mask],  format='%Y-%m-%d', errors='coerce')
    if dmy2_mask.any():
        parsed.loc[dmy2_mask] = pd.to_datetime(expiry_str.loc[dmy2_mask], format='%d%b%y', errors='coerce')
    if dmy4_mask.any():
        parsed.loc[dmy4_mask] = pd.to_datetime(expiry_str.loc[dmy4_mask], format='%d%b%Y', errors='coerce')

    # Fallback for unknown formats
    fallback_mask = ~(iso_mask | dmy2_mask | dmy4_mask)
    if fallback_mask.any():
        parsed.loc[fallback_mask] = pd.to_datetime(expiry_str.loc[fallback_mask], errors='coerce')

    index_options_data['parsed_expiry'] = parsed
    index_options_data = index_options_data.dropna(subset=['parsed_expiry'])

    # --- Step 3: Available expiries ---
    today = pd.to_datetime(datetime.date.today())
    available_expiries = sorted(index_options_data.loc[index_options_data['parsed_expiry'] >= today, 'parsed_expiry'].unique())

    if len(available_expiries) == 0:
        print("No valid expiry found for", user_trading_index)
        return

    print(f"Available Expiries for {user_trading_index}:")
    expiry_strings = [pd.to_datetime(e).strftime("%d%b%y").upper() for e in available_expiries]
    for e in expiry_strings:
        print(f"-> {e}")
    print()

       # --- Step 4: Nearest, farthest, last monthly ---
    nearest_dt = available_expiries[0]
    nearest_str = pd.to_datetime(nearest_dt).strftime("%d%b%y").upper()
    farthest_str = pd.to_datetime(available_expiries[-1]).strftime("%d%b%y").upper()

    nearest_month = nearest_dt.month
    nearest_year = nearest_dt.year
    monthly_expiries = [d for d in available_expiries if d.month == nearest_month and d.year == nearest_year]
    last_month_dt = monthly_expiries[-1]
    expiry_row = index_options_data[index_options_data['parsed_expiry'] == last_month_dt]
    if expiry_row.empty:
        print(f"No expiry row found for {last_month_dt}")
        return
    last_month_expiry = expiry_row.iloc[0]['expiry']   # <-- raw expiry from master script


    print(f"Nearest Expiry: {nearest_str}")
    print(f"Farthest Expiry: {farthest_str}")
    print(f"Last Monthly Expiry: {last_month_expiry}")
    print()

    # --- Step 5: Get Futures row from ticker_data (use LAST MONTHLY expiry) ---
    fut_row = ticker_data[
    (ticker_data['exch_seg'] == "NFO") &
    (ticker_data['symbol'].str.startswith(user_trading_index, na=False)) &  # stricter filter
    (ticker_data['symbol'].str.contains("FUT", na=False)) &
    (ticker_data['expiry'] == last_month_expiry)   # match exact expiry from master script
     ]



    if fut_row.empty:
        print(f"No FUT found in ticker_data for expiry {last_month_expiry}")
        return

    fut_symbol = fut_row.iloc[0]['symbol']
    fut_token = fut_row.iloc[0]['token']


    # --- Step 6: Spot Index LTP ---
    idx_row = ticker_data[(ticker_data['symbol'] == user_trading_index) & (ticker_data['exch_seg'] == "NSE")]
    if idx_row.empty:
        print(f"Index {user_trading_index} not found in NSE segment")
        return
    index_token = idx_row.iloc[0]['token']
    index_ltp = getLtp(session, user_trading_index, index_token, "NSE")

    # --- Step 7: Futures LTP ---
    future_ltp = getLtp(session, fut_symbol, fut_token, "NFO")

    # --- Step 8: Print results ---
    print(f"Index: {user_trading_index}, Token: {index_token}, LTP: {index_ltp}")
    print(f"Future: {fut_symbol}, Token: {fut_token}, LTP: {future_ltp}")




if __name__ == "__main__":
    # Initialize session
    session, _ = initialize_session()

    # Load ticker data (instrument list)
    ticker_data = get_ticker_data()

    # Run algo processing for NIFTY
    niftyAlgoProcessing(session, ticker_data, "NIFTY")
