# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 11:06:53 2025

@author: NARAYANA
"""

import time
from login import initialize_session, get_ticker_data
from get_index_expirydate_algo import get_expiry_date
from get_option_greeks_algo import indexGreeks
from get_final_strike_price_algo import final_strike_price
from index_name_formatting_algo import name_formatting
from transaction_cost_algo import transaction_cost_of_ticker,transaction_cost_on_HOLD
from cash_available_algo import available_cash
from profit_loss_algo import calculate_PL
from total_profit_loss_algo import calculate_tpl
from unrealized_PL_algo import calculate_unreal_PL
from MML_MMP_algo import update_MML_MMP
from buy_sell_qunatity_estimation_algo import decide_quantity
from delta_diff_algo import delta_diff
from buy_sell_action_algo import buy_sell_action
from data_base_algo import initialize_db, insert_trade
from trade_prices_algo import buy_sell_prices
import threading
import requests 
import socket

TABLE_NAME = "NIFTY_trades_" + time.strftime("%Y_%m_%d_%H_%M_%S")
buy_sell_quantity=75


def trade_cycle(session, ticker_data, ticker_name="NIFTY"):
    """
function_name: trade_cycle

Parameters:
    session : SmartConnect
        Active trading API session object used to fetch market data and place trades.
    ticker_data : DataFrame
        Instrument list or ticker details used to extract strike and token information.
    ticker_name : str, optional (default="NIFTY")
        Name of the index or ticker symbol to trade on.

Returns:
    None
        Executes a complete trade cycle by:
        - Fetching expiry, option greeks, strike details, and LTP.
        - Deciding buy/sell/hold action and trade quantity.
        - Calculating transaction cost, profit/loss, TPL, unrealized PL.
        - Updating margin levels (MML, MMP) and delta difference (DD).
        - Inserting trade details into the database table.
"""


    expiry_date, index_ltp, future_ltp = get_expiry_date(session, ticker_data, ticker_name)
    # indexGreeks_response = indexGreeks(session, expiry_date)

    strike_price, option_type, delta, gamma, theta, vega, IV, volume = final_strike_price(indexGreeks_response, index_ltp)
    formatted_index_symbol, index_token, lotsize, ltp, openinterest = name_formatting(session, ticker_data, ticker_name, expiry_date, strike_price, option_type)

    b_s_quantity = decide_quantity(buy_sell_quantity, int(lotsize))
    sno, time_stamp, action = buy_sell_action(buy_sell_quantity, float(delta))

    buy_price, sell_price = buy_sell_prices(action, ltp)
    
    transaction_cost_db=transaction_cost_on_HOLD(session, action, buy_sell_quantity, buy_price, sell_price, ticker_name, index_token, "NFO")

    transaction_cost = transaction_cost_of_ticker(session, action, buy_sell_quantity, buy_price, sell_price, ticker_name, index_token, "NFO",ltp)
    Profit_loss = calculate_PL(buy_price, sell_price, buy_sell_quantity, transaction_cost, action)
    total_profit_loss = calculate_tpl(Profit_loss)

    cash_available = available_cash(session)
    unrealized_PL = calculate_unreal_PL(buy_price, ltp, buy_sell_quantity, transaction_cost, action)
    mml, mmp = update_MML_MMP(unrealized_PL)
    DD = delta_diff(delta)

    rows = {
        "S_no": sno, "SYMBOL": formatted_index_symbol, "Ts": time_stamp,
        "B_S_Quant": b_s_quantity, "Tc": transaction_cost_db, "PL": Profit_loss,
        "unrealized_PL": unrealized_PL, "Td": action, "TPL": total_profit_loss,
        "delta": delta, "gamma": gamma, "theta": theta, "vega": vega,
        "IV": IV, "volume": volume, "cash": cash_available, "OI": openinterest,
        "FUTURE_LTP": future_ltp, "INDEX_LTP": index_ltp, "MML": mml,
        "MMP": mmp, "DD": DD
    }

    insert_trade(rows, TABLE_NAME)

    if action == "SELL":
        time.sleep(5)







stop_event = threading.Event()

def internet_available(host="8.8.8.8", port=53, timeout=3):
    """Check internet connectivity by connecting to Google DNS."""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

def main_loop():
    while not stop_event.is_set():
        try:
            # Wait until internet is available before trying login
            while not internet_available() and not stop_event.is_set():
                print("[No Internet] Waiting for connection...")
                time.sleep(10)

            # Initialize session + setup
            session, logindata = initialize_session()
            ticker_data = get_ticker_data()
            initialize_db(TABLE_NAME)

            print("[Info] Trading session initialized.")

            while not stop_event.is_set():
                try:
                    trade_cycle(session, ticker_data, "NIFTY")

                except requests.exceptions.ReadTimeout as e:
                    print(f"[Timeout Error] {e}. Retrying in 10s...")
                    time.sleep(10)
                    break  # re-login in outer loop

                except requests.exceptions.ConnectionError as e:
                    print(f"[Connection Error] {e}. Retrying in 20s...")
                    time.sleep(20)
                    break  # re-login in outer loop

                except Exception as e:
                    print(f"[Trade Error] {e}. Retrying in 5s...")
                    time.sleep(5)

                time.sleep(5)

        except Exception as e:
            print(f"[Init Error] {e}. Retrying in 15s...")
            time.sleep(15)

# Run trading loop in a separate thread
threadws = threading.Thread(target=main_loop, daemon=True)
threadws.start()

# Keep main thread alive and allow CTRL+C to stop
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopping...")
    stop_event.set()
    threadws.join()




	

