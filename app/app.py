#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 20:11:48 2020

@author: Colin
"""
import app.actions as actions

def main(alarm1, alarm2, query_dict, query_dict_count):
    
    actions.follow_query_users(query_dict[query_dict_count], 
                               less_followers_than=3000, 
                               less_friends_than=3000, 
                               add_deleted_users_since=60,
                               alarm1 = alarm1,
                               alarm2 = alarm2)
    actions.friend_followers()
    actions.like_tweets()
    actions.tweet()
    actions.insert_friend()
    actions.insert_un_newly_followed()
    actions.delete_old_friends(how_old = 5)