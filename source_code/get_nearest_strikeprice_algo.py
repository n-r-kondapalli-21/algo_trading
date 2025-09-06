# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 13:40:03 2025

@author: NARAYANA
"""

    
def get_all_nearest_strikes(response, index_ltp):
    """
    Finds all option data rows from the response that have the nearest strike price to index_ltp.

    Parameters:
        response (dict): Response from optionGreek API.
        index_ltp (float): Current Index LTP value.

    Returns:
        list: List of option data rows with the nearest strike price.
    """
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


def final_strike_price(indexGreeks_response,index_ltp=24771.65):
    
    strike_price_response=get_all_nearest_strikes(indexGreeks_response, index_ltp)
    max_delta=max(strike_price_response[0]['delta'],strike_price_response[1]['delta'])
    return max_delta
    