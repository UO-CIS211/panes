"""
Basic exercise of panes.py by drawing. 

"""
import panes
from panes import Pane, Polygon
panes.SIZE = 1000,800
import random
import time

color_wheel =  [ (0,0,0), (250,128,114), (139,0,0),
                    (255,215,0), (250,250,210), (50,205,50),
                    (0,100,0),(102,205,208), (0,191,255),
                    (65,105,225), (100,149,237), (0,0,205),
                    (230,230,250), (221,160,221), (147,112,219) ]
random.shuffle(color_wheel)

root = Pane(root=True)

width,height = panes.SIZE
shape = [(0,0), (0,height), (width, height), (width,0), (0,0)]


root.append(Polygon(shape, fill = color_wheel[0] ))

def recurse(n, parent):
    if n < 1:
        return
    nw = Pane(parent=parent, sf=0.5, tr=(0,0))
    nw.append(Polygon(shape, fill=random.choice(color_wheel)))
    recurse(n-1, nw)
    
    ne = Pane(parent=parent, sf=0.5, tr=(0.5*width,0))
    ne.append(Polygon(shape, fill=random.choice(color_wheel)))
    recurse(n-1, ne)

    sw = Pane(parent=parent, sf=0.5, tr=(0,0.5*height))
    sw.append(Polygon(shape, fill=random.choice(color_wheel)))
    recurse(n-1, sw)

    se = Pane(parent=parent, sf=0.5, tr=(0.5*width,0.5*height))
    se.append(Polygon(shape, fill=random.choice(color_wheel)))    
    recurse(n-1, se)

for i in range(8):
   recurse(i,root)
   root.render()
   time.sleep(1)
for i in reversed(range(7)):
   recurse(i,root)
   root.render()
   time.sleep(1)

    
input("Press enter to end")    
