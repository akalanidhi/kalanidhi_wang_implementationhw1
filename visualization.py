import pygame

"""
sample functions i should probably make
create_window(width, height)
draw_quadtree(screen, node)
draw_segments(screen, segments)
draw_query_rectangle(screen, rect)
draw_status_bar(screen, text)
highlight_node(screen, rect)
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

    screen = pygame.display.set_mode((h, h))
    pygame.display.set_caption(title)

    return screen
