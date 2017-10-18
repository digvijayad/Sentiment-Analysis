#try1
#stop words
from nltk.tokenize import word_tokenize , sent_tokenize 
from nltk.corpus import stopwords, wordnet
from nltk.tag import pos_tag as pos
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB,BernoulliNB
from sklearn.linear_model import LogisticRegression,SGDClassifier
from sklearn.svm import SVC,LinearSVC,NuSVC
from nltk import NaiveBayesClassifier
from nltk.classify.maxent import MaxentClassifier
from nltk.classify import ClassifierI,accuracy
from statistics import mode
import pickle, numpy, pymysql, random
import re
from csv import reader as csvreader
from voteclassifier import voteClassifier
import threading
import time
lemmatizer = WordNetLemmatizer()

class Sentiment(object):
    def __init__(self):
        training_set, self.training_featured_words, testing_set, = self.f_createData()
        self.f_callClassifiers(training_set, testing_set)


    def main(self):
        self.f_roger_sentiment(self.training_featured_words)
        self.f_novak_sentiment(self.training_featured_words)
        self.f_serena_sentiment(self.training_featured_words)
        self.f_gar_sentiment(self.training_featured_words)
        # self.f_live_sentiment()

    #=================================================================
    #=====================Get the wordnet POS tag=====================
    def f_get_wordnet_pos(self,treebank_tag):
        
        if treebank_tag.startswith('J'):
            return wordnet.ADJ #'a'
        elif treebank_tag.startswith('V'):
            return wordnet.VERB #'V'
        elif treebank_tag.startswith('R'):
            return wordnet.ADV #'r'
        else:
            return wordnet.NOUN #'n' #as NOUN is default
    #=================================================================
    #=================================================================    
    #=================================================================
    #=====================Processes initial tweets====================

    def f_process_tweets(self,tweets):
        
        #***initial declarations
        
        stop_words  = self.f_stop_words()
        processed_tweets=[]
#        tweets = tweets.lower()
        
        for tweet in tweets:
##            print(tweet)
            #process tweet
            re.LOCALE
            #covert to lower case
            tweet = tweet.lower()
            #Convert https?://* to URL
            tweet = re.sub('(http:[^\s]+)', 'URL', tweet)
            tweet = re.sub('(https:[^\s]+)', 'URL', tweet)
            #Convert @username to AT_USER
            tweet = re.sub('@([^\s]+)',' ',tweet)
            #Remove additional white spaces
            tweet = re.sub('[\s]+', ' ', tweet)
            #Replace #word with word
            tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
            #trim
        ##    tweet = tweet.strip('\'"')

        #************Remove stop words and punctuation**************
            words = word_tokenize(tweet)
    ##            words = words.lower()
            punc_tweet=[]
            for word in words:
    ##            print(word)
                #strip punctuation
                word.strip(':"?,.\'')
                val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", word)
                #ignore if it is a stop word
                if word in stop_words or val is None:
                    continue
                else:
                    punc_tweet.append(word)
                    

    #****************parts of speech tags**********************
            tagged_tweet = pos(punc_tweet)
    ##        print(tagged_tweet)
    #********************Lemmatizer***************************
            lemmatizer_words=[]
            for pos_tags in tagged_tweet:
                lemmatizer_words.append(lemmatizer.lemmatize(pos_tags[0],self.f_get_wordnet_pos(pos_tags[1])))
            #saving lemmatizer_words for everytweet in processed_tweets
            processed_tweets.append(lemmatizer_words)   
                
        #print(processed_tweets)
        return processed_tweets
    #=================================================================
    #=================================================================
    #=================================================================
    #===================For removal of stop words=====================
    #requires word tokens
    def f_stop_words(self):#(word_tokens):
        filtered_words=[]
        self.stop_words = set(stopwords.words("english"))
        
    ##    print (stop_words)
        self.stop_words.add('AT_USER')
        self.stop_words.add('roger')
        self.stop_words.add('federer')
        self.stop_words.add('novak')
        self.stop_words.add('djokovic')
        self.stop_words.add('murray')
        self.stop_words.add('serena')
        self.stop_words.add('williams')
        self.stop_words.add('garbine')
        self.stop_words.add('muguruza')
        self.stop_words.add('garbi')
        self.stop_words.add('URL')
        self.stop_words.add('rt')
        self.stop_words.add('wimbledon')
        return self.stop_words
    #=================================================================
    #=================================================================
    #=================================================================
    #========================Training Data============================
    def f_training_data(self):
        training_data=[]
        sentiment= []
        tweets = []
        
    #!!!!!!!!!!!!!!!!!!Better way to use CSV file!!!!!!!!!!!!!!!!!

    #    x,y = numpy.loadtxt('training_2.txt', delimiter=',', unpack=True)

    #********************Gets the total number of rows***************
        #using csv.reader() as csvreader
        check_length = csvreader(open('data/training_tennis.csv', encoding='latin-1'))
        length = sum(1 for row in check_length)#-500
        print(length)
    #********************Saves the Tweets and sentiment**************
        raw_data = csvreader(open('data/training_tennis.csv', encoding='latin-1'), delimiter =",")
        count = 0
        for row in raw_data:
            if count == 900:
                break
            tweets.append(row[1])
            sentiment.append(row[0])
            count+=1

