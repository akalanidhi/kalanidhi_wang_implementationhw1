from tkinter import font

import pygame
import sys
from enum import Enum

import parser
import visualization
import quadtree
import geometry
import animation 
from button import Button


WHITE = (255, 255, 255)


class Mode(Enum):
    NORMAL = 0
    INSERT = 1
    REPORT = 2
    ERROR = 3
    COUNT = 4

class GameState:

    def __init__(self):

        self.mode = Mode.NORMAL

        # animation starts ON
        self.anim = animation.AnimationManager(log_file_path="log.txt")

        self.buttons = []

        self.running = True

        self.screen = None
        self.tree = None

        self.h = 0

        # Used for REPORT mode
        self.first_click = None
        self.query_rect = None

        self.error_message = ""
        
        self.insert_start = None

        self.initial_reports = []
        self.initial_queries = []

        self.world_size = 0
        self.toolbox_width = 220
        self.status_height = 40

        self.query_history = []




def load_data(state):
    """
    Loads data from "input.txt"

    Args: state

    Returns: nothing, but sets initial h, as well as SegmentArray
    """

    h, SegmentArray, initial_reports, initial_queries, error = parser.read_file("input.txt")

    state.h = h
    state.initial_reports = initial_reports
    state.initial_queries = initial_queries

    if error:

        state.mode = Mode.ERROR
        state.error_message = "Invalid segment coordinates."

        state.screen = visualization.create_window(300,"Error screen")

        return

    state.world_size = 2 ** h

    width = state.world_size
    height = state.world_size + state.status_height

    state.screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Quadtree Visualization")    

    # Root boundary
    boundary = geometry.Rectangle(0,2 ** h,0,2 ** h)

    state.tree = quadtree.quadTree(boundary, anim=state.anim)

    def set_insert():
        state.mode = Mode.INSERT
        print("INSERT mode")

    def set_report():
        state.mode = Mode.REPORT
        print("REPORT mode")

    def set_count():
        state.mode = Mode.COUNT
        print("COUNT mode")

    def toggle_anim():
        state.anim.toggle_animation()
        print("Animation toggled")

    y = state.world_size + 5
    btn_w = 120
    btn_h = 25
    gap = 10
    x_start = 20

    state.buttons = [
        Button(x_start, y, btn_w, btn_h, "INSERT", set_insert),
        Button(x_start + (btn_w + gap), y, btn_w, btn_h, "REPORT", set_report),
        Button(x_start + 2 * (btn_w + gap), y, btn_w, btn_h, "COUNT", set_count),
        Button(x_start + 3 * (btn_w + gap), y, btn_w, btn_h, "ANIMATION", toggle_anim),
    ]

    # Insert all segments from file
    for segment in SegmentArray:
        state.tree.InsertSegment(segment)
    state.tree.build_endpoint_counts()

def process_initial_commands(state):
    """
    Processes all intial reports and queries from the input.txt file

    Args: state
    Returns: nothing, but does current reports and queries
    """
    print("Initial reports")
    for rect in state.initial_reports:
        print(f"Report rectangle: {rect}")
        results = state.tree.range_report(rect)
        print(f"Found {len(results)} segments.")

    for rect in state.initial_queries:
        print(f"Query point: ({rect})")
        results = state.tree.range_count(rect)
        print(f"Node contains {results} endpoints.")
    

def handle_keyboard(event, state):
    """
    Takes keyboard inputs and updates to proper mode, clearing rectangles on screen (if needed)
    
    Args: the event detected by pygame, state

    Returns: null
    """

    if event.key == pygame.K_i:
        mode = Mode.INSERT
        print("Switched to INSERT mode.")
        state.mode = Mode.INSERT
        reset_query_state(state)
    if event.key == pygame.K_r:
        mode = Mode.REPORT
        print("Switched to REPORT mode.")
        state.mode = Mode.REPORT
    if event.key == pygame.K_q:
        mode = Mode.COUNT
        print("Switched to COUNT mode.")
        state.mode = Mode.COUNT
    elif event.key == pygame.K_ESCAPE:
        state.mode = Mode.NORMAL
        print("Switched to NORMAL mode")
        mode = Mode.NORMAL
        reset_query_state(state)
    if event.key == pygame.K_a:
        state.anim.toggle_animation()
   
