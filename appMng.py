import pandas as pd

class TwitterApp:
   appCount = 0
   currentApp = 0
   appSize = 0
   appList = []
   def __init__(self,ck,cs,ak,asc):
      self.ck = ck
      self.cs = cs
      self.ak = ak
      self.asc = asc
    

   def getCk (self):
      #print("ck...")
      return self.ck

   
   def getCs(self):
      return self.cs

   def getAk(self):
      return self.ak

   def getAsc(self):
      return self.asc 

   def getTup(self):
      return (self.ck,self.cs,self.ak,self.asc)   

   def __str__(self):
      return ",".join([self.ck,self.cs,self.ak,self.asc]) 

def appMng(i):
      app = TwitterApp.appList
#      print("app = ",app)
      return (app[i-1].getCk(),app[i-1].getCs(),app[i-1].getAk(),app[i-1].getAsc())

def rotateApp():

      if TwitterApp.currentApp < TwitterApp.appSize:
         TwitterApp.currentApp+=1
      else:
         TwitterApp.currentApp = 1
      cApp = appMng(TwitterApp.currentApp)
      return cApp

def init():
    appList = pd.read_csv("appList.csv")
    appFile = pd.read_csv("appList.csv").values.tolist()
    for e in appFile:
        TwitterApp.appList.append(TwitterApp(e[0], e[1], e[2], e[3]))
    TwitterApp.appSize = appList.shape[0]

# print(rotateApp())
# print(rotateApp())
# print(rotateApp())