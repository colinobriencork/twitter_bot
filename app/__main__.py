#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 19:42:21 2020

@author: Colin
"""
import app.app as app, datetime

alarm1 = datetime.time(9, 30, 0)
alarm2 = datetime.time(21, 0, 0)
query_dict = {v:k for v, k in enumerate(['#datascience', 
                                         '#dataviz'])}

query_dict_count = 0
if __name__ == "__main__":
    while True:
        if query_dict_count == len(query_dict):
            query_dict_count = 0
        app.main(alarm1, alarm2, query_dict, query_dict_count)
        query_dict_count = query_dict_count + 1