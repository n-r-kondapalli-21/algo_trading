# # -*- coding: utf-8 -*-
# """
# Created on Mon Aug 25 16:26:40 2025

# @author: NARAYANA
# """
# from login import initialize_session,getToken




# def market_order(session, ticker_name,buy_sell,quantity,ticker_data,exchange="NFO"): 
#     params = {
#                 "variety":"NORMAL",
#                 "tradingsymbol":"{}-EQ".format(ticker_name),
#                 "symboltoken":getToken(ticker_name,ticker_data,exchange),
#                 "transactiontype":buy_sell,
#                 "exchange":"NFO",
#                 "ordertype":"MARKET",
#                 "producttype":"INTRADAY",
#                 "duration":"DAY",
#                 "quantity":quantity
#             }
#     order = session.placeOrder(params)
#     return order

  
    
    
# session,ticker_data = initialize_session()
# market_order(session, "TCS","BUY",1,ticker_data)

    
   
    



