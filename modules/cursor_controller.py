"""
Turns the iris landmark position into smoothed on-screen cursor movement.
"""

import pyautogui                              # used to actually move the OS mouse cursor
from modules import config                    # shared settings (bounds, smoothing, thresholds)

pyautogui.FAILSAFE = False                    # don't abort if the cursor hits a screen corner


class CursorController:
    """Keeps track of the previous cursor position and moves it smoothly toward the target."""

    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()  # get the real screen resolution
        self.prev_x = self.screen_width / 2    # start the cursor tracking at screen center
        self.prev_y = self.screen_height / 2   # (avoids a jump from (0,0) on the first frame)

    def _map_to_screen(self, iris):
        """Map the iris's normalized position (within the active box) to 0-1 screen space."""
        mapped_x = (iris.x - config.LEFT_BOUND) / (config.RIGHT_BOUND - config.LEFT_BOUND)  # x within box
        mapped_y = (iris.y - config.TOP_BOUND) / (config.BOTTOM_BOUND - config.TOP_BOUND)   # y within box
        mapped_x = max(0, min(1, mapped_x))    # clamp so we never leave the screen on the left/right
        mapped_y = max(0, min(1, mapped_y))    # clamp so we never leave the screen on top/bottom
        return mapped_x, mapped_y              # both values are now safely between 0 and 1

    def move(self, iris):
        """Move the OS cursor toward the iris position, smoothed and jitter-filtered."""
        mapped_x, mapped_y = self._map_to_screen(iris)         # get 0-1 normalized target position

        target_x = mapped_x * self.screen_width                # convert to actual screen pixels
        target_y = mapped_y * self.screen_height                # convert to actual screen pixels

        curr_x = self.prev_x + (target_x - self.prev_x) / config.SMOOTHENING  # ease toward target
        curr_y = self.prev_y + (target_y - self.prev_y) / config.SMOOTHENING  # ease toward target

        moved_enough = (
            abs(curr_x - self.prev_x) > config.MOVEMENT_THRESHOLD  # x moved more than the jitter floor
            or abs(curr_y - self.prev_y) > config.MOVEMENT_THRESHOLD  # or y moved more than the jitter floor
        )

        if moved_enough:                        # only actually move the mouse if it's a real motion
            pyautogui.moveTo(curr_x, curr_y)     # send the cursor to the new smoothed position
            self.prev_x = curr_x                 # remember this position for next frame's smoothing
            self.prev_y = curr_y                 # remember this position for next frame's smoothing
