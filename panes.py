"""
A 'pane' is a simple kind of 2D scene graph.  A pane is 
a graphics context with its own origin and scale factors, 
both relative to its parent frame.  A pane may contain 
individual graphics objects (polygons and polylines) and 
nested panes, each in coordinates relative to the pane.

We use pygame as the underlying graphics system. As a 
consequence of this, we have double-buffering and need 
to explicitly render and flip to see the scene. 
"""
import pygame

SIZE = 500,500
screen = None
pygame.init()

class Error(Exception):
    """Base class for exceptions in this module"""
    pass

class PanesError(Error):
    """Not further differentiated"""

    def __init__(self, expression, message):
        self.expression = expression;
        self.message = message

class Pane:
    """
    A graphics context and a list of objects to be rendered in 
    that context. 
    """
    def __init__(self, parent=None, root=False,  tr=(0,0), sf=1.0):
        if not root and not parent:
            raise PanesError("Every non-root pane must have a parent")
        self.parent = parent
        self.dx, self.dy = tr
        self.sf = sf
        self.contents = [ ]

        global screen
        if root:
            if not screen:
                screen = pygame.display.set_mode(SIZE)
                screen.fill((255,255,255))
        else:
            parent.append(self)

    def append(self, el):
        """
        Append a polyline, polygon, or nested pane. 
        """
        self.contents.append(el)

    def render(self, transform=None):
        transform = Transform(self.dx, self.dy, self.sf, prior=transform)
        for el in self.contents:
            el.render(transform)
        if not self.parent:
            pygame.display.flip()
            screen.fill((255,255,255)) # For next frame


def is_numeric(x):
    return isinstance(x,int) or isinstance(x,float)

class Poly:
    """
    Base class for polylines and polygons. 
    Sequence of points, relative to a Pane. 
    """
    def __init__(self, points=[], stroke=None, fill=None):
        self.__validate_points(points)
        self.points = points

    def _validate_points(self, points):
        for point in points:
            if len(point) != 2:
                raise PanesError("Each point must be a pair of numbers")
            x,y = point
            if not is_numeric(x) or not is_numeric(y):
                raise PanesError("Points must be pairs of int or float")
            
class Transform:
    """
    A transform relates world coordinates to screen coordinates.
    We build up transforms as we traverse a tree of Panes. 

    Attributes: 
       dx, dy:  Origin relative to screen
       sf:      Scale factor
    """
    def __init__(self,  dx, dy, sf, prior=None):
        if prior:
            self.dx = prior.dx + prior.sf*dx
            self.dy = prior.dy + prior.sf*dy
            self.sf = prior.sf * sf
        else:
            self.dx = dx
            self.dy = dy
            self.sf = sf

    def tx(self, pt):
        x,y = pt
        return self.dx + self.sf * x, self.dy + self.sf * y

class Polygon(Poly):
    """
    A polygon is closed and may have a fill.
    """
    def __init__(self, points=[], stroke=None, fill=None):
        self._validate_points(points)
        self.points = points
        self.stroke = stroke or 0
        self.fill = fill or (255,0,0)
            

    def render(self, context):
        """
        Render this polygon in the given 
        relative to the transformation context
        """
        assert isinstance(context, Transform)
        screen_coords = [ ]
        for pt in self.points:
            screen_coords.append( context.tx(pt) )
        pygame.draw.polygon(screen, self.fill, screen_coords, self.stroke)

    
if __name__ == "__main__":
    root = Pane(root=True)
    tr0 = Transform(0,0,1)
    tr1 = Transform(100,100,0.5, prior=tr0)
    tr2 = Transform(100,100,0.5, prior=tr1)

    p1 = Polygon([(0,0), (0,100), (100,100), (0,0)])
    root.append(p1)

    child = Pane(parent=root, sf=.5, tr=(100,100))
    child.append(p1)

    
    grandchild = Pane(parent=child, sf=0.5, tr=(100,100))
    grandchild.append(p1)


    root.render()
    input("Press enter to end")    
    

    
