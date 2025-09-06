# -*- coding: utf-8 -*-
"""
Created on Tue Aug 26 15:50:52 2025

@author: NARAYANA
"""
from login import initialize_session



def available_cash(session):
# Fetch funds/margin details
    response= session.rmsLimit()
    print(response['data']['availablecash'])


session,_= initialize_session()
available_cash(session)