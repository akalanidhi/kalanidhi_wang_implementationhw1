"""
SAMPLE IMPLEMENTATION, dont need to follow but helps me keep track of which types of functions will likely exist where
main()
load_data()
game_loop()
handle_keyboard(event)
handle_mouse(event)
set_mode(mode)
"""

import pygame
import sys
from enum import Enum

import parser
import visualization
import quadtree
import geometry


WHITE = (255, 255, 255)


class Mode(Enum):
    NORMAL = 0
    INSERT = 1
    REPORT = 2
    ERROR = 3

class GameState:

    def __init__(self):

        self.mode = Mode.NORMAL

        # animation starts ON
        self.animation = True

        self.running = True

        self.screen = None
        self.tree = None

        self.h = 0

        # Used for REPORT mode
        self.first_click = None
        self.query_rect = None

        self.error_message = ""



def load_data(state):

    h, initial_segments, error = parser.read_file("input.txt")

    state.h = h

    if error:

        state.mode = Mode.ERROR
        state.error_message = "Invalid segment coordinates."

        state.screen = visualization.create_window(
            300,
            "Error screen"
        )

        return

    state.screen = visualization.create_window(
        2 ** h,
        "Quadtree Visualization"
    )

    # Root boundary
    boundary = geometry.Rectangle(
        0,
        2 ** h,
        0,
        2 ** h
    )

    state.tree = quadtree.quadTree(boundary)

    # Insert all segments from file
    for segment in initial_segments:
        state.tree.insert(segment)



def handle_keyboard(event, state):

    if event.key == pygame.K_ESCAPE:

        state.mode = Mode.NORMAL

    elif event.key == pygame.K_i:

        state.mode = Mode.INSERT
        print("INSERT MODE")

    elif event.key == pygame.K_r:

        state.mode = Mode.REPORT
        state.first_click = None
        print("REPORT MODE")

    elif event.key == pygame.K_a:

        state.animation = not state.animation

        print(
            f"Animation: {'ON' if state.animation else 'OFF'}"
        )

def handle_mouse(event, state):

    if state.mode == Mode.ERROR:
        return

    x, y = event.pos


    if state.mode == Mode.INSERT:

        segment = geometry.Segment(
            x,
            x,
            y
        )

        state.tree.insert(segment)


    elif state.mode == Mode.REPORT:

        if state.first_click is None:

            state.first_click = geometry.Point(x, y)

        else:

            second = geometry.Point(x, y)

            xmin = min(state.first_click.x, second.x)
            xmax = max(state.first_click.x, second.x)

            ymin = min(state.first_click.y, second.y)
            ymax = max(state.first_click.y, second.y)

            state.query_rect = geometry.Rectangle(
                xmin,
                xmax,
                ymin,
                ymax
            )

            state.tree.query(state.query_rect)

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
            animation=state.animation,
            nodes=state.tree.count_nodes(),
            segments=state.tree.count_segments()
        )

    pygame.display.flip()


def update(state):

    # Placeholder for animation later
    pass

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

    pygame.init()

    state = GameState()

    load_data(state)

    game_loop(state)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()