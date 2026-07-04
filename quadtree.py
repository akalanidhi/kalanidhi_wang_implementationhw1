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
        self.segment_count = 0                  #total number of segments in the quadtree

    def insert(self, segment):
        """
        inserts a segment into quadtree.
        if node is not provided, insertion starts at the root.
        recursion is handled inside this function.
        
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
        """
        self.segment_count += 1
        self._insert(self.root, segment)

    def _insert(self, node, segment):

        # Ignore segments completely outside this node
        if not node.boundary.int_segment(segment):
            return

        # Leaf with room
        if node.is_leaf and len(node.segments) < self.max_segments:
            node.segments.append(segment)
            return

        # Need to split
        if node.is_leaf:
            self.split(node)

        # Insert into every intersecting child
        inserted = False

        for child in node.children:

            if child.boundary.int_segment(segment):
                self._insert(child, segment)
                inserted = True

        # Segment crosses multiple children
        if not inserted:
            node.segments.append(segment)

    def split(self, node):

        node.children = [
            quadNode(node.boundary.get_quad(0), node.level + 1),
            quadNode(node.boundary.get_quad(1), node.level + 1),
            quadNode(node.boundary.get_quad(2), node.level + 1),
            quadNode(node.boundary.get_quad(3), node.level + 1)
        ]

        node.is_leaf = False

        old_segments = node.segments
        node.segments = []

        for seg in old_segments:
            for child in node.children:
                if child.boundary.int_segment(seg):
                    self._insert(child, seg)

    def query(self, rectangle):
        results = []

        self._query(self.root, rectangle, results)

        return results
    
    def _query(self, node, rectangle, results):

        if node is None:
            return

        if not node.boundary.int_rectangle(rectangle):
            return

        for seg in node.segments:

            if seg.int_rectangle(rectangle):
                results.append(seg)

        if not node.is_leaf:

            for child in node.children:
                self._query(child, rectangle, results)

    def report(self):
        #Print information about the tree.
        ...

    def count_nodes(self):
        return self._count_nodes(self.root)

    def _count_nodes(self, node):

        if node is None:
            return 0

        total = 1

        for child in node.children:
            total += self._count_nodes(child)

        return total

    def draw(self, screen):
        self._draw(screen, self.root)
    
    def _draw(self, screen, node):

        if node is None:
            return

        node.boundary.draw(screen)

        for seg in node.segments:
            seg.draw(screen)

        if not node.is_leaf:

            for child in node.children:
                self._draw(screen, child)


    def find(self, point):
        return self._find(self.root, point)

    def _find(self, node, point):

        if node is None:
            return None

        if not node.boundary.cont_point(point):
            return None

        if node.is_leaf:
            return node

        for child in node.children:

            result = self._find(child, point)

            if result is not None:
                return result

        return node


    def clear_highlights(self):
        """
        Placeholder for later animation.
        """
        pass


    def print_tree(self):
        self._print(self.root)

    def _print(self, node):

        if node is None:
            return

        indent = "    " * node.level

        print(
            f"{indent}Level {node.level} | "
            f"Segments: {len(node.segments)}"
        )

        for child in node.children:
            self._print(child)