##        print(self.tweets)   
        processed_tweets = self.f_process_tweets(tweets)
##        print(self.trprocessed_tweets)
##        print(len(self.trprocessed_tweets), len(self.trsentiment))
        
        for i in range(len(processed_tweets)):
            
            #to convert it in [([words],positive),([words],positive)] format
            temp=(processed_tweets[i], sentiment[i])
            
            #to convert it in [[[words],positive],[[words],positive]] format
    ##        temp=[]
    ##        temp.append(self.trprocessed_tweets[i])
    ##        temp.append(self.trsentiment[i])
            training_data.append(temp)
##        print(self.training_data)
        random.shuffle(training_data)
        return training_data
    #=================================================================
    #================================================================= 
    #=================================================================
    #========================Testing Data=============================
    def f_testing_data(self):
        testing_data=[]
        sentiment= []
        tweets = []

    #********************Gets the total number of rows***************
        #using csv.reader() as csvreader
        check_length = csvreader(open('data/training_tennis.csv', encoding='latin-1'))
        length = sum(1 for row in check_length)-900
        print(length)
    #********************Saves the Tweets and sentiment**************
        raw_data = csvreader(open('data/training_tennis.csv', encoding='latin-1'), delimiter =",")
        count = 0
        for row in raw_data:
           if raw_data.line_num > length:
##               print(raw_data.line_num)
               if count == 71:
                   break
               tweets.append(row[1])
               sentiment.append(row[0])
               count+=1
##        print(self.tetweets)    
        processed_tweets = self.f_process_tweets(tweets)
##        print(self.teprocessed_tweets)
    ##    print(len(self.teprocessed_tweets), len(self.tesentiment))
        
        for i in range(len(processed_tweets)):
            
            #to convert it in [([words],positive),([words],positive)] format
            temp=(processed_tweets[i], sentiment[i])
            
            #to convert it in [[[words],positive],[[words],positive]] format
    ##        temp=[]
    ##        temp.append(self.teprocessed_tweets[i])
    ##        temp.append(self.tesentiment[i])
            testing_data.append(temp)
