#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 19:36:01 2020

@author: Colin
"""
from oauth.tweepy_auth import api
from oauth.gspread_auth import client
from datetime import datetime
from worksheet_dict import worksheet
import tweepy, time

class TweepyInfo():
    
    api = api
         
    def get_user_followers(self, user_name):
        followers = []
        for page in tweepy.Cursor(api.followers, screen_name=user_name, count=200).pages():
            try:
                followers.extend(page)
            except tweepy.TweepError as e:
                print("Going to sleep:", e)
                time.sleep(60)
        followers = [i.screen_name for i in followers]
        return followers
    
    def get_user_friends(self, user_name):
        friends = []
        for page in tweepy.Cursor(api.friends, screen_name=user_name, count=200).pages():
            try:
                friends.extend(page)
            except tweepy.TweepError as e:
                print("Going to sleep:", e)
                time.sleep(1)
        friends = [i.screen_name for i in friends]
        return friends
    
    def user_favorites_list(self, screen_name):
        favs = []
        for page in tweepy.Cursor(api.favorites, id=screen_name, count=200).pages():
            favs.append([tweet.id for tweet in page])
        return [item for elem in favs for item in elem]
    
    def twitter_rates(self):
        stats = api.rate_limit_status()  #stats['resources'].keys()
        for akey in stats['resources'].keys():
            if type(stats['resources'][akey]) == dict:
                for anotherkey in stats['resources'][akey].keys():
                    if type(stats['resources'][akey][anotherkey]) == dict:
                        #print(akey, anotherkey, stats['resources'][akey][anotherkey])
                        limit = (stats['resources'][akey][anotherkey]['limit'])
                        remaining = (stats['resources'][akey][anotherkey]['remaining'])
                        used = limit - remaining
                        if used != 0:
                            print("Twitter API used", used, "remaining queries", remaining,"for query type", anotherkey)
                        else:
                            pass
                    else:
                        pass  #print("Passing")  #stats['resources'][akey]
            else:
                print(akey, stats['resources'][akey])
                print(stats['resources'][akey].keys())
                limit = (stats['resources'][akey]['limit'])
                remaining = (stats['resources'][akey]['remaining'])
                used = limit - remaining
                if used != 0:
                    print("Twitter API:", used, "requests used,", remaining, "remaining, for API queries to", akey)
                    pass
                
    def capture_user_data(self, user, user_friends, user_followers, friends, followers):
        l = []
        try:
            l.append(user.screen_name)
            l.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            l.append(user.description)
            l.append(len([friend for friend in friends if friend in user_friends]))
            l.append(len([follower for follower in followers if follower in user_followers]))
            l.append(len([user for user in followers if user in user_friends]))
            l.append(user.friends_count)
            l.append(user.followers_count)
            l.append(user.verified)
            l.append(user.created_at.strftime("%Y-%m-%d %H:%M:%S"))
            l.append(user.favourites_count)
            l.append(user.statuses_count)
            l.append(user.location)
            l.append(0)
            return l
        except Exception as e: print(e)
        
    def user_add_count_contraints(self, user, less_followers_than, less_friends_than):
        if (user.followers_count < less_followers_than) and (user.friends_count < less_friends_than) and (user.followers_count < user.friends_count):
            return True
        else:
            return False
        
    def time_constraints(self, time_capture, alarm1, alarm2):
        if (datetime.now().time() != alarm1) and (datetime.now().time() != alarm2):
            if (alarm1 < datetime.now().time()) and (alarm1 > time_capture):
                return False
            elif (alarm2 < datetime.now().time()) and (alarm2 > time_capture):
                return False
            else:
                return True
        else:
            return False
        
class GspreadInfo():
    
    tweets_sheet = client.open("Twitter Bot").get_worksheet(worksheet['Tweets'])
    friends_added_sheet = client.open("Twitter Bot").get_worksheet(worksheet['Friends Added'])
    followers_sheet = client.open("Twitter Bot").get_worksheet(worksheet['Followers'])
    friends_sheet = client.open("Twitter Bot").get_worksheet(worksheet['Friends'])
    unfollowed_me_sheet = client.open("Twitter Bot").get_worksheet(worksheet['Unfollowed Me'])
    new_followers_sheet = client.open("Twitter Bot").get_worksheet(worksheet['New Followers'])
    deleted_sheet = client.open("Twitter Bot").get_worksheet(worksheet['Deleted'])
    
    def next_available_row(self, sheet, cols_to_sample=2):
        # looks for empty row based on values appearing in 1st N columns
        cols = sheet.range(1, 1, sheet.row_count, cols_to_sample)
        return max([cell.row for cell in cols if cell.value]) + 1
    
   