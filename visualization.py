import pygame
"""
SAMPLE IMPLEMENTATION, dont need to follow but helps me keep track of which types of functions will likely exist where
create_window(width, height)
draw_quadtree(screen, node)
draw_segments(screen, segments)
draw_rectangle(screen, rect)
draw_status_bar(screen, text)
draw_point(screen, point)
draw_query(screen, rect)
highlight_node(screen, rect)
update_screen()
"""



def create_window(h: int, title: str = "Pygame Window"):
    """Initialize Pygame and create a window.

    Args:
        width: Window width in pixels.
        height: Window height in pixels.
        title: Title displayed in the window.

    Returns:
        The Pygame display surface.
    """
    pygame.init()
    if (title == "Error screen"):
        screen = pygame.display.set_mode((300,100))
        pygame.display.set_caption(title)
        
        return screen

    screen = pygame.display.set_mode((h, h))
    pygame.display.set_caption(title)

    return screen

def draw_quadtree(screen, node):
    """Draw the quadtree on the given Pygame screen.

    Args:
        screen: The Pygame display surface.
        node: The root node of the quadtree.
    """
    print("draw_quadtree called")  # Debugging statement
    if node is None:
        return