##        print(self.testing_data)
        random.shuffle(testing_data)
        return testing_data
    #=================================================================
    #=================================================================
    #=================================================================
    #==============Returns just words from specific==============
    def f_specific_all_words(self,training_data):
        self.all_words=[]
        for data in training_data:
            for words in data:#[0]: #Just the words not sentiment
                self.all_words.append(words)
        return(self.all_words)
    #=================================================================
    #==============Returns just words from training_data==============
    def f_all_words(self,training_data):
        self.all_words=[]
        for data in training_data:
            for words in data[0]: #Just the words not sentiment
                self.all_words.append(words)
        return(self.all_words)
    #=================================================================
    #=================================================================
    #=================================================================
    #==============Returns just words from training_data============
    def f_feature_word(self,all_words):
        all_words = FreqDist(all_words)
        
        #**********IMPORTANT!!! Remeber to change the number******
        common_words =all_words.most_common(3000)
    ##    print(common_words)#prints word and maximum occurences

        self.featured_words = []
        for word in common_words:
            #just the word not the number of occurences!!
            self.featured_words.append(word[0])

        return self.featured_words

    #=================================================================
    #=================================================================
    #=================================================================
    #==============Finds the featured_word from the data==============
    ###!!!!!!!!IMPORTANT!!!! ASK WHY TO USE THIS
    def f_specific_find_feature(self,training_data, featured_words):

        word = set(training_data)
        feature = {}
        for i in featured_words:
            self.feature[i] = (i in word)
        return feature

    def f_find_feature(self,training_data, featured_words):
    #**** Use either list of words or set of words**********
    ##    word = []
    ##    for words in training_data[0]:
    ##        word.append(words)
        word = set(training_data[0])
        
    ##    print (word)
    ##    word=f_lemmatizer(word) # remember to lemmatize the original to check the equality
        feature = {}
        for i in featured_words:
            feature[i] = (i in word)
        return feature
    #=================================================================
    #=================================================================
    #=================================================================
    #==============Finds the featured_set from the data===============
    def f_feature_set(self,training_data, featured_word):
        self.feature_set = [(self.f_find_feature(i,featured_word),i[1]) for i in training_data]
        return self.feature_set


    #=================================================================
    #=================================================================
    #=================================================================
    #========================Naive bayes Classifier===================
    def f_naivebayes(self,training_set,testing_set):
##        NBClassifier = NaiveBayesClassifier.train(training_set)
    #**********Save Classifier to Pickle******************
##        save_naivebayes = open('data/pickles/naivebayes.pickle','wb')
##        pickle.dump(NBClassifier, save_naivebayes)
##        save_naivebayes.close()

    ##************Open classifier from pickle*********************
        open_naivebayes = open('data/pickles/naivebayes.pickle','rb')
        NBClassifier = pickle.load(open_naivebayes)
        open_naivebayes.close()


        print("Naive Bayes Algo accuracy", (accuracy(NBClassifier, testing_set))*100)
        #classifier.show_most_informative_features(15)
        return NBClassifier
    #=================================================================
    #============Multinomial Naive bayes Classifier===================
    def f_multinomialNB(self,training_set,testing_set):
##        multinomialNBClassifier =SklearnClassifier(MultinomialNB())
##        multinomialNBClassifier.train(training_set)
        
    #**********Save Classifier to Pickle******************
##        save_multinomialNB = open('data/pickles/multinomialNB.pickle','wb')
##        pickle.dump(multinomialNBClassifier, save_multinomialNB)
##        save_multinomialNB.close()

    #************Open classifier from pickle*********************
        open_multinomialNB = open('data/pickles/multinomialNB.pickle','rb')
        multinomialNBClassifier = pickle.load(open_multinomialNB)
        open_multinomialNB.close()

        print("multinomialNB Algo accuracy", (accuracy(multinomialNBClassifier, testing_set))*100)
        return multinomialNBClassifier
    #=================================================================
    #============Bernoulli Naive bayes Classifier===================
    def f_bernoulliNB(self,training_set,testing_set):
##        bernoulliNBClassifier =SklearnClassifier(BernoulliNB())
##        bernoulliNBClassifier.train(training_set)
        
    #**********Save Classifier to Pickle******************
