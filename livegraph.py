import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

# style.use('fivethirtyeight')
style.use("ggplot")

fig=plt.figure()
ax1=fig.add_subplot(1,1,1)


def animate(i):
    graph_data = open('data/pl_sen','r').read()
    lines = graph_data.split('\n')
    xar=[]
    yar=[]

    x=0
    y=0

    for line in lines:
        x+=1
        if('pos' in line):
            y+=1
        elif 'neg' in line:
            y-=1
        elif 'neut' in line:
            y=y

        xar.append(x)
        yar.append(y)
    
    ax1.clear()
    
    ax1.set_ylim(min(yar)-1,max(yar)+1)
    ax1.plot(xar,yar)


ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
