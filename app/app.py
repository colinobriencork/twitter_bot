#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 20:11:48 2020

@author: Colin
"""
import app.actions as actions, datetime

def main(query_count, query_max):
    print(1)
    actions.friend_followers()
    print(2)
    actions.like_tweets()
    print(3)
    actions.tweet()
    print(4)
    actions.insert_friend()
    print(5)
    actions.insert_un_newly_followed()
    print(6)
    actions.delete_old_friends(how_old = 5)
    print(7)
    query_count, query_max = actions.follow_query_users(query_count,
                                                        query_max,
                                                        less_followers_than=3000, 
                                                        less_friends_than=3000, 
                                                        add_deleted_users_since=60,
                                                        alarm1 = datetime.time(9, 30, 0),
                                                        alarm2 = datetime.time(21, 0, 0))
    return query_count, query_max