import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import time
from appMng import appMng
import pandas as pd
import os

fol = "./user_info_kaggle/"

consumer_key = "i4ReUBPhLUFNlGYfk5wBDZaAl"
consumer_secret = "YGe1TfIlBeo3DSKZ6cKzX5hD8Pkw3Pdgfv1OYKhSP2Z4fbZVyS"
access_key = "1973722680-GJon8YENN4i8FLOYxypXaMASlUfriceRZKXGj0r"
access_secret = "H5xnyIJ410E4qRjfIuS0fJYIxIbZ40aQJaRPAkh6UlPou"

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
   #fol = "user_profile/"
   fol = "./user_info_kaggle/"
   finishedList = fol + "finishedList.csv"
   
   fnFile = open(finishedList,"a")
   (CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET) = appMng(2)
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
         print("trying on userList: ",block,userList[block:(block+10)])		  
         test = api.lookup_users(user_ids= userList[block:(block+10)])
         for i,user in enumerate(test):
         #print("user: ",user.screen_name)
          with open(fol + str(user.id)  + ".csv","w") as f:
       
          #  l = [str(user.screen_name),str(user.name),str(user.location),str(user.description),str(user.followers_count),str(user.statuses_count),str(user.url)]
            print("writing for user ",str(user.id)) 
            #f.write("[DHXXX]".join(l).encode('utf-8').strip())
            #print("user = ",str(user)[:100])
            userStr = str(user).encode('ascii', 'ignore').decode('ascii')
            print("userStr = ",userStr[:100])
            f.write(userStr + "\n")
            block+=1
     
            print("block, i = ",block,i)
          fnFile.write(str(user.id) + ".csv \n")
     #block+=i
      except Exception as e:
         print("e = ",e)
         if 'Not authorized' in str(e) or 'No user matches for specified terms' in str(e):
             print("error sth like: ",e)
         #    fnFile.write(user_name + ".csv \n")
             block+=1
             continue
         time.sleep(60)

print("started...")
userList = []
finishedList = pd.read_csv(fol + "finishedList.csv",header=None).values.tolist() 
finishedList = [x[0].replace(".csv","") for x in finishedList]
print("finished List: ",finishedList[:10],len(finishedList))
dfUserList = pd.read_csv("kaggle_data/gender-classifier-DFE-791531.csv",encoding="latin_1")
userlist = dfUserList['_unit_id'].values.tolist()
userlist = [str(x) for x in userlist]
print("user List = ",userlist[:10])
#print("finishedList = ",finishedList[:10])
for u in userlist:
   if u not in finishedList:
      userList.append(u)
print("userList = ",userList[:10])
getUserInfo(userList)
print("Done")
  
