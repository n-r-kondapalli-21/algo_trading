  ## Algo Trading Project

Python-based options trading framework that connects to Angel One SmartAPI to fetch instruments and market data, compute option signals, estimate transaction costs, and log trades to SQLite.

### Features
- Index option workflow for NIFTY (extendable to BANKNIFTY/SENSEX)
- Expiry resolution and symbol construction for options/futures
- Option Greeks retrieval and strike selection
- Quantity estimation and buy/sell/hold decisioning
- Transaction cost estimation (brokerage, taxes, etc.)
- P&L, TPL, unrealized P&L, margin levels (MML/MMP), Delta Diff (DD)
- Trade persistence to SQLite database
- Resilient loop with reconnection and error handling

### Repository Structure
- `main.py`: Orchestrates the trading loop, calling all helper modules.
- `login.py`: SmartAPI authentication; instrument master download; helpers to build instrument DataFrames.
- `pull_livedata.py`: LTP utilities for indices and symbols.
- `get_index_expirydate_algo.py`: Finds nearest/monthly expiry; fetches index and futures LTP.
- `index_name_formatting_algo.py`: Builds option symbols, resolves token, lot size, LTP, OI.
- `get_option_greeks_algo.py`: Fetches option Greeks for a given underlying and expiry via SmartAPI.
- `transaction_cost_algo.py`: Estimates transaction charges for BUY/SELL/HOLD using SmartAPI.
- `data_base_algo.py`: Creates a SQLite table and inserts trade rows.
- Other `*_algo.py`: Business logic modules for strike selection, buy/sell action, P&L, TPL, delta diff, etc.

### Requirements
- OS: Windows 10+
- Python: 3.9+
- Angel One SmartAPI account with API key and TOTP secret

### Python Dependencies
Install globally or in a virtual environment:

```bash
pip install smartapi-python pyotp pandas requests
```

Modules from the standard library (no install): `sqlite3`, `json`, `urllib`, `time`, `threading`, `socket`, `datetime`.

### Configuration
1) SmartAPI credentials
- Create the directory: `D:\SmartAPI_keys`
- Create a file `login.txt` at `D:\SmartAPI_keys\login.txt` with four whitespace-separated values in a single line:
  - api_key username password totp_secret

Example (do not commit real keys):
```
your_api_key your_username your_password JBSWY3DPEHPK3PXP
```

The app reads this file in `login.py` and generates a session using TOTP.

2) SQLite database location
- The default DB path is defined in `data_base_algo.py`:
  - `DB_FILE = r"D:\\alpha inventors_training\\algo_data_bases\\algo_trades.db"`
- Ensure this directory exists, or change the path to a valid location you control.

### Running
From the project root:

```bash
python main.py
```

What it does:
- Waits for internet connectivity.
- Logs into SmartAPI and downloads the instrument master.
- Initializes a SQLite table named like `NIFTY_trades_YYYY_MM_DD_HH_MM_SS`.
- Repeatedly executes a trade cycle: resolve expiry, fetch greeks, select strike, decide action/qty, estimate costs, compute P&L metrics, and insert a row into the DB.
- Handles transient timeouts/connection errors with backoff and re-login.

To stop: press `CTRL+C` (gracefully signals the worker thread to stop).

### Customization
- Ticker/index: `trade_cycle(..., ticker_name="NIFTY")` in `main.py`.
- Lot size/quantity: `buy_sell_quantity` in `main.py` and the quantity logic in `buy_sell_qunatity_estimation_algo.py`.
- Strike selection and action logic: `get_final_strike_price_algo.py`, `buy_sell_action_algo.py`.
- Costs and P&L logic: `transaction_cost_algo.py`, `profit_loss_algo.py`, `total_profit_loss_algo.py`, `unrealized_PL_algo.py`.

### Data Model (SQLite)
`data_base_algo.initialize_db(table_name)` creates a table with columns including:
- `S_no`, `SYMBOL`, `Ts`, `B_S_Quant`, `Tc`, `PL`, `unrealized_PL`, `Td`, `TPL`,
- `delta`, `gamma`, `theta`, `vega`, `IV`, `volume`, `cash`, `OI`,
- `FUTURE_LTP`, `INDEX_LTP`, `MML`, `MMP`, `DD`.

### Notes and Caveats
- Hard-coded Windows paths exist in `login.py` and `data_base_algo.py`. Update them to your environment if needed.
- The code references many `*_algo.py` logic modules. Ensure each is implemented and consistent with current API responses.
- SmartAPI rate limits and session timeouts may require tuning retry intervals in `main.py`.
- This code is intended for educational purposes; live trading carries significant risk. Validate logic with paper trading before using real capital.

### Troubleshooting
- No internet: The loop waits and retries. Ensure connectivity.
- Login fails: Verify `login.txt` values and TOTP secret, API key activation, and system time sync.
- Instrument not found: The symbol format must match the instrument master. Confirm expiry formatting in `index_name_formatting_algo.py` and that the instrument master is up-to-date.
- DB errors: Create the DB directory or change `DB_FILE` to a valid path.
- Missing packages: Re-run `pip install` with the packages listed above.

### Disclaimer
This software is provided "as is" without warranties. Use at your own risk. Always comply with your broker’s terms and market regulations.


