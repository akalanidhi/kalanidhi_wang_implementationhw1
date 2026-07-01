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

animation_MODE = False
insert_MODE = False
report_MODE = False
error_MODE = False

h, initial_segments, error_MODE = parser.read_input("input.txt")
if error_MODE:
    screen = visualization.create_window(h, "Error screen")
    screen.fill((255, 255, 255))  # Fill the background with white
    TXTCOLOR = (255, 0, 0)  # Red color for error text
    font = pygame.font.Font(None, 20)
    text_surface = font.render("Error: Invalid segment coordinates!", True, TXTCOLOR)
    text_rect = text_surface.get_rect(center=(150, 50))  # Center the text
    screen.blit(text_surface, text_rect)  # Draw the text on the screen
    # Update the full display Surface to the screen
else:
    screen = visualization.create_window(2**h, "Quadtree Visualization")
    screen.fill((255, 255, 255))  # Fill the background with white


running = True
while running:
    # Look at all incoming operating system events
    for event in pygame.event.get():
        # If the user clicks the window's 'X' button, break the loop
        if event.type == pygame.QUIT:
            running = False
        
    pygame.display.flip()
    
    

pygame.quit()
sys.exit()