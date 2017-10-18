from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time, os
from PyQt4 import QtCore
# from Sentiment_analysis import Sentiment
#consumer key, consumer secret, access token, access secret.
ckey="fj8ZqiPyByadr2iUzQLBb855K"
csecret="BwsiA5C9trFbUG1jqU6mgrrPJIpaiHRDj9b8ETKue1kwVwnA16"
atoken="454930493-ETEUqZrzGS97f9TTi7UlcsL4zleLIyjS3gV5EeNM"
asecret="GIeOI05vYDL5CI0pNMBCiwvI7X6qcH4f1akkJjftmNVZY"

file=open('data/livePlayer.csv','w').close()
file=open('data/bar','w').close()
count = 0
nextcount= count + 2

class listener(StreamListener):
    def __init__(self, sentiment):
        self.running = True
        self.rest = False
        self.sentiment = sentiment
        self.time = time.time()
        self.timeOut = False
        self.limit = 60
        print('Live started')
 

    def on_data(self, data):
        global count, nextcount
        print('on_data entered')
        #*****can use count or time ******
        while(time.time() - self.time) < self.limit:
            print('while loop entered!')
            if self.running == False:
                print('exiting now!!!')
                self.rest = False
                return False
                break

            if count == nextcount:
                nextcount = count+2
                self.rest = True
                self.running == True
                self.sentiment.f_live_sentiment()
                time.sleep(1)

            tweet=data.split(',"text":"')[1].split('","source')[0]
            print(tweet)
            file=open('data/livePlayer.csv','a')
            file.write(tweet+'\n')
            file.close()
      
            count+=1
            
            return(True)
        print('Timeout!! Not recieving Tweets')
        self.timeOut = True
        return False

    def on_error(self, status):
        print(status)

    def on_timeout(self):
        print('timeOut')
        self.running = False
        self.rest = False
        return False

    
class liveApi(object):
    def __init__(self, sentiment):
        self.auth = OAuthHandler(ckey, csecret)
        self.auth.set_access_token(atoken, asecret)
        # t1 = time.time()
        self.sentiment= sentiment
        self.listen= listener(self.sentiment)
    
    def runStream(self,text):
        self.text = text
        self.listen.running = True
        print('Running from runstream')
        
        # Clears the contents of the files before running a new Search
        file=open('data/livePlayer.csv','w').close()
        file=open('data/bar','w').close()
        self.twitterStream = Stream(self.auth, self.listen)#, timeout=30)
        self.twitterStream.filter(languages=['en'],track=[self.text])

    def stopStream(self):
        print('stoping now')
        self.listen.running = False

    def getTimeOut(self):
        timeOut = self.listen.timeOut
        return timeOut 
        
if __name__== '__main__':
    from Sentiment_analysis import Sentiment

    sentiment = Sentiment()
    t1 = time.time()
    live = liveApi(sentiment)
    live.runStream('kejriwal')
    
    
