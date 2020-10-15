#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 11:43:05 2020

@author: Colin
"""
from app.oauth.tweepy_auth import api
import tweepy, time


friends = []
x = 0
for page in tweepy.Cursor(api.friends, screen_name='another_analyst', count=200).pages():
    try:
        x += 1
        print(x)
        friends.extend(page)
    except tweepy.TweepError as e:
        print("Going to sleep:", e)
        time.sleep(1)
friends = [i.screen_name for i in friends]