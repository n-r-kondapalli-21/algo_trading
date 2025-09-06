# -*- coding: utf-8 -*-
"""
Created on Fri Aug 29 16:23:39 2025

@author: NARAYANA
"""
"""
function name: decide_quantity
this function adjusts the user’s desired trade quantity to the nearest valid 
multiple of the specified lot size.

Parameters:
desired_qty : int
    The quantity the user wants to trade.
lot_size : int, optional (default = 75)
    The minimum tradable lot size. The final quantity must be a multiple of this value.

Returns:
int
    The adjusted valid trade quantity:
        - 0 if the desired quantity is less than or equal to 0.
        - Nearest multiple of lot_size otherwise.
"""

def decide_quantity(desired_qty, lot_size=75):
   
    if desired_qty <= 0:
        return 0  
        

    # Round to nearest multiple of lot size
    remainder = desired_qty % lot_size
    if remainder == 0:
        return desired_qty
    else:
        # Decide whether to round up or down
        if remainder >= lot_size / 2:
            return desired_qty + (lot_size - remainder)  # round up
        else:
            return desired_qty - remainder  # round down
        
# print(decide_quantity(78, lot_size=75))
