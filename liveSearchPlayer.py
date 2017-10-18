from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time

#consumer key, consumer secret, access token, access secret.
ckey="fj8ZqiPyByadr2iUzQLBb855K"
csecret="BwsiA5C9trFbUG1jqU6mgrrPJIpaiHRDj9b8ETKue1kwVwnA16"
atoken="454930493-ETEUqZrzGS97f9TTi7UlcsL4zleLIyjS3gV5EeNM"
asecret="GIeOI05vYDL5CI0pNMBCiwvI7X6qcH4f1akkJjftmNVZY"

file=open('data/livePlayer.csv','w').close()
file=open('data/pl_sen','w').close()
class listener(StreamListener):
    def __init__(self):
        self.running = True
    def on_data(self, data):
        global count, lastcount
        #*****can use count or time ******

        if count == lastcount:
            lastcount = count+10
            # time.sleep(30)
            self.running =False

            return False
            print('30 seconds rest')
            if(count==50):
                return False
            # return False
        # global t1
        # if time.time() > t1 + 50:
        #     return False # this is important to exit loop
            
        tweet=data.split(',"text":"')[1].split('","source')[0]
        print(tweet)
        file=open('data/livePlayer.csv','a')
        file.write(tweet+'\n')
        file.close()
  
        count+=1

        return(True)

    def on_error(self, status):
        print(status)

    
count = 0
lastcount= count +10
class liveApi(object):

    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    t1 = time.time()
    twitterStream = Stream(auth, listener())
    #print(twitterStream)
    twitterStream.filter(languages=['en'],track=["minions"])
    print(twitterStream.running)

    # if(!twitterStream.running):
    #     print('disconnection')
    #     self.disconnect()


    def disconnect(self):
        twitterStream.disconnect() # Don't think this matters.....
        print('this is a string')

if __name__== '__main__':
    liveApi() 