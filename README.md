# twitter_bot

Simple twitter bot to add users, delete added users if they don't follow back, follow back users who follow back, like tweets of newly followed users, tweet etc.

**Google:**

Data is populated into a Google sheet. To get this to work you need to create a client_secrets.json file which allows you to connect to Google Sheets / Google Drive API.

https://towardsdatascience.com/accessing-google-spreadsheet-data-using-python-90a5bc214fd2
https://console.developers.google.com/apis/

This client_secrets.json needs to be placed in the app/oauth/ folder.

I've called the Google worksheet that the data goes into "Twitter Bot". Do the same or change that in app/information.py on line 111 - 117. 

The dictonary of individual tabs in the worksheet which the app uses is in app/worksheet_dict.py

**Twitter:**

To access Twitter's API you need to register as a developer and fill out a form indicating what you intend to use the access for. Once you are ready to do this you can apply here: https://developer.twitter.com/en/apply-for-access

Having gotten access you need to enter 4 environment variables on your machine. The app looks for these in app/oauth/tweepy_auth.py when authenticating:

1. TWEEPY_CONSUMER_KEY
2. TWEEPY_CONSUMER_SECRET
3. TWEEPY_ACCESS_TOKEN
4. TWEEPY_ACCESS_TOKEN_SECRET

More information can be found here: https://realpython.com/twitter-bot-python-tweepy/#the-follow-followers-bot

**General:**

Parameters to dictate how the app is to work can be made in two modules:

1. app/app.py 

a. less_followers_than
  
b. less_friends_than
  
This does as it says on the tin. It looks only for users that have less followers than are shown in the parameter, and less friends (people the user has followed) than is shown in the parameter. There is an **important** caveat here: The number in less_followers_than cannot be greater than the number in less_friends_than. This cannot be changed unless you change the code in app/actions.py. The app, by default, only looks for users who are following more people than follow them, the thinking being that these are the kinds of users who are more likely to follow back.

c. add_deleted_users_since
  
This defines the length of time (in days) after which it is ok to add users who have previously been added but now sit in the 'Deleted' tab on Google worksheet having previously been unadded and removed from our friend's list. 

2. app/\__main__.py

a. alarm1
  
b. alarm2
  
These two variables, which are set and the top of the module and used in the function below, define the two times where the app breaks from it's regular routine (of searching for and adding users) to do basically everything else. The regular routine is to search for users and add them every 15 minutes (this constraint is made by how often the twitter api can be hit).
  
c. query_dict
  
The last thing to enter is a list of query search terms which will help the app to narrow down it's search for users. The app cycles to the next term down the list after each alarm (alarm1, alarm2), reseting when the end of the list has been reached.
