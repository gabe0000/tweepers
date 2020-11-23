#These lines import tools that this program will use

import time
import tweepy
import pprint
import pymongo
from pymongo import MongoClient

#This lets the program know where my database is and my credentials
myclient = 

#These are my twitter credentials
consumer_key = 
consumer_secret = 
access_token = 
access_token_secret = 
usernames = list()

#More Credentials
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#this variable just makes code more readable down the road
##api = tweepy.API(auth)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


#These variables to the same, make it more readable
mydb = myclient["mongotweeps"]
mycol = mydb["usernames"]
noDMs = mydb["DM's Blocked"]
myfollowers = mydb["My Followers"]
##############Actual "Do Stuff" part of the code starts here
current_friends = []
current_followers = []
black_list = []

screen_name = "quantumfuckery"


def get_friends():

    friends = api.friends_ids(screen_name)
    for friend in friends:
        current_friends.append(friend)
        #print(api.get_user(friend).screen_name)
    

def get_followers():

    followers = api.followers_ids(screen_name)
    for follower in followers:
       current_followers.append(follower)
        
def users_to_remove():
    for i in current_friends:
        if i in current_followers:  
            print (i)
            print("followed you back.")
        else: 
            black_list.append(i)
            print (i)
            print("is getting black listed.")
            #api.destroy_friendship(i)
    print("_______________________________________________________")

def fix_errors():

    for x in current_followers:
        if x in current_friends:
            print("All Good")
        else:
            try:
                api.create_friendship(x)
            except:
                print("Add back failed.")

get_friends()
get_followers()
#users_to_remove()
print (len(current_friends))
print (len(current_followers))
print (len(black_list))
fix_errors()
print(len(current_friends))
print(len(current_followers))
print(len(black_list))

#print(current_followers)
#print("You have "+len(current_followers)+" followers")
#print("You have "+ len(current_friends)+ " friends")
