import time
import tweepy
import pprint
import pymongo
from pymongo import MongoClient

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
mydb = myclient["lunch4dinner_tweeps"]
mycol = mydb["usernames"]
noDMs = mydb["DM's Blocked"]
myfollowers = mydb["My Followers"]


##############Actual "Do Stuff" part of the code starts here

#Just lets user know the program is running
print("Lez get it...")

#Searches twitter for tweets containing the words input here, couple extra parameters on how it should return the results
#public_tweets = api.search('fuckery, -rt', lang="en",
#                          count=10000, tweet_mode="extended", result_type="recent",)
current_usernames = []
for x in mycol.find():
    current_usernames.append(x["username"])

    #builds a locl list of people that dont accept DM's compiled from external database
no_DMs = []
for x in noDMs.find():
    no_DMs.append(x["username"])


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, tweet):

        #loops through the tweets we searched, variable created for usernames

        tweeter_name = tweet.user.screen_name
        print("")
        print("------------------------------------------------------")
        print(tweet.text)
        print(tweeter_name)
        print("")
        print("")
        tweeter_name = tweet.user.screen_name
        if tweeter_name in no_DMs:
            print("We don't fux with " + tweeter_name)

        #if we have tried them before, it gives this notification has been favorited more than the below defined amount of times, we retweet it

        else:
            if tweeter_name in current_usernames:
                print("match found")

                #If we havent tried them before, we start trying this stuff
            else:
                #try sending this DM
                try:
                    api.send_direct_message(
                        tweet.user.id, "Follow me for awesome vegan recipes!!")
                    #If they won't accept DM's, we put them on the NO DM's list in the external database

                    #if DM does go through, we add them to the external database of people we have reached and also how many followers they have
                except tweepy.TweepError as e:
                    print(e)

                #except:

                    current_usernames.append(tweet.user.screen_name)
                    blockedDM = {"username": tweet.user.screen_name,
                                 "followers": tweet.user.followers_count}
                    noDMs.insert_one(blockedDM)
                    print("We dont fux wit " + tweet.user.screen_name)

                else:
                    current_usernames.append(tweet.user.screen_name)
                    print(tweeter_name +
                          " has been added to the usernames list!!!")
                    mydict = {"username": tweet.user.screen_name,
                              "followers": tweet.user.followers_count}
                    mycol.insert_one(mydict)

                    #here we try to favorite their tweet
                    try:
                        api.create_favorite(tweet.id)
                        #if it doesnt work, error notification
                    except:
                        print("***Could not favorite")
                        #here we try to add them as a friend
                    try:
                        api.create_friendship(tweet.user.id)
                        #error message if it doesn't work
                    except:
                        print("***Could not friend")

                        #if the tweet

                    #this executes the


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

myStream.filter(track=['vegan '], is_async=False)

#############################################################


#Now we start deciding what to do with each tweet

#if the person writing the tweet is already on our no DM's list, it gives us a notification
