

# -*- coding: utf-8 -*-
"""
Created on Mon Aug  4 20:20:34 2025

@author: NARAYANA
"""
import pandas as pd
from login import initialize_session



"""
function name:indexGreeks
this function pulls the option greeks data from api server.

Parameters:
    
session:user must be authencated before use this function.
name:script name option greeks(TCS,NIFTY etc).
expirydate:expiry date of respective script.

Returns:
it returns the option greeks data for respective script.
"""
def indexGreeks(session,expriry_date):
    params = {
                "name":"NIFTY", #Here Name represents the Underlying stock
                "expirydate":expriry_date           
            }
    response = session.optionGreek(params)
    # print(response)
    return(response)
    # df=pd.DataFrame(response)
    # df.to_csv("indexgreeks.csv", index=False)
    

# session,_ = initialize_session() 
# indexGreeks(session) 
   
   


