from tkinter import font

import pygame
import sys
from enum import Enum

import parser
import visualization
import quadtree
import geometry
import animation 


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




def load_data(state):
    """
    loads data from "input.txt"
    sets initial h, as well as S
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

    state.screen = visualization.create_window(2 ** h,"Quadtree Visualization")

    # Root boundary
    boundary = geometry.Rectangle(0,2 ** h,0,2 ** h)

    state.tree = quadtree.quadTree(boundary, anim=state.anim)

    # Insert all segments from file
    for segment in SegmentArray:
        state.tree.InsertSegment(segment)
    state.tree.build_endpoint_counts()

def process_initial_commands(state):
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

    if state.mode == Mode.ERROR:
        return

    x, y = event.pos


    if state.mode == Mode.INSERT:

        # First click
        if state.insert_start is None:

            state.insert_start = geometry.Point(x, y)

            print(f"Start point selected: ({x}, {y})")

        # Second click
        else:

            start = state.insert_start

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

            state.query_rect = geometry.Rectangle(xmin,xmax,ymin,ymax)

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

            state.query_rect = geometry.Rectangle(xmin,xmax,ymin,ymax)

            results = state.tree.range_count(state.query_rect)
            print(f"Found {results} endpoints.")

            state.first_click = None


def draw(state):

    screen = state.screen

    screen.fill(WHITE)

    if state.mode == Mode.ERROR:

        visualization.draw_error(
            screen,
            state.error_message
        )

    else:

        # Draw tree
        state.tree.draw(screen)

        state.anim.draw_highlights(screen)

        # Draw query rectangle if one exists
        if state.query_rect is not None:

            visualization.draw_rectangle(
                screen,
                state.query_rect,
                color=(255, 0, 0)
            )

        # Draw status bar
        visualization.draw_status(
            screen,
            mode=state.mode.name,
            animation=state.anim.animation_on,
            nodes=state.tree.count_nodes(),
            segments=state.tree.count_segments()
        )

    pygame.display.flip()

def reset_query_state(state):
    state.query_rect = None
    state.first_click = None
    state.insert_start = None

def update(state):
    state.anim.update() 

def game_loop(state):

    while state.running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                state.running = False

            elif event.type == pygame.KEYDOWN:

                handle_keyboard(event, state)

            elif event.type == pygame.MOUSEBUTTONDOWN:

                handle_mouse(event, state)

        update(state)

        draw(state)



def main():
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