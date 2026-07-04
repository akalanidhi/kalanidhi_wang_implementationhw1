"""
SAMPLE IMPLEMENTATION, dont need to follow but helps me keep track of which types of functions will likely exist where

class Point

__init(x,y)
__repr__()

class Segment
__init__(x1, x2, y)
contains_point(point)
intersects_rectangle(rect)
draw(screen)


class Rectangle
__init__()
contains_point(point)
contains_segment(segment)
intersects_segment(segment)
intersects_rectangle(rectangle)
get_quadrant(index)
draw(screen)t



"""

class Point:
    """
    represents a 2D point with x and y coordinates.
    used to represent endpoints of segments and locations in plane. 
    plane defined with (0,0) at bottom left and (2^H-1, 2^H-1) at top right.
    """
    def __init__(self, x, y):
        """
        initializes a Point with x and y coords.
        both x and y should be numeric values (int or float).
        """
        self.x = x
        self.y = y

        if not isinstance(x, (int, float)):
            raise TypeError("x must be a number")
        if not isinstance(y, (int, float)):
            raise TypeError("y must be a number")
        
    def __repr__(self):
        """
        returns a str representation of Point (mainly for debugging and printing).
        """
        return f"Point({self.x}, {self.y})"
    
class Segment:
    """
    represents a horizontal line segment defined by two x-coordinates and a y-coordinate.
    since the segment is horizontal, the y-coordinate is constant across its entire length.
    segments are stored by index in the global SegmentArray; nodes reference them by index.
    """
    def __init__(self, x1, x2, y):
        """
        initializes a horizontal Segment with left endpoint x1, right endpoint x2, and height y.
        x1 should be <= x2 (left to right); y is the fixed vertical position of the segment.
        """
        self.x1 = x1
        self.x2 = x2
        self.y = y

    def cont_point(self, point):
        """
        checks whether a given point lies exactly on this segment.
        the point must be at the same y-coordinate (to ensure horizontal) and have x between x1 and x2 (inclusive).
        returns True if the point is on the segment, False otherwise.
        function not used in quadtree, but useful for counting endpoints in NumOfEndpoints.
        """
        return self.y == point.y and self.x1 <= point.x <= self.x2

    def int_rectangle(self, rect):
        """
        checks whether this segment intersects (overlaps with) a given rectangle.
        the segment's y must fall within the rectangle's vertical range,
        and the segment must not be entirely to the left or right of the rectangle.
        returns True if any part of the segment passes through the rectangle, False otherwise.
        """
        if not (rect.y_min <= self.y <= rect.y_max):
            return False
        return not (self.x2 < rect.x_min or self.x1 > rect.x_max)

    def draw(self, screen):
        """
        draws this segment on the given pygame screen.
        placeholder — to be implemented with pygame drawing logic.
        """
        pass

class Rectangle:
    """
    represents a 2D axis-aligned rectangle defined by its four boundary edges.
    used to represent the region R(v) associated with each quadtree node.
    the rectangle is defined by x_min (left), x_max (right), y_min (bottom), y_max (top).
    """
    def __init__(self, x_min, x_max, y_min, y_max):
        """
        initializes a Rectangle with its boundary edges.
        x_min and y_min are the lower bounds; x_max and y_max are the upper bounds.
        """
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    def cont_point(self, point):
        """
        checks whether a given point lies inside (or on the boundary of) this rectangle.
        function not used in quadtree, but useful for counting endpoints in NumOfEndpoints.
        returns True if the point is within bounds on both x and y axes, False otherwise.
        """
        return (self.x_min <= point.x <= self.x_max) and (self.y_min <= point.y <= self.y_max)

    def cont_segment(self, segment):
        """
        checks whether both endpoints of a segment lie within this rectangle.
        this is stricter than int_segment — the entire segment must be inside.
        returns True only if both (x1, y) and (x2, y) are contained in the rectangle.
        """
        return (self.cont_point(Point(segment.x1, segment.y)) and 
                self.cont_point(Point(segment.x2, segment.y)))

    def int_segment(self, segment):
        """
        checks whether a segment intersects (partially or fully overlaps) this rectangle.
        the segment's y must be within vertical bounds, and it must not be fully outside horizontally (inclusive).
        used during insertion to determine which quadrant children a segment should be pushed into.
        returns True if any part of the segment overlaps this rectangle, False otherwise.
        """
        if not (self.y_min <= segment.y <= self.y_max):
            return False
        return not (segment.x2 < self.x_min or segment.x1 > self.x_max)

    def int_rectangle(self, other):
        """
        checks whether this rectangle overlaps with another rectangle.
        used during range queries to determine if a quadtree node's region must be searched 
        (if node's boundary doesn't intersect query rectangle, whole subtree can be skipped).
        returns True if the two rectangles share any area, False if they are completely separate.
        """
        return not (self.x_max < other.x_min or self.x_min > other.x_max or 
                    self.y_max < other.y_min or self.y_min > other.y_max)

    def get_quad(self, index):
        """
        divides this rectangle into 4 equal quadrants and returns the one at the given index.
        index mapping: 0 = top-left (NW), 1 = top-right (NE), 2 = bottom-left (SW), 3 = bottom-right (SE).
        the midpoint is computed by averaging the min and max on each axis.
        raises ValueError if index is not in range [0, 3].
        """
        mid_x = (self.x_min + self.x_max) // 2
        mid_y = (self.y_min + self.y_max) // 2
        if index == 0:  # top-left (NW)
            return Rectangle(self.x_min, mid_x, mid_y, self.y_max)
        elif index == 1:  # top-right (NE)
            return Rectangle(mid_x, self.x_max, mid_y, self.y_max)
        elif index == 2:  # bottom-left (SW)
            return Rectangle(self.x_min, mid_x, self.y_min, mid_y)
        elif index == 3:  # bottom-right (SE)
            return Rectangle(mid_x, self.x_max, self.y_min, mid_y)
        else:
            raise ValueError("index must be in range [0-3]")

    def draw(self, screen):
        """
        draws this rectangle on the given pygame screen.
        placeholder — to be implemented with pygame drawing logic.
        """
        pass