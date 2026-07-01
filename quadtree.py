"""
SAMPLE IMPLEMENTATION, dont need to follow but helps me keep track of which types of functions will likely exist where

quadNode 
members: 
    boundary: Rectangle
    segments: list
    children: list[4]
    is_leaf
    level

insert(segment)
split()
query(rect)
contains(segment)
draw(screen)
count_nodes()
count_segments()



quadTree
members:
    root
    node_count
    segment_count
    max_segments = 3


insert(segment)
query(rect)
find(point)
clear_highlights()
draw(screen)
print_tree()

"""

class quadNode:
    """
    represents a node in the quadtree.
    each node has: a rectangular boundary, a list of segments it contains, and up to 4 children.
    if the number of segments exceeds max_segments, the node splits into 4 quadrants.
    """
    def __init__(self, boundary, level=0):
        self.boundary = boundary  #rectangle object defining the node's region
        self.segments = []        #list of segments contained in this node
        self.children = [None] * 4  #list of 4 child nodes (NW, NE, SW, SE)
        self.is_leaf = True       # true if this node has no children (optional, can be inferred from children, mainly for simplicity)
        self.level = level        #depth level of this node in the quadtree (also optional, mainly for debugging/visualization if want different colors)

class quadTree:
    """
    represents the quadtree structure.
    manages insertion of segments, querying, and visualization.
    """
    def __init__(self, boundary):
        self.root = quadNode(boundary)   #root node of the quadtree
        self.max_segments = 3            #maximum segments a node can hold before splitting

    def insert(self, segment):
        """
        inserts a segment into quadtree.
        if node is not provided, insertion starts at the root.
        recursion is handled inside this function.
        """
        #start at root if no node provided
        if node is None:
            node = self.root

    #Case 1: base case --> node has space for the segment
        #if leaf node and has less than 3 segments currently, store segment here
        #node.children[0] is None is a proxy check for the whole node being a leaf, bc if it's a leaf, all children should be None
        if node.children[0] is None and len(node.segments) < self.max_segments:
            node.segments.append(segment)
            return

    #Case 2: recursive case --> node is full and needs to split, redistribute segments, and insert into children
        #if leaf node but already 3 segments, split first
        if node.children[0] is None:
            mid_x = (node.boundary.x_min + node.boundary.x_max) / 2
            mid_y = (node.boundary.y_min + node.boundary.y_max) / 2

            node.children = [
                quadNode(node.boundary.get_quad(0), node.level + 1),
                quadNode(node.boundary.get_quad(1), node.level + 1),
                quadNode(node.boundary.get_quad(2), node.level + 1),
                quadNode(node.boundary.get_quad(3), node.level + 1)
            ]

            node.is_leaf = False

            #redistribute OLD segments into children bc now that the node has children, the segments should be pushed down to the appropriate quadrants
            old_segments = node.segments
            node.segments = []

            for old_seg in old_segments:
                self.insert(old_seg, node)

            #insert NEW segment into children (can be multiple children if it spans quadrants)
            for child in node.children:
                if child.boundary.int_segment(segment):
                    self.insert(segment, child)

    def query(self, rectangle):
        """Return all segments intersecting the rectangle."""

    def report(self):
        """Print information about the tree."""
        ...

    def count_nodes(self):
        """Return the total number of nodes."""

    def draw(self, screen):
        """Draw the entire quadtree."""
