"""
SAMPLE IMPLEMENTATION, dont need to follow but helps me keep track of which types of functions will likely exist where


read_input(file_path)

"""
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



"""
    if event.key == pygame.K_RETURN:

        cmd = command.strip()
        command = ""

        if cmd == "":
            return

        cmd_str = cmd.split()
        for i in range(1, len(cmd_str)):
            cmd_str[i] = cmd_str[i].strip()
            if int(cmd_str[i]) < 0 or int(cmd_str[i]) > 2 ** state.h:
                print("Error: Values are out of bounds.")
                return
        try:
            if cmd_str[0].lower() == "i":

                if len(cmd_str) != 4:
                    print("Usage: i x1 x2 y")
                    return

                x1 = int(cmd_str[1])
                x2 = int(cmd_str[2])
                y = int(cmd_str[3])

                segment = geometry.Segment(
                    min(x1, x2),
                    max(x1, x2),
                    y
                )
                state.anim.clear_highlights()  # Clear highlights before inserting a new segment
                state.tree.insert(segment)

                print(f"Inserted segment ({x1}, {x2}, {y})")

            elif cmd_str[0].lower() == "r":

                if len(cmd_str) != 5:
                    print("Usage: r xmin ymin xmax ymax")
                    return

                xmin = int(cmd_str[1])
                ymin = int(cmd_str[2])
                xmax = int(cmd_str[3])
                ymax = int(cmd_str[4])

                state.anim.clear_highlights()  # Clear highlights before performing a new query
                state.query_rect = geometry.Rectangle(xmin,xmax,ymin,ymax)

                results = state.tree.query(state.query_rect)

                print(f"Found {len(results)} segments.")
            elif cmd_str[0].lower() == "c":

                print("Nodes:", state.tree.count_nodes())
                print("Segments:", state.tree.count_segments())

            else:
                print("Unknown command.")

        except ValueError:
            print("Invalid numeric input.")
    elif event.key == pygame.K_BACKSPACE:

        command = command[:-1]
    elif event.key == pygame.K_ESCAPE:

        state.mode = Mode.NORMAL
    elif event.key == pygame.K_a:

        state.anim.toggle_animation()

        print(
            f"Animation: {'ON' if state.anim.animation_on else 'OFF'}"
        )
    else:

        if event.unicode.isprintable():
            command += event.unicode
"""
