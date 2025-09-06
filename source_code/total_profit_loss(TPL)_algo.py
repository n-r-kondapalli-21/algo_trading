# -*- coding: utf-8 -*-
"""
Created on Sat Aug 23 17:30:00 2025

@author: NARAYANA
"""

def calculate_tpl(pl_list):
   
    tpl_list = []
    cumulative = 0
    for pl in pl_list:
        cumulative += pl
        tpl_list.append(cumulative)
    print(tpl_list)

pl = -249.1113
pl_values = [pl]   # ✅ put float into a list
calculate_tpl(pl_values)



