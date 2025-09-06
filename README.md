## Algo Trading Project

This project is an algorithmic trading system built using Python and Angel One SmartAPI. It automates trading strategies, fetches market data, and executes buy/sell orders with predefined conditions.

### Features
-Connects to Angel One SmartAPI for real-time market data
-Automated order execution (BUY/SELL/HOLD logic)
-Error handling and reconnection support
-Strategy-based trading (customizable rules)

### Repository Structure
algo-trading-project/
│── source_code/ # Core trading scripts and strategy logic
│ ├── main.py # Orchestrates the trading loop and execution flow
│ ├── login.py # SmartAPI authentication; instrument master download; DataFrame helpers
│ ├── pull_livedata.py # Utilities to fetch LTP for indices and symbols
│ ├── get_index_expirydate_algo.py # Finds nearest/monthly expiry; fetches index & futures LTP
│ ├── index_name_formatting_algo.py# Builds option symbols; resolves token, lot size, LTP, OI
│ ├── get_option_greeks_algo.py # Fetches option Greeks (Delta, Gamma, Theta, Vega) via SmartAPI
│ └── transaction_cost_algo.py # Estimates transaction charges for BUY/SELL/HOLD operations
│
│── application/ # Main application files to run trading bot
│
│── sample_test/ # Example test cases or demo scripts
│
│── requirements.txt # Python dependencies
│── README.md # Project documentation

### Requirements
- OS: Windows 10+
- Python: 3.9+
- Angel One SmartAPI account with API key and TOTP secret

### Installation
Clone the repository:
git https://github.com/n-r-kondapalli-21/algo_trading
cd algo_trading

Create and activate a virtual environment (optional but recommended):
conda create -n algo_trading python=3.9
conda activate algo_trading

Install dependencies:
pip install -r requirements.txt

### Configuration
  SmartAPI credentials:
- Create the directory: `D:\SmartAPI_keys`
- Create a file `login.txt` at `D:\SmartAPI_keys\login.txt` with four whitespace-separated values in a single line:
  - api_key username password totp_secret

Example (do not commit real keys):
```
your_api_key your_username your_password JBSWY3DPEHPK3PXP
```
The app reads this file in `login.py` and generates a session using TOTP.

### Running
From the project root:

```bash
python main.py
```
What it does:
- Waits for internet connectivity.
- Logs into SmartAPI and downloads the instrument master.
- Initializes a SQLite table named like `NIFTY_trades_YYYY_MM_DD_HH_MM_SS`.
- Repeatedly executes a trade cycle: resolve expiry, fetch greeks, select strike, decide action/qty, estimate costs, compute P&L metrics, and        insert a row into the DB.
- Handles transient timeouts/connection errors with backoff and re-login.

To stop: press `CTRL+C` (gracefully signals the worker thread to stop).

### Future Improvements
-Add backtesting module
-Implement multiple trading strategies
-Support for more brokers
-Web dashboard for monitoring trades

### Disclaimer
This software is provided "as is" without warranties. Use at your own risk. Always comply with your broker’s terms and market regulations.

