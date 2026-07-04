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

    screen = pygame.display.set_mode((h, h+30))
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
    
STATUS_HEIGHT = 30


def draw_status(screen, mode, animation, nodes, segments):
    """
    Draws the status bar at the bottom of the window.

    Args:
        screen: Pygame display surface.
        mode: Current mode (string or Mode enum).
        animation: True if animation is enabled.
        nodes: Total number of nodes in the quadtree.
        segments: Total number of stored segments.
    """

    width = screen.get_width()
    height = screen.get_height()

    # Background
    pygame.draw.rect(
        screen,
        (230, 230, 230),
        (0, height - STATUS_HEIGHT, width, STATUS_HEIGHT)
    )

    # Top border
    pygame.draw.line(
        screen,
        (150, 150, 150),
        (0, height - STATUS_HEIGHT),
        (width, height - STATUS_HEIGHT),
        1
    )

    font = pygame.font.Font(None, 24)

    if not isinstance(mode, str):
        mode = mode.name

    animation_text = "ON" if animation else "OFF"

    status = (
        f"Mode: {mode}    "
        f"Animation: {animation_text}    "
        f"Nodes: {nodes}    "
        f"Segments: {segments}"
    )

    text = font.render(status, True, (0, 0, 0))

    screen.blit(text, (10, height - STATUS_HEIGHT + 6))


def draw_error(screen, message):
    """
    Draws an error message on the screen.

    Args:
        screen: Pygame display surface.
        message: Error message to display.
    """
    width = screen.get_width()
    height = screen.get_height()

    # Background
    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (0, 0, width, height)
    )

    font = pygame.font.Font(None, 30)
    text = font.render(message, True, (255, 0, 0))

    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)