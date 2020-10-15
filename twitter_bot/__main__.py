#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 19:42:21 2020

@author: Colin
"""
import app as app

query_count = 0
query_max = 0

if __name__ == "__main__":
    while True:
        query_count, query_max = app.main(query_count, query_max)
