#These lines import tools that this program will use

import time
import tweepy
import pprint
import pymongo
from pymongo import MongoClient


#This lets the program know where my database is and my credentials
myclient = pymongo.MongoClient(
    "mongodb+srv://gabe0000:TESSA1@cluster0.gdmvn.mongodb.net")

#These are my twitter credentials
consumer_key = "NvOt8eUG0oVwQjmO4XC2ogRyI"
consumer_secret = "jPmEppKkPgpzmVp4RpPrVO1ibDTL4m7EUncJoMfGEA2Wd2BFO8"
access_token = "1108557129609347073-1YdBjzMiKwPVFs7Qcir8a335EeDdjA"
access_token_secret = "4faJ3y7DLHl9OQWyYot1FNTT5BJGKw0szePygVo5h4uog"
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
    current_usernames = []
    for x in mycol.find():
        current_usernames.append(x["username"])
    
    no_DMs = []
    for x in noDMs.find():
        no_DMs.append(x["username"])

    for tweet in public_tweets:
        tweeter_name = tweet.user.screen_name
        def add_attempt_1():
            
            if tweeter_name in no_DMs:
                print("We don't fux with " + tweeter_name)
            else:

                if tweeter_name in current_usernames:
                    print("match found")
                else:
                    try:
                        api.send_direct_message(
                            tweet.user.id, "Help Fight the Fuckery!  Wanted to see if I can get a follow back?")
                    except:
                        blockedDM = {"username": tweet.user.screen_name,
                                    "followers": tweet.user.followers_count}
                        noDMs.insert_one(blockedDM)
                        print("We dont fux wit " +tweet.user.screen_name)             
                    else:
                        print(tweeter_name+" has been added to the usernames list!!!")
                        mydict = {"username": tweet.user.screen_name,
                                "followers": tweet.user.followers_count}
                        mycol.insert_one(mydict)

                        try:
                            api.create_favorite(tweet.id)
                        except:
                            print("***Could not favorite")
                        try:
                            api.create_friendship(tweet.user.id)
                        except:
                            print("***Could not friend")
                        
                    
                                

                if tweet.favorite_count >= 100:
                    try:
                        api.retweet(tweet.id)
                    except:
                        print("***Could Not Retweet")
        
        
      
        add_attempt_1()
        
            
    #print(current_usernames)



while 5<10:
    usermatch()
    print("***********************************finished loop***********************************")
    time.sleep(1000)
       
