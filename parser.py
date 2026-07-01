def parse(file_path):
    """
    Parses the input file and returns a list of segments.

    Args:
        file_path (str): The path to the input file.

    Returns:
        h, initial_segments
        h: size of the grid, 2^Hx2^H
        initial_segments: list of segments, each segment is a tuple (x1, x2, y)
    """
    with open(file_path, "r", encoding="utf-8") as file:
        h = int(next(file).strip())  # Read the first line for grid size
        init_segments = []
        for line in file:
            split_line = line.strip().split(", ")
            x1, x2, y = map(int, split_line)
            init_segments.append((x1, x2, y))

    return h, init_segments
