"""
Watches the gap between the upper and lower eyelid to detect blinks,
and turns blinks into left-clicks (single blink) or right-clicks (double blink).
"""

import time                                   # used for cooldown and double-blink timing
import pyautogui                              # used to actually send the click events
from modules import config                    # shared settings (thresholds, cooldowns)


class BlinkDetector:
    """Tracks eyelid state across frames and fires mouse clicks on blinks."""

    def __init__(self):
        self.eye_closed = False                # whether the eye was closed on the previous frame
        self.last_click_time = 0                # timestamp of the most recent click (for cooldown)
        self.blink_count = 0                    # how many blinks seen so far in the current pair
        self.first_blink_time = 0               # timestamp of the first blink in a potential pair

    @staticmethod
    def _eye_distance(face):
        """Vertical gap between the top and bottom eyelid landmarks."""
        top_eye = face[config.TOP_EYELID_LANDMARK]        # upper eyelid landmark
        bottom_eye = face[config.BOTTOM_EYELID_LANDMARK]   # lower eyelid landmark
        return abs(top_eye.y - bottom_eye.y)                # smaller = eye more closed

    def update(self, face):
        """Call once per frame. Returns True if the eye is currently detected as closed."""
        eye_distance = self._eye_distance(face)             # measure how open the eye currently is

        if eye_distance >= config.BLINK_THRESHOLD:           # eye is open
            self.eye_closed = False                          # reset state so the next closing re-triggers
            return False                                     # nothing to report this frame

        # From here on, the eye is closed.
        if self.eye_closed:                                  # already counted this closure last frame
            return True                                      # still closed, but don't fire again

        self.eye_closed = True                                # mark that we've now registered this closure
        self._handle_new_blink()                              # decide single vs double blink and click
        return True                                            # report the closed state to the caller

    def _handle_new_blink(self):
        """Called exactly once per fresh blink. Decides click type based on timing."""
        current_time = time.time()                            # timestamp of this blink

        if self.blink_count == 0:                              # this is the first blink of a potential pair
            self.blink_count = 1                                # start counting
            self.first_blink_time = current_time                # remember when the pair started
        elif current_time - self.first_blink_time <= config.DOUBLE_BLINK_TIME:  # second blink, in time
            pyautogui.rightClick()                               # fire a right-click for the double-blink
            self.blink_count = 0                                 # reset the pair counter
            self.last_click_time = current_time                  # start the cooldown from here
            return                                                # don't also fire a left-click below
        else:                                                    # too slow to count as a pair, restart
            self.blink_count = 1                                  # treat this blink as a fresh "first"
            self.first_blink_time = current_time                  # remember its timestamp

        if current_time - self.last_click_time > config.CLICK_COOLDOWN:  # cooldown has elapsed
            pyautogui.click()                                     # fire a normal left-click
            self.last_click_time = current_time                   # restart the cooldown timer
