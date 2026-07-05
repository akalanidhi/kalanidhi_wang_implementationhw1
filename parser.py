from geometry import Segment
from geometry import Rectangle

def read_file(file_path):
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
        init_segments = []
        init_reports = []
        init_queries = []
        for line in file:
            print(line)
            split_line = line.split(" ")
            if split_line[0] == "%":
                log_command(line)
            elif len(split_line) == 1:
                h = int(split_line[0])
                boundary = (2**h)-1
            elif split_line[0] == "i":
                x1, x2, y = int(split_line[1]), int(split_line[2]), int(split_line[3])
                x_min = min(x1, x2)
                x_max = max(x1, x2)
                if x1 < 0 or x2 < 0 or y < 0 or x1 > boundary or x2 > boundary or y > boundary:
                    return h, init_segments, init_reports, init_queries, True
                init_segments.append(Segment(x_min, x_max, y))
            elif split_line[0] == "r":
                x1, y1, x2, y2 = int(split_line[1]), int(split_line[2]), int(split_line[3]), int(split_line[4])
                if x1 < 0 or x2 < 0 or y1 < 0 or y2 < 0 or x1 > boundary or x2 > boundary or y1 > boundary or y2 > boundary:
                    return h, init_segments, init_reports, init_queries, True
                init_reports.append(Rectangle(x1,x2,y1,y2))
            elif split_line[0] == "q":
                x1, y1, x2, y2 = int(split_line[1]), int(split_line[2]), int(split_line[3]), int(split_line[4])
                if x1 < 0 or x2 < 0 or y1 < 0 or y2 < 0 or x1 > boundary or x2 > boundary or y1 > boundary or y2 > boundary:
                    return h, init_segments, init_reports, init_queries, True
                init_queries.append(Rectangle(x1,x2,y1,y2))
    print(f"h = {h}")
    return h, init_segments, init_reports, init_queries, False


def log_command(line):
    with open('log.txt', 'a') as f:
        f.write(line.rstrip() + "\n")

def get_h(file):
    h, _, _, _, _ = read_file(file)
    return h