##        save_bernoulliNB = open('data/pickles/bernoulliNB.pickle','wb')
##        pickle.dump(bernoulliNBClassifier, save_bernoulliNB)
##        save_bernoulliNB.close()

    #************Open classifier from pickle*********************
        open_bernoulliNB = open('data/pickles/bernoulliNB.pickle','rb')
        bernoulliNBClassifier = pickle.load(open_bernoulliNB)
        open_bernoulliNB.close()
        
        print("bernoulliNB accuracy", (accuracy(bernoulliNBClassifier, testing_set))*100)
        return bernoulliNBClassifier

    #=================================================================
    #============LogisticRegression Classifier===================
    def f_logisticRegression(self,training_set,testing_set):
##        logisticRegressionClassifier =SklearnClassifier(LogisticRegression())
##        logisticRegressionClassifier.train(training_set)
        
    #**********Save Classifier to Pickle******************
##        save_logisticRegression = open('data/pickles/logisticRegression.pickle','wb')
##        pickle.dump(logisticRegressionClassifier, save_logisticRegression)
##        save_logisticRegression.close()

    #************Open classifier from pickle*********************
        open_logisticRegression = open('data/pickles/logisticRegression.pickle','rb')
        logisticRegressionClassifier = pickle.load(open_logisticRegression)
        open_logisticRegression.close()
        
        print("LogisticRegression Algo accuracy", (accuracy(logisticRegressionClassifier, testing_set))*100)
        return logisticRegressionClassifier


    #=================================================================
    #============SGD Classifier===================
    def f_sGD(self,training_set,testing_set):
##        sGDClassifier =SklearnClassifier(SGDClassifier())
##        sGDClassifier.train(training_set)
##        
##    #**********Save Classifier to Pickle******************
##        save_sGDClassifier = open('data/pickles/sGD.pickle','wb')
##        pickle.dump(sGDClassifier, save_sGDClassifier)
##        save_sGDClassifier.close()

    #************Open classifier from pickle*********************
        open_sGDClassifier = open('data/pickles/sGD.pickle','rb')
        sGDClassifier = pickle.load(open_sGDClassifier)
        open_sGDClassifier.close()
        print("SGD Algo accuracy", (accuracy(sGDClassifier, testing_set))*100)
        return sGDClassifier

    #=================================================================
    #============NuSVC Classifier===================
    def f_nuSVC(self,training_set,testing_set):
##        nuSVCClassifier =SklearnClassifier(NuSVC())
##        nuSVCClassifier.train(training_set)
##        
##    #**********Save Classifier to Pickle******************
##        save_NuSVC = open('data/pickles/nuSVC.pickle','wb')
##        pickle.dump(nuSVCClassifier, save_NuSVC)
##        save_NuSVC.close()

    #************Open classifier from pickle*********************
        open_NuSVC = open('data/pickles/nuSVC.pickle','rb')
        nuSVCClassifier = pickle.load(open_NuSVC)
        open_NuSVC.close()
        
        print("NuSVC Algo accuracy", (accuracy(nuSVCClassifier, testing_set))*100)
        return nuSVCClassifier

    #=================================================================
    #============LinearSVC Classifier===================
    def f_linearSVC(self,training_set,testing_set):
##        linearSVCClassifier =SklearnClassifier(LinearSVC())
##        linearSVCClassifier.train(training_set)
##        
##    #**********Save Classifier to Pickle******************
##        save_linearSVC = open('data/pickles/linearSVC.pickle','wb')
##        pickle.dump(linearSVCClassifier, save_linearSVC)
##        save_linearSVC.close()

    #************Open classifier from pickle*********************
        open_linearSVC= open('data/pickles/linearSVC.pickle','rb')
        linearSVCClassifier = pickle.load(open_linearSVC)
        open_linearSVC.close()
            
        print("LinearSVC Algo accuracy", (accuracy(linearSVCClassifier, testing_set))*100)
        return linearSVCClassifier


    #=================================================================
    #============Max Entropy Classifier===================
    def f_maxEnt(self,training_set,testing_set):
