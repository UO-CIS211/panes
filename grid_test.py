"""
Basic exercise of panes.py by drawing. 

"""
import panes
from panes import Pane, GridPane, Polygon
panes.SIZE = 1000,800
import random

color_wheel =  [ (0,0,0), (250,128,114), (139,0,0),
                    (255,215,0), (250,250,210), (50,205,50),
                    (0,100,0),(102,205,208), (0,191,255),
                    (65,105,225), (100,149,237), (0,0,205),
                    (230,230,250), (221,160,221), (147,112,219) ]
random.shuffle(color_wheel)

root = Pane(root=True)

width,height = panes.SIZE

grid = GridPane(root, 10, 5)
for row in range(10):
    for col in range(5):
        grid.append(panes.GridCellPoly(row, col,
                                       fill=random.choice(color_wheel)))
        
root.render()
input("Press enter to end")    
