from SmartApi import SmartConnect
import os
from pyotp import TOTP
import urllib
import json
import pandas as pd


"""
    function name: login
    this function logs into the SmartAPI platform and retrieves authentication tokens.
    
    Parameters:
    None
    
    Returns:
    it returns a dictionary containing:
        - feedToken: feed token for streaming data
        - userProfile: user profile details
        - jwtToken: JWT authentication token
        - login: SmartConnect object for API calls
        - refreshToken: token for refreshing the session
        - secret_key: stored API credentials
    """
def login():
    key_path = r"D:\SmartAPI_keys"
    os.chdir(key_path)

    key_secret = open("login.txt","r").read().split()

    login=SmartConnect(api_key=key_secret[0],timeout=20)# apikey
    data = login.generateSession(key_secret[1],key_secret[2],TOTP(key_secret[3]).now()) #usrname,pwd,totp
    refreshToken= data['data']['refreshToken']

    #fetch the feedtoken
    feedToken=login.getfeedToken()

    #fetch User Profile 
    userProfile= login.getProfile(refreshToken)
    
    #fetch jwtToken
    jwtToken =  data['data']['jwtToken']
    params = {
                "feedToken":feedToken,
                "userProfile":userProfile,
                "jwtToken":jwtToken,
                "login":login,
                "refreshToken":refreshToken,
                "secret_key" : key_secret
                }
    return params


"""
    function name: initialize_session
    this function initializes the SmartAPI session.
    
    Parameters:
    None
    
    Returns:
    it returns a tuple (session, logindata):
        - session: SmartConnect object for making API calls
        - logindata: dictionary containing authentication details from login()
    """
def initialize_session():
    logindata = login()
    session = logindata['login']
    return session, logindata

"""
    function name: getExchangeTickers
    this function fetches the complete list of instruments from Angel Broking API.
    
    Parameters:
    None
    
    Returns:
    it returns a list of dictionaries containing instrument details.
    """
def getExchangeTickers():
    instrument_url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
    response = urllib.request.urlopen(instrument_url)
    instrument_list = json.loads(response.read())
    instru=instrument_list
    return instru


"""
    function name: get_ticker_data
    this function returns the complete instrument list as a pandas DataFrame.
    
    Parameters:
    None
    
    Returns:
    it returns a DataFrame containing all instrument details.
    """
def get_ticker_data():
    instrument_list = getExchangeTickers()
    return pd.DataFrame(instrument_list)

"""
    function name: get_nifty_tickers
    this function returns only NIFTY related instruments.
    
    Parameters:
    None
    
    Returns:
    it returns a DataFrame containing only NIFTY instruments.
    """
def get_nifty_tickers():
    
    """Return only NIFTY related instruments."""
    n_data= getExchangeTickers()
    df=pd.DataFrame(n_data)
    return df[df['name'].str.upper() == 'NIFTY28AUG2524800CE'].reset_index(drop=True)


"""
    function name: get_banknifty_tickers
    this function returns only BANKNIFTY related instruments.
    
    Parameters:
    None
    
    Returns:
    it returns a DataFrame containing only BANKNIFTY instruments.
    """
def get_banknifty_tickers():
    """Return only BANKNIFTY related instruments."""
    bn_data= getExchangeTickers()
    df=pd.DataFrame(bn_data)
    return df[df['name'].str.upper() == 'BANKNIFTY'].reset_index(drop=True)

"""
    function name: get_sensex_tickers
    this function returns only SENSEX related instruments.
    
    Parameters:
    None
    
    Returns:
    it returns a DataFrame containing only SENSEX instruments.
    """
def get_sensex_tickers():
    """Return only SENSEX related instruments."""
    s_data= getExchangeTickers()
    df=pd.DataFrame(s_data)
    return df[df['name'].str.upper() == 'SENSEX'].reset_index(drop=True)

def getToken(tiker_name,ticker_data,exchange="NSE"):
    global Ticker
    global TickerToken
    #nifty and banknifty details
    Ticker = ticker_data[ticker_data['name']==tiker_name]
    TickerToken = (Ticker.iloc[0,Ticker.columns.get_loc('token')])
    return TickerToken   

