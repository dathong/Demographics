import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import time
import pandas as pd
import os
import json

fol = "./user_info/IA/"

consumer_key = "hKXueOOum1p0o4zwdpTK7aTjH"
consumer_secret = "q3pew4xM3mzLD1JUzlVPS4Y0BFMly9W7PmBO4sh1FdDxG1Hl3S"
access_key = "509412750-auC5IpGBM791qXJM098oW6XixHmbKtb4eemaI3gj"
access_secret = "53YYqDdRNp0mPU8TuapHAsUE6DRe9iNwLW9elDQK5SluM"

CONSUMER_KEY = consumer_key
CONSUMER_SECRET = consumer_secret
ACCESS_KEY = access_key
ACCESS_SECRET = access_secret
auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
api = tweepy.API(auth)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
class TweetListener(StreamListener):
    # A listener handles tweets are the received from the stream.
    #This is a basic listener that just prints received tweets to standard output

    def on_data(self, data):
        print (data)
        return True

    def on_error(self, status):
        print (status)
#search
api = tweepy.API(auth)
twitterStream = Stream(auth,TweetListener())
#test = api.lookup_users(user_ids=['17006157','59145948','157009365','1973722680'])
#userList = []
import os  
#for fn in os.listdir("/home/dthong/TwitterUsers/USERS/IA"):
   #print("fn ",fn)  
#   if ".csv" in fn: 
        #print("fn = ",fn)
#        userList.append(fn.replace(".csv",""))
def getUserInfo(userList):
   fol = "user_profile_json/"

   finishedList = "./user_profile_json/finishedList.csv"

   fnFile = open(finishedList,"a")
   consumer_key = "hKXueOOum1p0o4zwdpTK7aTjH"
   consumer_secret = "q3pew4xM3mzLD1JUzlVPS4Y0BFMly9W7PmBO4sh1FdDxG1Hl3S"
   access_key = "509412750-auC5IpGBM791qXJM098oW6XixHmbKtb4eemaI3gj"
   access_secret = "53YYqDdRNp0mPU8TuapHAsUE6DRe9iNwLW9elDQK5SluM"

   CONSUMER_KEY = consumer_key
   CONSUMER_SECRET = consumer_secret
   ACCESS_KEY = access_key
   ACCESS_SECRET = access_secret
   
   auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
   api = tweepy.API(auth)
   auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
   userCount = len(userList)
   print("len userList: ",str(userCount))
   #test = api.lookup_users(screen_names= userList)
   
   block = 0
   blockSize = 50
   while block < userCount:
      try:
         test = api.lookup_users(screen_names= userList[block:(block+10)])
         for i,user in enumerate(test):
         #print("user: ",user.screen_name)
          with open(fol + user.screen_name  + ".csv","w") as f:
       
          #  l = [str(user.screen_name),str(user.name),str(user.location),str(user.description),str(user.followers_count),str(user.statuses_count),str(user.url)]
            print("writing for user ",user.screen_name)
            #f.write("[DHXXX]".join(l).encode('utf-8').strip())
            #userStr = str(user._json).encode('ascii', 'ignore').decode('ascii')
            #f.write(userStr + "\n")
            json.dump(user._json, f)
            block+=1
      
            print("block, i = ",block,i)
          fnFile.write(user.screen_name + ".csv \n")
     #block+=i
      except Exception as e:
         print("e,block i = ",e)
         if 'Not authorized' in str(e):
             print("returning... bkup user ",user_name)
             fnFile.write(user_name + ".csv \n")
             continue
         time.sleep(60)

print("started...")
userList = []
finishedList = pd.read_csv("./user_profile_json/finishedList.csv",header=None).values.tolist() 
finishedList = [x[0] for x in finishedList]
print("finished List: ",finishedList[:10],len(finishedList))
dfUserList = pd.read_csv("Unique.csv",header=None)
userlist = dfUserList[0].values.tolist()
print("user List = ",userlist[:10])
for u in userlist:
   if u not in finishedList:
      userList.append(u)
getUserInfo(userList)
print("Done")
  
