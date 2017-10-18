import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

##style.use('fivethirtyeight')
style.use('ggplot')        

fig=plt.figure()
ax1=fig.add_subplot(1,1,1)

def animate(i):
    graph_data = open('data/bar','r').read()
    lines = graph_data.split('\n')
    length = len(lines)-1
    print(length)
    xs = ["total","pos","neg","neut"]
    ys = [0,0,0,0]
    if length > 1:
        i,j,l,m = lines[length-1].split(',')
        ys[0]+=int(i)
        ys[1]+=int(j)
        ys[2]+=int(l)
        ys[3]+=int(m)
    
    
    ax1.clear()
    ax1.bar(range(len(xs)), ys)


ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
