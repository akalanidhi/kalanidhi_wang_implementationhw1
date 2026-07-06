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

        if node.is_leaf:

            # Leaf has room
            if len(node.segments) < self.max_segments:
                node.segments.append(segment)
                return

            # Leaf is full -> split it
            self.split(node)
        children_hit = []

        for i, child in enumerate(node.children):
            if child.boundary.int_segment(segment):
                children_hit.append(i)

        print(
            segment.x1,
            segment.x2,
            segment.y,
            "hits children",
            children_hit,
            "at level",
            node.level,
        )

        for child in node.children:

            if child.boundary.int_segment(segment):
                self._insert(child, segment)

    def build_endpoint_counts(self):
        self._build_endpoint_counts(self.root)

    def _build_endpoint_counts(self, node):
        if node is None:
            return 0

        if node.is_leaf:
            total = 0

            for seg in node.segments:

                # Degenerate segment (a single point)
                if seg.x1 == seg.x2:
                    if node.boundary.cont_point(Point(seg.x1, seg.y)):
                        total += 1

                # Normal segment
                else:
                    if node.boundary.cont_point(Point(seg.x1, seg.y)):
                        total += 1

                    if node.boundary.cont_point(Point(seg.x2, seg.y)):
                        total += 1

            node.endpoint_count = total
            return total

        total = 0

        for child in node.children:
            total += self._build_endpoint_counts(child)

        node.endpoint_count = total

        return total

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

    def range_report(self, rectangle, log_path="log.txt"):
        results = set()

        x1, y1, x2, y2 = rectangle.x_min, rectangle.y_min, rectangle.x_max, rectangle.y_max

        with open('log.txt', "a") as log_file:
            log_file.write(f"RangeReporting was called with parameters {x1}, {y1}, {x2}, {y2}.\n")
        self._range_report(self.root, rectangle, results, log_file) #printing the log file is handled in the recursive function

        return results
    
    def _range_report(self, node, rectangle, results, log_file):

        if node is None:
            return
        
        self._highlight_node(node)  # highlight the node being visited

        if not node.boundary.int_rectangle(rectangle):
            return
        
        x1, y1, x2, y2 = rectangle.x_min, rectangle.y_min, rectangle.x_max, rectangle.y_max
        
        for seg in node.segments:

            if seg.int_rectangle(rectangle):
                if seg not in results:
                    results.add(seg)

                    if self.anim:              
                        self.anim.highlight_segment(seg)
                    with open ('log.txt', 'a') as log_file:
                        log_file.write(
                        f"reporting segment {seg.name} whose coordinates are "
                        f"{seg.x1} {seg.y} {seg.x2}. It intersects the query region "
                        f"{x1} {y1} {x2} {y2}\n")

        if not node.is_leaf:

            for child in node.children:
                self._range_report(child, rectangle, results, log_file)

    def range_count(self, rectangle, log_path="log.txt"):
        seen = set()
        count = self._range_count(self.root, rectangle, seen)

        x1, y1, x2, y2 = rectangle.x_min, rectangle.y_min, rectangle.x_max, rectangle.y_max

        with open('log.txt', "a") as log_file:
            log_file.write(
            f"RangeCounting was called with parameters {x1} {y1} {x2} {y2}. "
            f"We found {count} endpoints of segments inside the query region.\n"
        )

        return count
    
    def _range_count(self, node, rectangle, seen):
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
                if id(seg) in seen:
                    continue
                seen.add(id(seg))

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

            total += self._range_count(child,rectangle, seen)

        return total

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
    
    def check_duplicates(self):
        counts = {}

        def dfs(node):
            if node is None:
                return

            for seg in node.segments:
                key = (seg.x1, seg.x2, seg.y)
                counts[key] = counts.get(key, 0) + 1

            for child in node.children:
                dfs(child)

        dfs(self.root)

        for seg, c in counts.items():
            print(seg, c)

    def print_segment_locations(self):
        self._print_segment_locations(self.root)

    def _print_segment_locations(self, node):
        if node is None:
            return

        if node.is_leaf:
            for seg in node.segments:
                print(
                    id(seg),
                    seg.x1, seg.x2, seg.y,
                    "leaf:",
                    node.boundary.x_min,
                    node.boundary.x_max,
                    node.boundary.y_min,
                    node.boundary.y_max,
                )

        else:
            for child in node.children:
                self._print_segment_locations(child)