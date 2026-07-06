import pygame
import parser

VISIBLE_MIN = 0
HIGHLIGHT_FRAMES = 1000
HIGHLIGHT_COLOR = (255, 215, 0) #highlighting color for quads

HIGHLIGHT_COLOR = (255, 215, 0)
SEGMENT_HIGHLIGHT_COLOR = (255, 0, 0)          # ighlighting color for segments
SEGMENT_HIGHLIGHT_WIDTH = 4                     #thicker line so a segment is easy to spot


class AnimationManager:
    def __init__(self, log_file_path="log.txt"):
        """ Initializes the animation manager, handling all highlights of nodes and segments
    
        Args: 
        log_file_path: where outputs are being written to
        """
        self.animation_on = True  # spec: must start ON
        self._log_file = open(log_file_path, "a")
        self._highlighted_quads = []  # list of {x1,y1,x2,y2,frames_left}
        self._highlighted_segments = []
        self.h = (2 ** (parser.get_h("input.txt"))) - 1

    def close(self):
        """
        Helper function that closes whichever file is open and being written to
        """
        self._log_file.close()

    def toggle_animation(self):
        """Helper function that toggles animation mode
        """
        self.animation_on = not self.animation_on

    def print_and_highlight_quadrant(self, x1, y1, x2, y2):
        """
        If animation is OFF: no-op.
        If ON: log the visit, and if the quad is on-screen, queue it to
        blink for a few frames.

        Args:
        x1, x2, y1, y2: dimensions of quadrant box being called upon
        """
        if not self.animation_on:
            return

        self._log_file.write(
            f"A quadrant with LL=({x1}, {y1}) and UR=({x2}, {y2}) was called\n"
        )
        self._log_file.flush()

        if not (x2 < VISIBLE_MIN or x1 > self.h or
                y2 < VISIBLE_MIN or y1 > self.h):
            self._highlighted_quads.append({
                "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                "frames_left": HIGHLIGHT_FRAMES,
            })

    def highlight_segment(self, segment): 
        """
        If animation is OFF: no-op.
        If ON: queue this segment to blink for HIGHLIGHT_FRAMES frames.
        
        Args: segment to be highlighted (if animation mode is on)
        """
        if not self.animation_on:
            return
        self._highlighted_segments.append({
            "x1": segment.x1, "x2": segment.x2, "y": segment.y,
            "frames_left": HIGHLIGHT_FRAMES,
        })

    def update(self):
        """Call once per frame to age out expired highlights."""
        for q in self._highlighted_quads:
            q["frames_left"] -= 1
        self._highlighted_quads = [q for q in self._highlighted_quads if q["frames_left"] > 0]

        for s in self._highlighted_segments:      #age out expired segment highlights
            s["frames_left"] -= 1
        self._highlighted_segments = [s for s in self._highlighted_segments if s["frames_left"] > 0]

    def draw_highlights(self, screen):
        """Draw all currently-highlighted quadrants. Call after your normal draw()."""
        if not self.animation_on:
            return

        h = screen.get_size()[1]
        for q in self._highlighted_quads:
            cx1, cy1 = max(q["x1"], VISIBLE_MIN), max(q["y1"], VISIBLE_MIN)
            cx2, cy2 = min(q["x2"], self.h), min(q["y2"], self.h)
            if cx2 < cx1 or cy2 < cy1:
                continue
            rect_w = cx2 - cx1
            rect_h = cy2 - cy1
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, (cx1, cy1, rect_w, rect_h), width=2)

        for s in self._highlighted_segments:       #draw blinking segments on top of everything else
            sx1, sx2 = max(s["x1"], VISIBLE_MIN), min(s["x2"], self.h)
            sy = s["y"]
            if sx2 < sx1 or sy < VISIBLE_MIN or sy > self.h:
                continue
            pygame.draw.line(
                screen, SEGMENT_HIGHLIGHT_COLOR,
                (sx1, sy), (sx2, sy),
                SEGMENT_HIGHLIGHT_WIDTH
            )


    def clear_highlights(self):
        """Clear all currently-highlighted quadrants and segments. Call at the start of each frame."""
        self._highlighted_quads.clear()
        self._highlighted_segments.clear()