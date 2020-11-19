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
api = tweepy.API(auth)

#These variables to the same, make it more readable
mydb = myclient["mongotweeps"]
mycol = mydb["usernames"]
noDMs = mydb["DM's Blocked"]
myfollowers = mydb["My Followers"]

##############Actual "Do Stuff" part of the code starts here

#Just lets user know the program is running
print("Lez get it...")

#Searches twitter for tweets containing the words input here, couple extra parameters on how it should return the results
public_tweets = api.search('fuckery, -rt', lang="en",
                           count=10000, tweet_mode="extended", result_type="recent",)

#def is defining a function, starting with its name.  This function will be called later in the program


def usermatch():
    print("")
    print("Executing.............")

    #build a local list of all the people I have reached out to before compiled from from external database
    current_usernames = []
    for x in mycol.find():
        current_usernames.append(x["username"])

    #builds a locl list of people that dont accept DM's compiled from external database
    no_DMs = []
    for x in noDMs.find():
        no_DMs.append(x["username"])

    #loops through the tweets we searched, variable created for usernames
    for tweet in public_tweets:
        tweeter_name = tweet.user.screen_name

        #Now we start deciding what to do with each tweet
        def add_attempt_1():

            #if the person writing the tweet is already on our no DM's list, it gives us a notification
            if tweeter_name in no_DMs:
                print("We don't fux with " + tweeter_name)

            #if we have tried them before, it gives this notification
            else:
                if tweeter_name in current_usernames:
                    print("match found")

                #If we havent tried them before, we start trying this stuff
                else:
                    #try sending this DM
                    try:
                        api.send_direct_message(
                            tweet.user.id, "Help Fight the Fuckery!  Wanted to see if I can get a follow back?")
                    #If they won't accept DM's, we put them on the NO DM's list in the external database
                    except:
                        blockedDM = {"username": tweet.user.screen_name,
                                     "followers": tweet.user.followers_count}
                        noDMs.insert_one(blockedDM)
                        print("We dont fux wit " + tweet.user.screen_name)
                    #if DM does go through, we add them to the external database of people we have reached and also how many followers they have
                    else:
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

                #if the tweet has been favorited more than the below defined amount of times, we retweet it
                if tweet.favorite_count >= 100:
                    try:
                        api.retweet(tweet.id)
                    #if it doesnt work
                    except:
                        print("***Could Not Retweet")

        #this executes the add_attempt_1 function that we defined above
        add_attempt_1()


#texecutes usermatch function defined above which contains add_attempt functionand then run again every 15 minutes as long as the if condition is true
while 5 < 10:
    usermatch()
    print("***********************************finished loop***********************************")
    time.sleep(1000)
    
    #SYNC CHECK
