"""
Depict CIS course schedule in grid

"""
import panes
from panes import Pane, GridPane, Polygon
panes.SIZE = 1000,800
import random

bk_gnd = [ (242,242,242), (217,217,217) ]

class_color = (153,204,255) #light sky blue

bars  = [ (255,153,153), #pink
          (204,255,204), #light green
          (153,204,255)  #light sky blue
         ]

start_hour = 8

root = Pane(root=True)
width,height = panes.SIZE

framed = panes.Framed(root, left=30,right=10,top=30,bottom=10)
grid = GridPane(framed, 10, 5)

day_columns = { "m": 0, "t": 1, "w": 2, "r": 3, "f": 4 }
offsets_col = { "A": 0.1, "B": 0.4, "C": 0.7 }

def hours_offset( time_string ):
    """
    From a time string like "1420", produce a
    numeric offset in hours from start_hour, e.g., 
    14-8 = 6 + 20/60 = 6.33
    """
    hour = int(time_string[0:2])
    minute = int(time_string[2:4])
    offset = (hour - start_hour) + minute/60
    return offset

def draw_bar(pane, in_col, from_time, to_time):
    pane.append(panes.Polygon(
        [(in_col,from_time), (in_col,to_time),
         (in_col+0.2,to_time), (in_col+0.2, from_time),
         (in_col,from_time)],
         fill=class_color))

# Background columns in alternating greys
for col in range(5):
    for row in range(10):
        # Grey fill
        grid.append(panes.GridCellPoly(row, col,
                                       stroke=0,
                                       fill=bk_gnd[col % 2]))
        # white stroke
        grid.append(panes.GridCellPoly(row, col,
                                       stroke=2,
                                       fill=(255,255,255)))

# Label the hours
for row in range(10):
    offset = row
    label_y = grid.y_out(offset, root)
    # print("Y coord for label: {} -> {}".format(offset, label_y))
    root.append(panes.Text("{}".format(start_hour+row),
                               10, label_y, size=20))

# Label the days
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
for col in range(5):
    label_x = grid.x_out(col, root)
    print("Placing {} at {},{}".format(days[col], label_x, 5))
    root.append(panes.Text(days[col], label_x, 5, size=20))


for line in open("data/conflicts.txt"):
    if line[0] not in "ABC": continue
    col_label = line[0]
    fields = line.split()
    day_label = fields[1]
    times = fields[2].split("-")
    start_hour_offset = hours_offset(times[0])
    end_hour_offset = hours_offset(times[1])
    class_num = fields[5]

    col_pos = day_columns[day_label] + offsets_col[col_label]
    draw_bar(grid,col_pos, start_hour_offset, end_hour_offset)
    grid.append(panes.Text(class_num,
                               col_pos + 0.05,
                               (start_hour_offset + end_hour_offset)/2, 
                               size=18
                               ))

        

root.render()
input("Press enter to end")    