##        MaxEntClassifier = MaxentClassifier.train(training_set, 'GIS', trace=3,encoding=None, labels=None, gaussian_prior_sigma=0, max_iter = 10)
##        
##    #**********Save Classifier to Pickle******************
##        save_maxEnt = open('data/pickles/MaxEnt.pickle','wb')
##        pickle.dump(MaxEntClassifier, save_maxEnt)
##        save_maxEnt.close()

    #************Open classifier from pickle*********************
        open_maxEnt= open('data/pickles/MaxEnt.pickle','rb')
        MaxEntClassifier = pickle.load(open_maxEnt)
        open_maxEnt.close()
            
        print("Max Entropy Algo accuracy", (accuracy(MaxEntClassifier, testing_set))*100)
        return MaxEntClassifier

    def f_createData(self):
    #=================================================================
    #=====================Creating testing and training sets========================
        training_data = self.f_training_data()
##        print(self.training_data)
        ##all_words= f_all_words(training_data)
        training_featured_words = self.f_feature_word(self.f_all_words(training_data))
        ##print(self.training_featured_words)
        #self.featureFile= open('feature_words','w')
        ##for word in self.training_featured_words:
        ##    self.featureFile.write(word+'\n')
        ##self.featureFile.close()
        self.training_set = self.f_feature_set(training_data, training_featured_words)
        testing_data= self.f_testing_data()
        self.testing_set = self.f_feature_set(testing_data, training_featured_words)
##        print(self.testing_set)
        return self.training_set,  training_featured_words, self.testing_set
    
    def f_callClassifiers(self, training_set, testing_set):
        #======================================================================
        #======================Calling Classifiers=============================
        NBClassifier=self.f_naivebayes(training_set,testing_set)
        bernoulliNBClassifier=self.f_bernoulliNB(training_set,testing_set)
        multinomialNBClassifier=self.f_multinomialNB(training_set,testing_set)
        logisticRegressionClassifier=self.f_logisticRegression(training_set,testing_set)
        sGDClassifier=self.f_sGD(training_set,testing_set)
##        nuSVCClassifier=self.f_nuSVC(training_set,testing_set)
        linearSVCClassifier=self.f_linearSVC(training_set,testing_set)
##        self.maxEntClassifier = self.f_maxEnt(training_set,testing_set) #Takes really long

        self.voted_classifier = voteClassifier(linearSVCClassifier,)
                                              # bernoulliNBClassifier,
##                                               multinomialNBClassifier,
##                                               logisticRegressionClassifier,
                                              # sGDClassifier,)
##                                         ,nuSVCClassifier
##                                          NBClassifier)
##        print("voted_classifier accuracy percent:", (accuracy(self.voted_classifier, testing_set))*100)
##        print("Classification:", voted_classifier.f_classify(testing_set[0][0]), "Confidence %:",voted_classifier.f_confidence(testing_set[0][0])*100)
##        print("Classification:", voted_classifier.f_classify(testing_set[1][0]), "Confidence %:",voted_classifier.f_confidence(testing_set[1][0])*100)

    def f_test_sentiment(self):
        self.loop_count = 0
        self.count = 0
        self.pos = 0
        self.neg = 0
        self.neut = 0
        for sentiment in range(len(self.testing_set)):
            self.loop_count +=1
            if self.voted_classifier.f_classify(self.testing_set[sentiment][0]) == self.testing_set[sentiment][1]:
                self.count +=1
            if self.voted_classifier.f_classify(self.testing_set[sentiment][0]) == 'positive':
                self.pos += 1
            elif self.voted_classifier.f_classify(self.testing_set[sentiment][0]) == 'negative':
                self.neg += 1
            elif self.voted_classifier.f_classify(self.testing_set[sentiment][0]) == 'neutral':
                self.neut += 1

        print(self.loop_count,self.count, self.pos, self.neg, self.neut)

    def f_roger_sentiment(self, training_featured_words):
        
        try:
            # Reading roger sentiment from the pickle
            roger = open('data/pickles/rog_sen.pickle', 'rb')
            self.rdata = pickle.load(roger)
            roger.close()

            number=[]
            tweet=[]
            # print(self.rdata)
            
            for line in self.rdata.split("\n"):
                x= line.split()[0]
                number.append(int(x))
            
            self.rtotal = number[0]
            self.rpos = number[1]
            self.rneg = number[2]
            self.rneut = number[3]


        except:
            rtweets=[]
            rsentiment=[]
            roger_data=[]
            #********************Gets the total number of rows***************
            #using csv.reader() as csvreader
            check_length = csvreader(open('data/roger_tweets.csv', encoding='latin-1'))
            length = sum(1 for row in check_length)#-500
            print(length)
        #********************Saves the Tweets and sentiment**************
            file = open('data/roger_tweets.csv').read()
            count = 0
            for r in file.split('\n'):
                # if count == 2000:
                #     break
                rtweets.append(r)
                rsentiment.append('None')
                count+=1
            
    ##        print(self.rtweets)
                
            roger_tweets = self.f_process_tweets(rtweets)
    ##        print(self.roger_tweets)
            for i in range(len(roger_tweets)):
                if roger_tweets[i]:
                    rtemp = (roger_tweets[i], rsentiment[i])
                    roger_data.append(rtemp)
    ##        print(self.roger_data)
                    
