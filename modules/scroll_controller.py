"""
Uses up/down nose movement (tilting the head) to trigger page scrolling.
"""

import time                                   # used for the scroll cooldown timer
import pyautogui                              # used to actually send scroll events
from modules import config                    # shared settings (thresholds, cooldown, amount)


class ScrollController:
    """Tracks a reference nose position and scrolls when the head tilts away from it."""

    def __init__(self):
        self.reference_y = None                # nose y-position we compare against (set on first frame)
        self.last_scroll_time = 0               # timestamp of the last scroll event (for cooldown)

    def update(self, nose):
        """Call once per frame with the nose landmark. Scrolls the page if the head tilted enough."""
        if self.reference_y is None:            # first frame we've seen a face, set the baseline
            self.reference_y = nose.y            # remember the neutral head position
            return                               # nothing to scroll on this very first frame

        current_time = time.time()               # timestamp for cooldown comparison
        if current_time - self.last_scroll_time <= config.SCROLL_COOLDOWN:  # still cooling down
            return                               # skip this frame, too soon since last scroll

        difference = nose.y - self.reference_y    # positive = head tilted down, negative = tilted up

        if difference > config.SCROLL_THRESHOLD:   # head tilted down past the threshold
            pyautogui.scroll(-config.SCROLL_AMOUNT)  # negative scroll = move the page down
            self.last_scroll_time = current_time      # restart the cooldown
        elif difference < -config.SCROLL_THRESHOLD:  # head tilted up past the threshold
            pyautogui.scroll(config.SCROLL_AMOUNT)     # positive scroll = move the page up
            self.last_scroll_time = current_time       # restart the cooldown

    def reset_reference(self):
        """Call this if you want the next frame to redefine 'neutral' head position."""
        self.reference_y = None                  # forces update() to re-baseline next call
