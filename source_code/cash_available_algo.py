# -*- coding: utf-8 -*-
"""
Created on Tue Aug 26 15:50:52 2025

@author: NARAYANA
"""
from login import initialize_session


"""
function name: available_cash
this function fetches the available cash balance from the trading account 
using the active session.

Parameters:
session : object
    An authenticated trading session object (e.g., SmartAPI session).

Returns:
float or str
    The available cash balance from the user’s account as provided by the broker API.
"""

def available_cash(session):
# Fetch funds/margin details
    response= session.rmsLimit()
    return response['data']['availablecash']


# session,_= initialize_session()
# available_cash(session)