##            roger_words = self.f_feature_word(self.f_specific_all_words(roger_tweets))
    ##        print(self.roger_words)
               
            roger_set = self.f_feature_set(roger_data, training_featured_words)
    ##        print(self.roger_set)
            self.rtotal = 0
            self.rpos = 0
            self.rneg = 0
            self.rneut = 0
            for tweets in range(len(roger_set)):
                self.rtotal +=1
                if self.voted_classifier.f_classify(roger_set[tweets][0]) == 'positive':
                    self.rpos += 1
                elif self.voted_classifier.f_classify(roger_set[tweets][0]) == 'negative':
                    self.rneg += 1
                elif self.voted_classifier.f_classify(roger_set[tweets][0]) == 'neutral':
                    self.rneut += 1
            print(self.rtotal, self.rpos, self.rneg, self.rneut)

            self.rdata = """%d total
%d pos
%d neg
%d neut"""%(self.rtotal, self.rpos, self.rneg, self.rneut)
            
            print(self.rdata)
            #Saving sentiment result in pickle
            roger = open('data/pickles/rog_sen.pickle', 'wb')
            pickle.dump(self.rdata, roger)
            roger.close()

            

    def f_novak_sentiment(self,training_featured_words):
        try:
            novak = open('data/pickles/nov_sen.pickle', 'rb')
            self.ndata = pickle.load(novak)
            novak.close()

            number=[]
            tweet=[]
            # print(self.ndata)
            for line in self.ndata.split("\n"):
                x= line.split()[0]
                number.append(int(x))
            
            self.ntotal = number[0]
            self.npos = number[1]
            self.nneg = number[2]
            self.nneut = number[3]

        except:
            ntweets=[]
            nsentiment=[]
            novak_data=[]
            #********************Gets the total number of rows***************
            #using csv.reader() as csvreader
            check_length = csvreader(open('data/novak_tweets.csv', encoding='latin-1'))
            length = sum(1 for row in check_length)#-500
            print(length)
        #********************Saves the Tweets and sentiment**************
            file = open('data/novak_tweets.csv').read()
            count = 0
            for r in file.split('\n'):
                # if count == 2000:
                #     break
                ntweets.append(r)
                nsentiment.append('None')
                count+=1
            
    ##        print(ntweets)
                
            novak_tweets = self.f_process_tweets(ntweets)
    ##        print(novak_tweets)
            for i in range(len(novak_tweets)):
                if novak_tweets[i]: #to remove empty lists
                    temp = (novak_tweets[i], nsentiment[i])
                    novak_data.append(temp)
    ##        print(novak_data)
                    
