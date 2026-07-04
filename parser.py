"""
SAMPLE IMPLEMENTATION, dont need to follow but helps me keep track of which types of functions will likely exist where


read_input(file_path)

"""
from geometry import Segment

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
        h = int(next(file).strip())  # Read the first line for grid size
        boundary = (2**h)-1
        init_segments = []
        for line in file:
            split_line = line.strip().split(", ")
            x1, x2, y = map(int, split_line)
            x_min = min(x1, x2)
            x_max = max(x1, x2)
            if x1 < 0 or x2 < 0 or y < 0 or x1 > boundary or x2 > boundary or y > boundary:
                return h, init_segments, True
            init_segments.append(Segment(x_min, x_max, y))
    return h, init_segments, False


def read_user_input(animation_mode, insert_mode, report_mode):
    """
    Reads user input from the console to set the modes.

    Args:
        animation_mode (bool): Current state of animation mode.
        insert_mode (bool): Current state of insert mode.
        report_mode (bool): Current state of report mode.

    Returns:
        animation_mode (bool): Updated state of animation mode.
        insert_mode (bool): Updated state of insert mode.
        report_mode (bool): Updated state of report mode.
        """
    user_input = input("enter command (a/i/r/q): ").strip().lower()
    if user_input == 'a':
        animation_mode = not animation_mode
    elif user_input == 'i':
        insert_mode = not insert_mode
    elif user_input == 'r':
        report_mode = not report_mode
    elif user_input == 'q':
        print("Exiting program.")
        exit(0)
    else:
        print("Invalid input. Please try again.")
    print(f"Animation mode: {'ON' if animation_mode else 'OFF'}, Insert mode: {'ON' if insert_mode else 'OFF'}, Report mode: {'ON' if report_mode else 'OFF'}")
    return animation_mode, insert_mode, report_mode