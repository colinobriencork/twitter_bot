#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 11:49:38 2020

@author: Colin
"""

import tweepy, os

# Authenticate to Twitter
auth = tweepy.OAuthHandler(os.environ.get('TWEEPY_CONSUMER_KEY'), 
    os.environ.get('TWEEPY_CONSUMER_SECRET'))
auth.set_access_token(os.environ.get('TWEEPY_ACCESS_TOKEN'),
                     os.environ.get('TWEEPY_ACCESS_TOKEN_SECRET'))

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