##            novak_words = self.f_feature_word(self.f_specific_all_words(novak_tweets))
    ##        print(self.novak_words)
               
            novak_set = self.f_feature_set(novak_data, training_featured_words)
    ##        for i in range(10):
    ##            print(novak_set[i])
            self.ntotal = 0
            self.npos = 0
            self.nneg = 0
            self.nneut = 0
            for tweets in range(len(novak_set)):
                self.ntotal +=1
                if self.voted_classifier.f_classify(novak_set[tweets][0]) == 'positive':
                    self.npos += 1
                elif self.voted_classifier.f_classify(novak_set[tweets][0]) == 'negative':
                    self.nneg += 1
                elif self.voted_classifier.f_classify(novak_set[tweets][0]) == 'neutral':
                    self.nneut += 1
            print(self.ntotal, self.npos, self.nneg, self.nneut)

            self.ndata = """%d total
%d pos
%d neg
%d neut"""%(self.ntotal, self.npos, self.nneg, self.nneut)

            print(self.ndata)
            novak = open('data/pickles/nov_sen.pickle','wb')
            pickle.dump(self.ndata, novak)
            novak.close()

    def f_serena_sentiment(self,training_featured_words):
        try:
            serena = open('data/pickles/ser_sen.pickle', 'rb')
            self.sdata = pickle.load(serena)
            serena.close()

            # print(self.sdata)

            number=[]
            tweet=[]
            for line in self.sdata.split("\n"):
                x= line.split()[0]
                number.append(int(x))
            
            self.stotal = number[0]
            self.spos = number[1]
            self.sneg = number[2]
            self.sneut = number[3]

        except:
            stweets=[]
            ssentiment=[]
            serena_data=[]
            #********************Gets the total number of rows***************
            #using csv.reader() as csvreader
            check_length = csvreader(open('data/serena_tweets.csv', encoding='latin-1'))
            length = sum(1 for row in check_length)#-500
            print(length)
        #********************Saves the Tweets and sentiment**************
            file = open('data/serena_tweets.csv').read()
            count = 0
            for r in file.split('\n'):
                # if count == 2000:
                #     break
                stweets.append(r)
                ssentiment.append('None')
                count+=1
            
    ##        print(self.stweets)
                
            serena_tweets = self.f_process_tweets(stweets)
    ##        print(self.serena_tweets)
            for i in range(len(serena_tweets)):
                if serena_tweets[i]:
                    temp = (serena_tweets[i], ssentiment[i])
                    serena_data.append(temp)
    ##        print(self.serena_data)
    ##                
##            serena_words = self.f_feature_word(self.f_specific_all_words(serena_tweets))
    ##        print(self.serena_words)
            
            serena_set = self.f_feature_set(serena_data, training_featured_words)
    ##        for i in range(1):
    ##            print(serena_set[i][0])
            self.stotal = 0
            self.spos = 0
            self.sneg = 0
            self.sneut = 0
            for tweets in range(len(serena_set)):
                self.stotal +=1
                if self.voted_classifier.f_classify(serena_set[tweets][0]) == 'positive':
                    self.spos += 1
                elif self.voted_classifier.f_classify(serena_set[tweets][0]) == 'negative':
                    self.sneg += 1
                elif self.voted_classifier.f_classify(serena_set[tweets][0]) == 'neutral':
                    self.sneut += 1
            print(self.stotal, self.spos, self.sneg, self.sneut)

            self.sdata = """%d total
%d pos
%d neg
%d neut"""%(self.stotal, self.spos, self.sneg, self.sneut)

            # print(self.sdata)

            serena = open('data/pickles/ser_sen.pickle','wb')
            pickle.dump(self.sdata, serena)
            serena.close()


    def f_gar_sentiment(self,training_featured_words):
        try:
            garbi = open('data/pickles/gar_sen.pickle','rb')
            self.gdata = pickle.load(garbi)
            garbi.close()

            # print(self.gdata)

            number=[]
            tweet=[]

            for line in self.gdata.split("\n"):
                x= line.split()[0]
                number.append(int(x))
            
            self.gtotal = number[0]
            self.gpos = number[1]
            self.gneg = number[2]
            self.gneut = number[3]

        except:
            gtweets=[]
            gsentiment=[]
            gar_data=[]
            #********************Gets the total number of rows***************
            #using csv.reader() as csvreader
            check_length = csvreader(open('data/garbi_tweets.csv', encoding='latin-1'))
            length = sum(1 for row in check_length)#-500
            print(length)
        #********************Saves the Tweets and sentiment**************
            file = open('data/garbi_tweets.csv').read()
            count = 0
            for r in file.split('\n'):
                # if count == 2000:
                #     break
                gtweets.append(r)
                gsentiment.append('None')
                count+=1
            
    ##        print(gtweets)
                
            gar_tweets = self.f_process_tweets(gtweets)
    ##        print(gar_tweets)
            for i in range(len(gar_tweets)):
                if gar_tweets[i]:
                    temp = (gar_tweets[i], gsentiment[i])
                    gar_data.append(temp)
    ##        print(gar_data)
                    
