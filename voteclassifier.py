from nltk.classify import ClassifierI
from statistics import mode
#=================================================================
#=================================================================
#=================================================================
#======================class Vote Classifier===================
class voteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def f_classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
##        if len(set(votes)) != len(votes):
##            Most = mode(votes)
##            print('the mode is ', Most)
            
##        else:
##            print('no duplicates in nums')
##        print(votes)
##        print(len(votes))
        return mode(votes)
    
    def f_confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf

#====================================
