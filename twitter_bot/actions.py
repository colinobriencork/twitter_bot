#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 11:57:09 2020

@author: Colin
"""

#need to resize the friends added sheet and deleted sheet

from datetime import datetime, timedelta
from gspread_dataframe import set_with_dataframe
import tweepy, time, requests, os, pandas as pd, numpy as np

def delete_perished_users(tweepyinfo, sheet):
    screen_names = sheet.range("A2:A{}".format(sheet.row_count))
    screen_names = [user.value for user in screen_names if user.value != '']
    time.sleep(1)
    for user in screen_names:
        while True:
            try:
                tweepyinfo.api.get_user(user)
                break
            except Exception as e:
                if str(e).find('User not found.') != -1:
                    print(user)
                    sheet.delete_rows(sheet.find(user).row)
                    time.sleep(1)
                    break
                time.sleep(1)

def follow_query_users(tweepyinfo,
                       gspreadinfo,
                       query_count,
                       query_max,
                       less_followers_than, 
                       less_friends_than, 
                       add_deleted_users_since,
                       alarm1,
                       alarm2):
    
    my_friends = tweepyinfo.get_user_friends(user_name="_data_engineer")
    my_followers = tweepyinfo.get_user_followers(user_name="_data_engineer")
    query_words = pd.read_csv('./twitter_bot/KeywordList.csv')['Query']
    query_max = len(query_words)
    
    dataframe = pd.DataFrame(gspreadinfo.deleted_sheet.get_all_records())
    good_to_add = dataframe.loc[pd.to_datetime(dataframe['Deleted Date']) < datetime.now()-timedelta(days=add_deleted_users_since)]['Screen Name'].values.tolist()
    not_good_to_add = dataframe.loc[pd.to_datetime(dataframe['Deleted Date']) >= datetime.now()-timedelta(days=add_deleted_users_since)]['Screen Name'].values.tolist()
    del dataframe
    print('got here')
    
    time_capture = datetime.now().time()
    
    while tweepyinfo.time_constraints(time_capture=time_capture, alarm1=alarm1, alarm2=alarm2):
        if query_count == query_max:
            query_count = 0    
        for page in tweepy.Cursor(tweepyinfo.api.search_users, q=query_words.loc[query_count]).pages(51):
            if tweepyinfo.time_constraints(time_capture=time_capture, alarm1=alarm1, alarm2=alarm2) == False:
                break            
            for user in page:
                if tweepyinfo.time_constraints(time_capture=time_capture, alarm1=alarm1, alarm2=alarm2) == False:
                    break
                time_capture = datetime.now().time()                
                if user.screen_name in my_friends:
                    pass
                elif user.screen_name in not_good_to_add:
                    pass
                elif user.protected == True:
                    pass
                elif tweepyinfo.user_add_count_contraints(user, less_followers_than, less_friends_than):
                    try:
                        print(user.screen_name)
                        user_friends = tweepyinfo.get_user_friends(user.screen_name)
                        user_followers = tweepyinfo.get_user_followers(user.screen_name)
                        user_data = tweepyinfo.capture_user_data(user, user_friends, user_followers, my_friends, my_followers)
    
                        tweepyinfo.api.create_friendship(user.screen_name)
                        index = gspreadinfo.next_available_row(gspreadinfo.friends_added_sheet)
                        time.sleep(1)
                        print('got here1')
                        try:
                            gspreadinfo.friends_added_sheet.insert_row(user_data, index)
                            if user.screen_name in good_to_add:
                                gspreadinfo.deleted_sheet.delete_rows(gspreadinfo.deleted_sheet.find(user.screen_name).row)
                                time.sleep(1)
                                print('got here3')
                            print(f"{user.screen_name}")
                            my_friends.append(user.screen_name)
                        except Exception as e: print(e) 
                        time.sleep(1)
                        print('got here2')
                        tweepyinfo.twitter_rates()
                        time.sleep(900)
                    except Exception as e: print(e)
                else:
                    pass
        query_count += 1
    return query_count, query_max

def friend_followers(tweepyinfo):
    
    for follower in tweepy.Cursor(tweepyinfo.api.followers, count=200).items():
        if not follower.following:
            try:
                follower.follow()
                print(f"{follower.screen_name}")
            except Exception as e: print(e)
        else:
            pass
        
def like_tweets(tweepyinfo, gspreadinfo, max_tweet_likes = 3):

    time.sleep(2)
    likes_num_column = gspreadinfo.friends_added_sheet.range("N2:N{}".format(gspreadinfo.friends_added_sheet.row_count))
    potential_like_list = [i for i in likes_num_column if i.value != '' and int(i.value) < max_tweet_likes]
    my_favs = tweepyinfo.user_favorites_list("_data_engineer")

    for cell in potential_like_list:
        screen_name = gspreadinfo.friends_added_sheet.acell('A' + str(cell.row)).value
        #check if the user still exists, if not pass
        try:
            user = tweepyinfo.api.get_user(screen_name)
            if user.protected == True:
                pass
            else:
                time.sleep(1)
                tweets = tweepyinfo.api.user_timeline(screen_name = screen_name, count = 100, include_rts = False)
                list_of_potential_favs = [i.id for i in tweets if i.id not in my_favs]
                
                #if there is nothing in the list
                if not list_of_potential_favs:
                    pass
                else:
                    like_count = int(cell.value)
                    #np.random.randint(4) needs to be 4 because it only returns 3
                    loop_range = range(len(list_of_potential_favs)) if len(list_of_potential_favs) < 3 else range(np.random.randint(4))
        
                    for like in loop_range:
                        random_number = np.random.randint(len(list_of_potential_favs))
                        tweepyinfo.api.create_favorite(list_of_potential_favs[random_number])
                        del list_of_potential_favs[random_number]
                        like_count = like_count + 1
                        print(str(like) + ' like count:' + str(like_count) + ' ' + screen_name)
                        if like_count == max_tweet_likes:
                            break
                    gspreadinfo.friends_added_sheet.update_cell(cell.row, cell.col, str(like_count))
                    time.sleep(1)
        except:
            pass


            
def tweet(tweepyinfo, gspreadinfo):
    
    def tweet_image(tweepyinfo, message, url=''):
    
        if url != '':
            filename = 'temp.jpg'
            request = requests.get(url, stream=True)
            if request.status_code == 200:
                with open(filename, 'wb') as image:
                    for chunk in request:
                        image.write(chunk)
    
                tweepyinfo.api.update_with_media(filename, status=message)
                os.remove(filename)
            else:
                print("Unable to download image")
        else:
            tweepyinfo.api.update_status(message)
    time.sleep(2)
    date_published_col = gspreadinfo.tweets_sheet.range("C2:C{}".format(gspreadinfo.tweets_sheet.row_count))
    time.sleep(1)
    potential_tweets = [i for i in date_published_col if i.value == '']
    
    try:
        message = gspreadinfo.tweets_sheet.acell('A' + str(potential_tweets[0].row)).value.replace('\\n','\n')
        time.sleep(1)
        url = gspreadinfo.tweets_sheet.acell('B' + str(potential_tweets[0].row)).value
        time.sleep(1)
        tweet_image(message, url)
        gspreadinfo.tweets_sheet.update_cell(potential_tweets[0].row, potential_tweets[0].col, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        time.sleep(1)
    except:
        print('no tweets')

def delete_old_friends(tweepyinfo, gspreadinfo, how_old = 4):
    
    friends_added = pd.DataFrame(gspreadinfo.friends_added_sheet.get_all_records())
    time.sleep(1)
    
    friends_added_to_delete = friends_added.loc[(pd.to_datetime(friends_added['Date Added']).dt.date <= datetime.now().date()-timedelta(days=how_old)) &
                                                (friends_added['Follow Back'] == '')]
    friends_added_to_delete['Deleted Date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for i in friends_added_to_delete['Screen Name'].values.tolist():
        try:
            tweepyinfo.api.destroy_friendship(i)
            gspreadinfo.friends_added_sheet.delete_rows(gspreadinfo.friends_added_sheet.find(i).row)
            time.sleep(1)
            print(i)
        except Exception as e: print(e)
    
    set_with_dataframe(gspreadinfo.deleted_sheet, friends_added_to_delete, row=gspreadinfo.next_available_row(gspreadinfo.deleted_sheet), include_column_header=False)
    time.sleep(1)

def insert_friend(tweepyinfo, gspreadinfo):
    
    my_friends = tweepyinfo.get_user_friends(user_name="_data_engineer")
    gspreadinfo.friends_sheet.resize(rows=1)
    time.sleep(1)
    friends_df = pd.DataFrame({'Friend': my_friends, 'Date Updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    gspreadinfo.friends_sheet.update([friends_df.columns.values.tolist()] + friends_df.values.tolist())
    time.sleep(1)

def insert_un_newly_followed(tweepyinfo, gspreadinfo):
    
    old_followers = gspreadinfo.followers_sheet.col_values(1)[1:]
    time.sleep(1)
    new_followers = tweepyinfo.get_user_followers(user_name = "_data_engineer")
    unfollowed = [i for i in old_followers if i not in new_followers]
    newly_followed = [i for i in new_followers if i not in old_followers]
    
    if not unfollowed:
        pass
    else:
        friends_added = pd.DataFrame(gspreadinfo.friends_added_sheet.get_all_records())
        friends_added_unfollowed = friends_added[friends_added['Screen Name'].isin(unfollowed)]
            
        for i in unfollowed:
            if friends_added_unfollowed.empty:
                pass
            else:
                try:
                    tweepyinfo.api.destroy_friendship(i)
                    gspreadinfo.friends_added_sheet.delete_rows(gspreadinfo.friends_added_sheet.find(i).row)
                    time.sleep(1)
                except:
                    pass
            
            l = [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            l.insert(0, i)
            index = gspreadinfo.next_available_row(gspreadinfo.unfollowed_me_sheet)
            time.sleep(1)
            gspreadinfo.unfollowed_me_sheet.insert_row(l, index)
            time.sleep(1)
        
        #add unfollowed users from friends added sheet to deleted sheet
        friends_added_unfollowed['Deleted Date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        set_with_dataframe(gspreadinfo.deleted_sheet, friends_added_unfollowed, row=gspreadinfo.next_available_row(gspreadinfo.deleted_sheet), include_column_header=False)
        time.sleep(1)
        
    if not newly_followed:
        pass
    else:
        for i in newly_followed:
            l = [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            l.insert(0, i)
            index = gspreadinfo.next_available_row(gspreadinfo.new_followers_sheet)
            time.sleep(1)
            gspreadinfo.new_followers_sheet.insert_row(l, index)
            time.sleep(2)
            #add followed back information to 'Friends Added' sheet
            name_column = gspreadinfo.friends_added_sheet.range("A1:A{}".format(gspreadinfo.friends_added_sheet.row_count))
            time.sleep(1)
            cell = [found for found in name_column if found.value == i]
            if not cell:
                pass
            else:
                #list so need to access the element, should always have only 1 element
                cell = cell[0]
                gspreadinfo.friends_added_sheet.update('O' + str(cell.row), True)
                time.sleep(1)
                gspreadinfo.friends_added_sheet.update('P' + str(cell.row), l[1])
                time.sleep(2)
                
            #check if deleted user has followed me back, add to friends sheet and remove from delete sheet            
            name_column = gspreadinfo.deleted_sheet.range("A1:A{}".format(gspreadinfo.deleted_sheet.row_count))
            time.sleep(1)
            cell = [found for found in name_column if found.value == i]
            if not cell:
                pass
            else:
                cell = cell[0]
                #take off Follow Back + Date entries, and add in
                values = gspreadinfo.deleted_sheet.row_values(cell.row)[:-3]
                time.sleep(1)
                values.append(True)
                values.append(l[1])
                
                index = gspreadinfo.next_available_row(gspreadinfo.friends_added_sheet)
                time.sleep(1)
                gspreadinfo.friends_added_sheet.insert_row(values, index)
                time.sleep(1)
                gspreadinfo.deleted_sheet.delete_rows(cell.row)
                time.sleep(1)
     
    #update the followers sheet with the new followers list      
    followers_df = pd.DataFrame({'Follower': new_followers, 'Date Updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    gspreadinfo.followers_sheet.resize(rows=1)
    time.sleep(1)
    gspreadinfo.followers_sheet.update([followers_df.columns.values.tolist()] + followers_df.values.tolist())
    time.sleep(1)