##            gar_words = self.f_feature_word(self.f_specific_all_words(gar_tweets))
    ##        print(gar_words)
               
            gar_set = self.f_feature_set(gar_data, training_featured_words)
    ##        print(gar_set)
            self.gtotal = 0
            self.gpos = 0
            self.gneg = 0
            self.gneut = 0
            for tweets in range(len(gar_set)):
                self.gtotal +=1
                if self.voted_classifier.f_classify(gar_set[tweets][0]) == 'positive':
                    self.gpos += 1
                elif self.voted_classifier.f_classify(gar_set[tweets][0]) == 'negative':
                    self.gneg += 1
                elif self.voted_classifier.f_classify(gar_set[tweets][0]) == 'neutral':
                    self.gneut += 1
            print(self.gtotal, self.gpos, self.gneg, self.gneut)

            self.gdata = """%d total
%d pos
%d neg
%d neut"""%(self.gtotal, self.gpos, self.gneg, self.gneut)

            # print(self.gdata)

            garbi = open('data/pickles/gar_sen.pickle', 'wb')
            pickle.dump(self.gdata, garbi)
            garbi.close()

    def f_live_sentiment(self):

        try:
            playerfile = open('data/livePlayer.csv').read()
        except:
            print('Error!!!\nFile Not ready. Try Again')
        # print(playerfile)

        plsentiment = []
        pltweets = []
        playerdata = []

        for line in playerfile.split('\n'):
            pltweets.append(line)
            plsentiment.append('None')

        pltweets = self.f_process_tweets(pltweets)

        for i in range(len(pltweets)):
            if pltweets[i]: #To remove empty lists
                temp = (pltweets[i], plsentiment[i])
                playerdata.append(temp)
        # pl_words = self.f_feature_word(self.f_specific_all_words(pltweets))
        pl_set  = self.f_feature_set(playerdata, self.training_featured_words)
           
        self.plneut =0
        self.plpos =0
        self.plneg =0
       
        self.pltotal = 0
        player = open('data/bar','a')
        for tweets in range(len(pl_set)):
            

            self.pltotal +=1
            if self.voted_classifier.f_classify(pl_set[tweets][0]) == 'positive':
                self.plpos += 1
##                player.write('pos\n')
            elif self.voted_classifier.f_classify(pl_set[tweets][0]) == 'negative':
                self.plneg += 1
##                player.write('neg\n')
            elif self.voted_classifier.f_classify(pl_set[tweets][0]) == 'neutral':
                self.plneut += 1
##                player.write('neut\n')
            print(self.pltotal, self.plpos, self.plneg, self.plneut)
        sen=('%d,%d,%d,%d\n')%(self.pltotal, self.plpos, self.plneg, self.plneut)
        player.write(sen)
        player.close()

if __name__ == '__main__':
    Sentiment().main()
