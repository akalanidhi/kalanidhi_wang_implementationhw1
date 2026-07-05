#new file

"""
includes:
    - animation on/off toggle
    - PrintAndHighlightQuadrant: logs + queues a visited node's region to blink

Usage:
    from animation import AnimationManager
    anim = AnimationManager(log_file_path="log.txt")

    # 'a' key handler
    anim.toggle_animation()

    # inside insert/report/count, every time you visit a node v with
    # region R(v) = LL(x1,y1), UR(x2,y2):
    anim.print_and_highlight_quadrant(x1, y1, x2, y2)

    # once per frame, after drawing the tree/segments normally:
    anim.update()
    anim.draw_highlights(screen)
"""

import pygame

VISIBLE_MIN = 0
VISIBLE_MAX = 511
HIGHLIGHT_FRAMES = 300
HIGHLIGHT_COLOR = (255, 215, 0)


class AnimationManager:
    def __init__(self, log_file_path="log.txt"):
        self.animation_on = True  # spec: must start ON
        self._log_file = open(log_file_path, "a")
        self._highlighted_quads = []  # list of {x1,y1,x2,y2,frames_left}

    def close(self):
        self._log_file.close()

    def toggle_animation(self):
        self.animation_on = not self.animation_on

    def print_and_highlight_quadrant(self, x1, y1, x2, y2):
        """
        If animation is OFF: no-op.
        If ON: log the visit, and if the quad is on-screen, queue it to
        blink for a few frames.
        """
        if not self.animation_on:
            return

        self._log_file.write(
            f"A quadrant with LL=({x1}, {y1}) and UR=({x2}, {y2}) was called\n"
        )
        self._log_file.flush()

        if not (x2 < VISIBLE_MIN or x1 > VISIBLE_MAX or
                y2 < VISIBLE_MIN or y1 > VISIBLE_MAX):
            self._highlighted_quads.append({
                "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                "frames_left": HIGHLIGHT_FRAMES,
            })

    def update(self):
        """Call once per frame to age out expired highlights."""
        for q in self._highlighted_quads:
            q["frames_left"] -= 1
        self._highlighted_quads = [q for q in self._highlighted_quads if q["frames_left"] > 0]

    def draw_highlights(self, screen):
        """Draw all currently-highlighted quadrants. Call after your normal draw()."""
        if not self.animation_on:
            return

        h = screen.get_size()[1]
        for q in self._highlighted_quads:
            cx1, cy1 = max(q["x1"], VISIBLE_MIN), max(q["y1"], VISIBLE_MIN)
            cx2, cy2 = min(q["x2"], VISIBLE_MAX), min(q["y2"], VISIBLE_MAX)
            if cx2 < cx1 or cy2 < cy1:
                continue
            rect_w = cx2 - cx1
            rect_h = cy2 - cy1
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, (cx1, cy1, rect_w, rect_h), width=2)


    def clear_highlights(self):
        """Clear all currently-highlighted quadrants. Call at the start of each frame."""
        self._highlighted_quads.clear()