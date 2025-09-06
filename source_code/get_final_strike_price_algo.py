# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 13:40:03 2025

@author: NARAYANA
"""

"""
function name: get_all_nearest_strikes
this function finds the option strike price that is closest to the given index LTP 
and returns all option rows corresponding to that strike.

Parameters:
response : dict
    The response object from the broker API containing option chain data.
index_ltp : float
    The current LTP (Last Traded Price) of the index.

Returns:
list
    A list of option rows (dicts) matching the nearest strike price.

Raises:
ValueError
    If the response format is invalid or does not contain required data.
"""
    
def get_all_nearest_strikes(response, index_ltp):
   
    if not response.get("status") or "data" not in response:
        raise ValueError("Invalid response format")

    data = response["data"]

    # Find the strike price that is nearest to index_ltp
    nearest_strike = min(
        (float(x["strikePrice"]) for x in data),
        key=lambda sp: abs(sp - index_ltp)
    )

    # Collect all rows that match this nearest strike
    nearest_rows = [row for row in data if float(row["strikePrice"]) == nearest_strike]

    return nearest_rows

"""
function name: final_strike_price
this function determines the final strike price and option details by selecting 
the option (Call or Put) with the maximum delta among the nearest strikes.

Parameters:
indexGreeks_response : dict
    The response object containing option chain data with Greeks.
index_ltp : float, optional (default = 24771.65)
    The current LTP of the index, used to identify nearest strikes.

Returns:
tuple
    A tuple containing:
        - strike_price (int): The selected strike price.
        - option_type (str): The option type ("CE" or "PE").
        - delta (float): Delta value of the selected option.
        - gamma (float): Gamma value of the option.
        - theta (float): Theta value of the option.
        - vega (float): Vega value of the option.
        - impliedVolatility (float): IV of the option.
        - tradeVolume (float): Trade volume of the option.
"""

def final_strike_price(indexGreeks_response,index_ltp=24771.65):
    
    strike_price_response=get_all_nearest_strikes(indexGreeks_response, index_ltp)
    max_delta=max(strike_price_response[0]['delta'],strike_price_response[1]['delta'])
    for deltas in strike_price_response:
        if deltas['delta']==max_delta:
            return (int(float(deltas['strikePrice'])), deltas['optionType'],deltas['delta'],deltas['gamma'],
                    deltas['theta'],deltas['vega'],deltas['impliedVolatility'],deltas['tradeVolume'])

# strike_price, option_type, delta, theta, gamma, vega, IV ,volume= final_strike_price(indexGreeks_response,index_ltp)    