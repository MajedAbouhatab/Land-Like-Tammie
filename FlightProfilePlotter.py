import sqlite3
import matplotlib.pyplot as plt
import matplotlib.animation
import time
LastValue=0
LastTimeStamp=0

def PlotTopic(Topic,SubPlot):
    global LastValue,LastTimeStamp
    # Get latest Topic data
    c.execute("SELECT timestamp,scalar FROM Data WHERE topic='"+Topic+"' order by 1 desc limit 50")#order by 1 desc limit 50
    # Create empty lists to be used as x and y for plotting
    timestamp,scalar = [],[]
    # Add topic data to the proper list
    for d in c.fetchall():
        LastTimeStamp=d[0]
        timestamp.append(LastTimeStamp)
        LastValue=d[1]
        scalar.append(LastValue)
    # Clear previous plot
    plt.subplot(SubPlot).clear()
    # What are we looking at?
    plt.subplot(SubPlot).title.set_text(Topic)
    # Connect x,y points
    plt.plot(timestamp,scalar,'-')
    # Remove clutter
    plt.xticks([])
    plt.yticks([])
    # Experimental feature to avoid graphics overlap
    plt.tight_layout()
    plt.gcf().canvas.set_window_title('Flight Profile Plotter')
    #plt.ylim(25, 55)

def animate(x):
    for i,L in enumerate(TopicList):
        # Call plotting function for a specific topic and location on layout
        PlotTopic(L,str(len(TopicList)+1)+'1'+str(i+2))
        plt.subplot(str(len(TopicList)+1)+'1'+str(i+1)).clear()
        plt.subplot(str(len(TopicList)+1)+'1'+str(i+1)).text((i+1)/10,(i+1)*7/10,L,fontsize=30)
        plt.subplot(str(len(TopicList)+1)+'1'+str(i+1)).text((i+1)/10,(i+1)*4/10,str(LastValue)+' Feet',fontsize=30)
        plt.subplot(str(len(TopicList)+1)+'1'+str(i+1)).text((i+1)/10,(i+1)*2/10,str(time.ctime(int(str(LastTimeStamp)[:10]))),fontsize=10)
        #plt.xticks([])
        #plt.yticks([])
        plt.axis('off')
    
conn = sqlite3.connect('/home/pi/Desktop/FP.db')
c = conn.cursor()
# Dummy table
c.execute("CREATE TABLE IF NOT EXISTS Data(timestamp INTEGER, topic TEXT, scalar INTEGER)")
# Topics in database
c.execute("SELECT DISTINCT topic FROM Data ORDER BY 1 DESC")
# Create empty list to hold topics
TopicList=[]
# Add topics to the list
for d in c.fetchall():
        TopicList.append(d[0])
# If we start plotting before data is available
if not TopicList: 
    TopicList.append("ALTITUDE")
# Set animation
a = matplotlib.animation.FuncAnimation(plt.figure(),animate)
# Bring it all together
plt.show()
