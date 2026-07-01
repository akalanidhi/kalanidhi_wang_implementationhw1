import pygame
import sys
import parser as parser
import visualization as visualization

"""
SAMPLE IMPLEMENTATION, dont need to follow but helps me keep track of which types of functions will likely exist where
main()
load_data()
game_loop()
handle_keyboard(event)
handle_mouse(event)
set_mode(mode)
"""
h, initial_segments = parser.parse("input.txt")

screen = visualization.create_window(2**h, "Quadtree Visualization")

running = True
while running:
    # Look at all incoming operating system events
    for event in pygame.event.get():
        # If the user clicks the window's 'X' button, break the loop
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255,255,255))

    # Update the full display Surface to the screen
    pygame.display.flip()

pygame.quit()
sys.exit()