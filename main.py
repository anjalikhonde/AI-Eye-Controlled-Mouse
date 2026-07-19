"""
AI Eye Controlled Mouse
------------------------
Move the cursor with your iris, left-click with a single blink,
right-click with a double blink, and scroll by tilting your head.

Run with:  python main.py
Quit with: ESC key
"""

import time                                    # used for FPS calculation
import cv2                                      # used for the webcam preview window and key handling

from modules import config                       # shared settings
from modules import camera                       # webcam open/read helpers
from modules import face_tracker                  # MediaPipe model loading and detection
from modules import ui_overlay                     # drawing helpers (status panel, control box, iris dot)
from modules.cursor_controller import CursorController  # turns iris position into cursor movement
from modules.blink_detector import BlinkDetector          # turns blinks into clicks
from modules.scroll_controller import ScrollController     # turns head tilt into scrolling


class FPSCounter:
    """Small helper that reports frames-per-second once per second."""

    def __init__(self):
        self.fps = 0                             # last computed FPS value
        self.frame_count = 0                      # frames seen since the last FPS update
        self.start_time = time.time()             # when the current 1-second window started

    def tick(self):
        """Call once per frame. Updates and returns the current FPS value."""
        self.frame_count += 1                      # count this frame
        elapsed = time.time() - self.start_time      # how long the current window has been open
        if elapsed >= 1:                              # a full second has passed
            self.fps = self.frame_count                # freeze the count as this second's FPS
            self.frame_count = 0                         # reset for the next window
            self.start_time = time.time()                 # restart the window clock
        return self.fps                                   # hand back the most recent FPS value


def process_frame(frame, detector, cursor, blink_detector, scroll_controller, fps_counter):
    """Run detection + controls on a single frame and draw the overlay. Returns the annotated frame."""
    face = face_tracker.get_face_landmarks(detector, frame)  # try to find a face in this frame
    tracking = face is not None                                # whether a face was found
    blink = False                                              # default blink state for this frame

    if tracking:                                               # only act if we actually see a face
        iris = face[config.IRIS_LANDMARK]                        # iris landmark drives the cursor
        nose = face[config.NOSE_LANDMARK]                         # nose landmark drives scrolling

        ui_overlay.draw_control_area(frame)                        # show the active control box
        ui_overlay.draw_iris_marker(frame, iris)                    # show the tracked iris point

        cursor.move(iris)                                            # move the OS cursor toward the iris
        scroll_controller.update(nose)                                # check for head-tilt scrolling
        blink = blink_detector.update(face)                            # check for blink-based clicks

    fps_value = fps_counter.tick()                                  # update and read the current FPS
    ui_overlay.draw_status(frame, fps_value, tracking, blink)          # draw the status panel

    return frame                                                       # annotated frame, ready to display


def main():
    """Set everything up, run the capture loop, and clean up on exit."""
    detector = face_tracker.load_model()          # load the MediaPipe face landmark model once
    cam = camera.open_camera()                     # open the webcam once

    cursor = CursorController()                     # tracks and smooths cursor position across frames
    blink_detector = BlinkDetector()                  # tracks eyelid state across frames
    scroll_controller = ScrollController()              # tracks head-tilt baseline across frames
    fps_counter = FPSCounter()                            # tracks frame timing across frames

    while True:                                             # main capture loop
        success, frame = camera.read_frame(cam)              # grab the next mirrored frame
        if not success:                                        # camera failed / disconnected
            break                                               # stop the loop cleanly

        frame = process_frame(
            frame, detector, cursor, blink_detector, scroll_controller, fps_counter
        )                                                        # run detection, controls, and drawing

        cv2.imshow(config.WINDOW_NAME, frame)                     # show the annotated frame

        key = cv2.waitKey(1)                                        # poll for a keypress, 1ms wait
        if key == 27:                                                 # 27 = ESC key
            break                                                      # exit the loop on ESC

    cam.release()                                                        # release the webcam
    cv2.destroyAllWindows()                                                # close the preview window


if __name__ == "__main__":                          # only run if this file is executed directly
    main()                                            # kick off the program
