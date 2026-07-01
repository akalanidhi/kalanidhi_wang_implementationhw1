"""
SAMPLE IMPLEMENTATION, dont need to follow but helps me keep track of which types of functions will likely exist where


read_input(file_path)

"""

def read_input(file_path):
    """
    Parses the input file and returns a list of segments.

    Args:
        file_path (str): The path to the input file.

    Returns:
        h, initial_segments, screen, error_mode
        h: size of the grid, 2^Hx2^H
        initial_segments: list of segments, each segment is a tuple (x1, x2, y)
        error_mode: True if there was an error in the input file, False otherwise
    """
    with open(file_path, "r", encoding="utf-8") as file:
        h = int(next(file).strip())  # Read the first line for grid size
        boundary = (2**h)-1
        init_segments = []
        for line in file:
            split_line = line.strip().split(", ")
            x1, x2, y = map(int, split_line)
            if x1 < 0 or x2 < 0 or y < 0 or x1 > boundary or x2 > boundary or y > boundary:
                return h, init_segments, True
            init_segments.append((x1, x2, y))
    return h, init_segments, False