def handle_mouse(event, state):
    """
    Handles mouse to find correct position of mouse when clicked for queries and new segments

    Args: event detected by pygame

    Returns: null
    """

    if state.mode == Mode.ERROR:
        return

    x, y = event.pos

    # ignore status bar clicks
    if not (0 <= x < state.world_size and 0 <= y < state.world_size):
        return


    if state.mode == Mode.INSERT:

        # First click
        if state.insert_start is None:

            state.insert_start = geometry.Point(x, y)

            print(f"Start point selected: ({x}, {y})")

        # Second click
        else:

            start = state.insert_start

            if x<start.x:
                print("ERROR: SEGMENT DOES NOT GO FROM LEFT TO RIGHT")
                state.insert_start = None
                return 
            x1 = min(start.x, x)
            x2 = max(start.x, x)

            segment = geometry.Segment( x1, x2, start.y)

            state.tree.InsertSegment(segment)
            state.tree.build_endpoint_counts()

            print(f"Inserted segment ({x1}, {x2}, {start.y})")

            state.insert_start = None


    elif state.mode == Mode.REPORT:

        if state.first_click is None:

            state.first_click = geometry.Point(x, y)

        else:

            second = geometry.Point(x, y)
           

            xmin = min(state.first_click.x, second.x)
            xmax = max(state.first_click.x, second.x)

            ymin = min(state.first_click.y, second.y)
            ymax = max(state.first_click.y, second.y)
            if xmin != state.first_click.x or ymin == state.first_click.y:
                print("ERROR: RECTANGLE DOES NOT GO FROM BOTTOM LEFT TO TOP RIGHT")
                print(f"{xmin},{ymin},{xmax},{ymax}")
                state.first_click = None
                return

            state.query_rect = geometry.Rectangle(xmin,xmax,ymin,ymax)
            
            
            MAX_HISTORY = 10

            state.query_history.append(state.query_rect)

            if len(state.query_history) > MAX_HISTORY:
                state.query_history.pop(0)  


            results = state.tree.range_report(state.query_rect)
            print(f"Found {len(results)} segments.")

            state.first_click = None


    elif state.mode == Mode.COUNT:

        if state.first_click is None:

            state.first_click = geometry.Point(x, y)

        else:

            second = geometry.Point(x, y)
           
            
            xmin = min(state.first_click.x, second.x)
            xmax = max(state.first_click.x, second.x)

            ymin = min(state.first_click.y, second.y)
            ymax = max(state.first_click.y, second.y)

            if xmin != state.first_click.x or ymin == state.first_click.y:
                print("ERROR: RECTANGLE DOES NOT GO FROM BOTTOM LEFT TO TOP RIGHT")
                print(f"{xmin},{ymin},{xmax},{ymax}")
                state.first_click = None
                return

            state.query_rect = geometry.Rectangle(xmin,xmax,ymin,ymax)


            MAX_HISTORY = 10

            state.query_history.append(state.query_rect)

            if len(state.query_history) > MAX_HISTORY:
                state.query_history.pop(0)  


            results = state.tree.range_count(state.query_rect)
            print(f"Found {results} endpoints.")

            state.first_click = None

    

def draw(state):
    """
    Draws error screen (if input.txt is not correct), status, and query rectangle if in use
    """
    screen = state.screen
    screen.fill(WHITE)

    if state.mode == Mode.ERROR:

        visualization.draw_error(
            screen,
            state.error_message
        )

    else:

        screen.set_clip((0, 0, state.world_size, state.world_size))

        state.tree.draw(screen)
        state.anim.draw_highlights(screen)

        screen.set_clip(None)

        if state.query_rect is not None:
            visualization.draw_rectangle(
                screen,
                state.query_rect,
                color=(255, 0, 0)
            )

        status_y = state.world_size
        button_area_height = 35
        status_text_area_y = state.world_size + button_area_height

        pygame.draw.rect(
            screen,
            (230, 230, 230),
            (0, state.world_size, state.world_size, state.status_height)
        )

        pygame.draw.line(
            screen,
            (0, 0, 0),
            (0, status_y),
            (state.world_size, status_y),
            2
        )

        visualization.draw_status(
            screen,
            mode=state.mode.name,
            animation=state.anim.animation_on,
            nodes=state.tree.count_nodes(),
            segments=state.tree.count_segments()
        )

    for button in state.buttons:
        button.draw(screen)
    
    for rect in state.query_history:
        visualization.draw_rectangle(
        screen,
        rect,
        color=(200, 200, 200)
    )

    pygame.display.flip()

def reset_query_state(state):
    """
    Helper function to clear any rectangle on screen for when in normal or insert  mode
    
    Args: state

    Returns: null
    """
    state.query_rect = None
    state.first_click = None
    state.insert_start = None

def update(state):
    """
    Helper function to update the state when needed
    
    Args: state

    Returns: null
    """
    state.anim.update() 

def game_loop(state):
    """
    Keeps the game state updated, watching for events such as quit, key presses, or mouse clicks 
    
    Args: state

    Returns: null
    """

    while state.running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                state.running = False
            
            for button in state.buttons:
                button.handle_event(event)

            if event.type == pygame.KEYDOWN:

                handle_keyboard(event, state)

            elif event.type == pygame.MOUSEBUTTONDOWN:

                handle_mouse(event, state)

        update(state)

        draw(state)



def main():
    """
    Main function. Opens file, creates the state, loads the data, and loops the state
    
    Args: N/A

    Returns: null
    """
    with open("log.txt",'w') as file:
        pass
    pygame.init()

    state = GameState()

    load_data(state)

    process_initial_commands(state)
    
    game_loop(state)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()