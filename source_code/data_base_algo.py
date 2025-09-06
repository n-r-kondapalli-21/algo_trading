# -*- coding: utf-8 -*-
"""
Created on Sat Aug 30 17:38:45 2025
@author: NARAYANA
"""
import sqlite3

DB_FILE = r"D:\alpha inventors_training\algo_data_bases\algo_trades_1.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

def initialize_db(table_name: str):
    """Create table if not exists."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        S_no INTEGER,
        SYMBOL TEXT,
        Ts TEXT,
        B_S_Quant INTEGER,
        Tc REAL,
        PL REAL,               -- NULL or FLOAT
        unrealized_PL REAL,
        Td TEXT,
        TPL REAL,              -- NULL or FLOAT
        delta REAL,
        gamma REAL,
        theta REAL,
        vega REAL,
        IV REAL,
        volume REAL,
        cash REAL,
        OI REAL,
        FUTURE_LTP REAL,
        INDEX_LTP REAL,
        MML REAL,
        MMP REAL,
        DD REAL                -- NULL or FLOAT
    )
    """)
    conn.commit()
    conn.close()


def insert_trade(rows: dict, table_name: str):
    """Insert trade row, auto-create table if needed."""
    conn = get_connection()
    cur = conn.cursor()

    # Ensure nullable floats handled correctly
    for key in ["PL", "TPL", "DD"]:
        if rows.get(key) is not None:
            try:
                rows[key] = float(rows[key])
            except:
                rows[key] = None

    try:
        cur.execute(f"""
            INSERT INTO {table_name} (
                S_no, SYMBOL, Ts, B_S_Quant, Tc, PL, unrealized_PL, Td, TPL,
                delta, theta, gamma, vega, IV, volume, cash, OI, FUTURE_LTP,
                INDEX_LTP, MML, MMP, DD
            ) VALUES (
                :S_no, :SYMBOL, :Ts, :B_S_Quant, :Tc, :PL, :unrealized_PL, :Td, :TPL,
                :delta, :theta, :gamma, :vega, :IV, :volume, :cash, :OI, :FUTURE_LTP,
                :INDEX_LTP, :MML, :MMP, :DD
            )
        """, rows)
    except sqlite3.OperationalError as e:
        if "no such table" in str(e).lower():
            initialize_db(table_name)  # Auto-create
            cur.execute(f"""
                INSERT INTO {table_name} (
                    S_no, SYMBOL, Ts, B_S_Quant, Tc, PL, unrealized_PL, Td, TPL,
                    delta, theta, gamma, vega, IV, volume, cash, OI, FUTURE_LTP,
                    INDEX_LTP, MML, MMP, DD
                ) VALUES (
                    :S_no, :SYMBOL, :Ts, :B_S_Quant, :Tc, :PL, :unrealized_PL, :Td, :TPL,
                    :delta, :theta, :gamma, :vega, :IV, :volume, :cash, :OI, :FUTURE_LTP,
                    :INDEX_LTP, :MML, :MMP, :DD
                )
            """, rows)
        else:
            raise

    conn.commit()
    conn.close()
