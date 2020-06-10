#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 11:43:05 2020

@author: Colin
"""
import app.actions as actions, datetime

alarm1 = datetime.time(9, 30, 0)
alarm2 = datetime.time(21, 0, 0)

actions.follow_query_users('#datascience', 
                           less_followers_than=3000, 
                           less_friends_than=3000, 
                           add_deleted_users_since=60,
                           alarm1 = alarm1,
                           alarm2 = alarm2)