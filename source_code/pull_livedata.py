
"""
    Function Name:
    getLtp

    Description:
    Fetches the Last Traded Price (LTP) for a given trading symbol from the specified exchange.

    Parameters:
    session (object): Active trading API session object.
    tradingsymbol (str): Trading symbol (e.g., 'NIFTY', 'BANKNIFTY').
    symboltoken (str/int): Token representing the symbol.
    exchange (str): Exchange code (default is "NFO").

    Returns:
    float: Last traded price of the given symbol.
    """
def getLtp(session,tradingsymbol,symboltoken,exchange="NFO"):
    params = {
                "tradingsymbol":tradingsymbol,
                "symboltoken": symboltoken
             }
    response = session.ltpData(exchange, params["tradingsymbol"], params["symboltoken"])
    return response["data"]['ltp']


"""
    Function Name:
    getNiftyTokenLtp

    Description:
    Retrieves the token for the NIFTY index from ticker data and fetches its LTP.

    Parameters:
    session (object): Active trading API session object.
    Nticker_data (DataFrame): DataFrame containing instruments list with 'name' and 'token' columns.

    Returns:
    float: Last traded price of NIFTY.
    """
def getNiftyTokenLtp(session,Nticker_data):
    global Nifty
    global NiftyToken  
    Nifty = Nticker_data[Nticker_data['name']=="NIFTY"]
    NiftyToken = (Nifty.iloc[0,Nifty.columns.get_loc('token')])
    print(f"Nifty token:{NiftyToken}")
    responce = getLtp(session,'NIFTY',NiftyToken,'NSE')
    print(f"Nifty live data:{responce}")
    return responce

"""
    Function Name:
    getBankNiftyTokenLtp

    Description:
    Retrieves the token for the BANKNIFTY index from ticker data and fetches its LTP.

    Parameters:
    session (object): Active trading API session object.
    Nticker_data (DataFrame): DataFrame containing instruments list with 'name' and 'token' columns.

    Returns:
    float: Last traded price of BANKNIFTY.
    """
def getBankNiftyTokenLtp(session,Nticker_data):
    global BankNifty
    global BankNiftyToken
    BankNifty = Nticker_data[Nticker_data['name']=="BANKNIFTY"]
    BankNiftyToken = (BankNifty.iloc[0,BankNifty.columns.get_loc('token')])
    print(f"BankNifty token:{BankNiftyToken}")
    responce = getLtp(session,'BANKNIFTY',BankNiftyToken,'NSE')
    print(f"BankNifty live data:{responce}")
    return responce

"""
    Function Name:
    getSensexTokenLtp

    Description:
    Retrieves the token for the SENSEX index from ticker data and fetches its LTP.

    Parameters:
    session (object): Active trading API session object.
    Nticker_data (DataFrame): DataFrame containing instruments list with 'name' and 'token' columns.

    Returns:
    float: Last traded price of SENSEX.
    """
def getSensexTokenLtp(session,Nticker_data):
    global Sensex
    global SensexToken
    Sensex = Nticker_data[Nticker_data['name']=="SENSEX"]
    SensexToken = (Sensex.iloc[0,Sensex.columns.get_loc('token')])
    print(f"Sensex token:{ SensexToken}")
    responce = getLtp(session,'SENSEX',SensexToken,'BSE')
    print(f"Sensex live data:{responce}")
    return responce