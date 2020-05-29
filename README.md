# twitter_bot

Simple twitter bot to add users, delete added users if they don't follow back, follow back users who follow, like tweets of newly followed users, tweet etc.

**Google:**

Data is populated into a Google sheet. To get this to work you need to create a client_secrets.json file which allows you to connect to Google Sheets / Google Drive API.

https://towardsdatascience.com/accessing-google-spreadsheet-data-using-python-90a5bc214fd2
https://console.developers.google.com/apis/

This client_secrets.json needs to be placed in the app/oauth/tweepy_auth.py, these are:

I've called the worksheet that the data goes into "Twitter Bot". Do the same or change that in app/information.py on line 111 - 117. 

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

Parameters to dictate how the app is to work can be made in two places:

1. app/app.py 
Here you can parameterize the kinds of users that you're searching for and subsequently add. 

  a. less_followers_than
  b. less_friends_than
  
This does as it says on the tin. It looks only for users that have less followers than are shown in the parameter, and less friends (people the user has followed) than is shown in the parameter. There is an **important** caveat here: The number in less_followers_than cannot be greater than the number in less_friends_than. This cannot be changed unless you change the code in app/actions.py. The app, by default, only looks for users who are following more people than follow them, the thinking being that these are the kinds of users who are more likely to follow back.

  c. add_deleted_users_since
  
This defines the length of time (in days) after which it is ok to add users who have previously been added but now sit in the 'Deleted' sheet on Google Sheets having previously been deleted from our friend's list. 

2. app/__main__.py
