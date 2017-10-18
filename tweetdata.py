
import json
import csv
##import pandas as pd

##tweets_data_path = 'roger_tweets.json'
##
##tweets_data = []
##tweets_file = open(tweets_data_path, "r")
##for line in tweets_file:
##    try:
##        tweet = json.load(line)
##        tweets_data.append(tweet)
##    except:
##        raise
##        continue
##print(len(tweets_data))
##print(tweets_data)

##file = open('roger_tweets.csv').read()
##data =[]
##
##for r in file.split('\n'):
##    data.append(r)
##for i in range(10):
##    print(data[i])
##    
##print(data)



##fig = plt.figure(figsize=(xinch,yinch/.8))
##
##ax = plt.axes([0., 0., 1., .8], frameon=False, xticks=[],yticks=[])
##ax.imshow(img, interpolation='none')
##ax.set_title('Matplotlib is fun!', size=16, weight='bold')
##plt.savefig('e:\\mpl_logo.png', dpi=dpi, transparent=True)

##try:
##    file = open('rog_sen.txt','r').read()
##    tweet=[]
##    number=[]
##    for line in file.split("\n"):
##        x, y = line.split()
##        number.append(int(x))
##        tweet.append(y)
##
##    print(tweet)
##    self.total = number[0]
##    self.pos = number[1]
##    self.neg = number[2]
##    self.neut = number[3]
##    print(self.total, self.pos, self.neg, self.neut)
import pickle
##try:
##    file = open('rog_sen.txt','r').read()
##    tweet=[]
##    number=[]
##    for line in file.split("\n"):
##        x, y = line.split()
##        number.append(int(x))
##        tweet.append(y)
##
##    
##    
##    print(tweet)
##    total = number[0]
##    pos = number[1]
##    neg = number[2]
##    neut = number[3]
##    print(total, pos, neg,neut)
##
##total =300
##pos =200
##neut =50
##neg = 50
##data = """%d total
##%d pos
##%d neg
##%d neut"""%(total, pos,neg,neut)
##
##file =['total','pos','neg','neut']
##
##print(data)
##rog = open('rog_sen.pickle', 'wb')
##pickle.dump(file, rog)
##rog.close()

# bog = open('final/data/pickles/rog_sen.pickle', 'rb')
# file1 = pickle.load(bog)
# bog.close()
# print(file1)
# number=[]
# for line in file1.split('\n'):
#     print(line)
#     x = line.split()[0]
#     print(x)
#     number.append(int(x))
# print(number)


# player = open('pl_sen.txt', 'r').readline()
# pos, neg= player.split(',')

# print(pos, neg)
# file1 = open('pl_sen.txt', 'w')
# tpos = int(pos)+10
# tneg = int(neg)+10
# sen = '%d,%d'%(tpos, tneg)
# file1.write(sen)
# file1.close()

# player1 = open('pl_sen.txt', 'r').readline()
# pos, neg= player1.split(',')
# print(pos ,neg)

# from liveSearch_API import liveApi
# import threading
# from Sentiment_analysis import Sentiment
# from PyQt4 import QtGui, QtCore
# import sys
# from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# import time


# class Gui():
# 	def __init__(self):
# 		self.widget = QtGui.QWidget()
# 		# self.check()
# 		self.widget.show()

# 	def check(self):

# 		vl = QtGui.QVBoxLayout(self.widget)
# 		# button = QtGui.QPushButton('press me', widget)
# 		# vl.addWidget(button)
# 		# button1 = QtGui.QPushButton('press me1', widget)
# 		# vl.addWidget(button1)


# 		livefigure = plt.figure()
# 		livecanvas = FigureCanvas(livefigure)

# 		vl.addWidget(livecanvas)
# 		ax = livefigure.add_subplot(111)

# 		def animate(i):
# 			graph_data = open('data/pl_sen','r').read()
# 			lines = graph_data.split('\n')
# 			xar=[]
# 			yar=[]
# 			x=0
# 			y=0
# 			for line in lines:
# 				x+=1
# 			if('pos' in line):
# 				y+=1
# 			elif 'neg' in line:
# 				y-=1
# 			elif 'neut' in line:
# 				y=y

# 			xar.append(x)
# 			yar.append(y)

# 			ax.clear()

# 			ax.set_ylim(min(yar)-1, max(yar)+1)
# 			ax.plot(xar,yar)


# 		ani = animation.FuncAnimation(livefigure, animate, interval=50)

# 		livecanvas.draw()
	
	


# def runapi():
# 	sentiment = Sentiment()
# 	live=liveApi(sentiment)
# 	live.runStream()

# def opengraph():
# 	# import livegraph
# 	# print('graph')
# 	# widget.show()
# 	Gu=Gui()
# 	Gu.check()	



# app = QtGui.QApplication(sys.argv)
# widget = QtGui.QWidget()

# Gu=Gui()
# Gu.check()

# t1 = threading.Thread(target = runapi)
# # t2 = threading.Thread(target = opengraph)
# # threads = []
# # threads.append(t2)
# # threads.append(t1)
# t1.start()
# # t2.start()

# # for x in threads:
# # 	x.join()
# sys.exit(app.exec_())


graph_data = open('data/bar','r').read()
lines = graph_data.split('\n')
length = len(lines)-1
print(length)
# lines = graph_data.split('\n')
xs = ["total","pos","neg","neut"]
ys = [0,0,0,0]

i,j,l,m = lines[length-1].split(',')
ys[0]+=int(i)
ys[1]+=int(j)
ys[2]+=int(l)
ys[3]+=int(m)
print(ys)