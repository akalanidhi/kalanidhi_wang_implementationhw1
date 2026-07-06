import pygame


class Button:
    """
    clickable button for the pygame ui. holds its rect, label, color, and
    a callback that fires on click. tracks hover state so it can highlight.
    """

    def __init__(self, x, y, w, h, text, callback):
        """
        sets up the button's position, size, label, and click behavior.
        colors are hardcoded defaults for normal vs. hovered look.
        """
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        self.font = pygame.font.SysFont("Arial", 18)
        self.base_color = (220, 220, 220)
        self.hover_color = (180, 180, 180)
        self.text_color = (0, 0, 0)
        self.hovered = False

    def draw(self, screen):
        """
        draws the button: fills it with hover color if the mouse is over it,
        otherwise base color, outlines it, and centers the label text.
        """
        color = self.hover_color if self.hovered else self.base_color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        """
        updates hover state on mouse movement, and fires the callback if
        a click lands inside the button's rect.
        """
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()