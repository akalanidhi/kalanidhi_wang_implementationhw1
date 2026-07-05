from geometry import Point

class quadNode:
    """
    represents a node in the quadtree.
    each node has: a rectangular boundary, a list of segments it contains, and up to 4 children.
    if the number of segments exceeds max_segments, the node splits into 4 quadrants.
    """
    def __init__(self, boundary, level=0, anim = None):
        self.boundary = boundary  #rectangle object defining the node's region
        self.segments = []        #list of segments contained in this node
        self.children = [None] * 4  #list of 4 child nodes (NW, NE, SW, SE)
        self.is_leaf = True       # true if this node has no children (optional, can be inferred from children, mainly for simplicity)
        self.level = level        #depth level of this node in the quadtree (also optional, mainly for debugging/visualization if want different colors)
        self.anim = anim
        self.endpoint_count = 0

class quadTree:
    """
    represents the quadtree structure.
    manages insertion of segments, querying, and visualization.
    """
    def __init__(self, boundary, anim=None):
        self.root = quadNode(boundary, anim=anim)   #root node of the quadtree
        self.max_segments = 3            #maximum segments a node can hold before splitting
        self.segment_count = 0                  #total number of segments in the quadtree
        self.anim = anim

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
        """
        Recursively inserts a segment into the quadtree.

        A segment is stored only in leaf nodes. If a leaf overflows
        (more than max_segments), it is split and its segments are
        redistributed among the appropriate children.
        """

        # Highlight visited node (animation)
        self._highlight_node(node)

        # Segment does not intersect this node's region
        if not node.boundary.int_segment(segment):
            return

        # Update endpoint count for this node
        left = Point(segment.x1, segment.y)
        right = Point(segment.x2, segment.y)

        if node.boundary.cont_point(left):
            node.endpoint_count += 1

        if node.boundary.cont_point(right):
            node.endpoint_count += 1

        if node.is_leaf:

            # Leaf has room
            if len(node.segments) < self.max_segments:
                node.segments.append(segment)
                return

            # Leaf is full -> split it
            self.split(node)
        for child in node.children:

            if child.boundary.int_segment(segment):
                self._insert(child, segment)

    def split(self, node):

        node.children = [
            quadNode(node.boundary.get_quad(0), node.level + 1, self.anim),
            quadNode(node.boundary.get_quad(1), node.level + 1, self.anim),
            quadNode(node.boundary.get_quad(2), node.level + 1, self.anim),
            quadNode(node.boundary.get_quad(3), node.level + 1, self.anim)
        ]

        node.is_leaf = False

        old_segments = node.segments
        node.segments = []

        for seg in old_segments:
            for child in node.children:
                if child.boundary.int_segment(seg):
                    self._insert(child, seg)

    def range_report(self, rectangle):
        results = []

        self._range_report(self.root, rectangle, results)

        return results
    
    def _range_report(self, node, rectangle, results):

        if node is None:
            return
        
        self._highlight_node(node)  # highlight the node being visited

        if not node.boundary.int_rectangle(rectangle):
            return
        
        for seg in node.segments:

            if seg.int_rectangle(rectangle):
                results.append(seg)

        if not node.is_leaf:

            for child in node.children:
                self._range_report(child, rectangle, results)

    def range_count(self, rectangle): 
        return self._range_count(self.root, rectangle)
    
    def _range_count(self, node, rectangle):
        if node is None:
            return 0

        self._highlight_node(node)

        # completely outside
        if not node.boundary.int_rectangle(rectangle):
            return 0

        # node completely inside query
        if rectangle.cont_rectangle(node.boundary):
            return node.endpoint_count

        # leaf
        if node.is_leaf:

            total = 0

            for seg in node.segments:

                if rectangle.cont_point(
                    Point(seg.x1, seg.y)
                ):
                    total += 1

                if rectangle.cont_point(
                    Point(seg.x2, seg.y)
                ):
                    total += 1

            return total

        total = 0

        for child in node.children:

            total += self._range_count(
                child,
                rectangle
            )

        return total


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
        
        self._highlight_node(node)  # highlight the node being visited

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
        self.anim._highlighted_quads.clear()

    def _highlight_node(self, node):
        if self.anim:
            b = node.boundary
            self.anim.print_and_highlight_quadrant(b.x_min, b.y_min, b.x_max, b.y_max)
        
        else:
            return
        
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

    def count_segments(self):
        return self.segment_count