"""
All the cv2.putText / cv2.rectangle calls live here, so main.py stays
focused on logic instead of drawing code.
"""

import cv2                                    # used for all drawing calls
from modules import config                    # shared settings (bounds, used for the control box)


def draw_control_area(frame):
    """Draw the rectangle showing where iris movement actually controls the cursor."""
    h, w, _ = frame.shape                      # need frame size to convert normalized bounds to pixels
    left = int(config.LEFT_BOUND * w)           # left edge in pixels
    right = int(config.RIGHT_BOUND * w)          # right edge in pixels
    top = int(config.TOP_BOUND * h)               # top edge in pixels
    bottom = int(config.BOTTOM_BOUND * h)          # bottom edge in pixels
    cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 0), 2)  # cyan box, 2px thick


def draw_iris_marker(frame, iris):
    """Draw a red dot on the tracked iris position."""
    h, w, _ = frame.shape                       # need frame size to convert normalized -> pixels
    eye_x = int(iris.x * w)                       # iris x in pixels
    eye_y = int(iris.y * h)                        # iris y in pixels
    cv2.circle(frame, (eye_x, eye_y), 8, (0, 0, 255), -1)  # solid red dot, 8px radius


def draw_status(frame, fps_value, tracking, blink):
    """Draw the FPS / tracking status / blink status panel in the top-left corner."""
    cv2.rectangle(frame, (10, 10), (260, 145), (40, 40, 40), -1)  # dark background panel

    cv2.putText(
        frame, f"FPS : {fps_value}", (20, 35),           # FPS counter line
        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2  # white text
    )

    tracking_color = (0, 255, 0) if tracking else (0, 0, 255)  # green if tracking, red if not
    tracking_text = "Tracking" if tracking else "No Face"       # human-readable status
    cv2.putText(
        frame, f"Status : {tracking_text}", (20, 70),      # tracking status line
        cv2.FONT_HERSHEY_SIMPLEX, 0.6, tracking_color, 2     # colored to match state
    )

    blink_color = (0, 255, 255) if blink else (255, 255, 255)  # yellow if blinking, white otherwise
    blink_text = "YES" if blink else "NO"                        # human-readable blink flag
    cv2.putText(
        frame, f"Blink : {blink_text}", (20, 105),           # blink status line
        cv2.FONT_HERSHEY_SIMPLEX, 0.6, blink_color, 2          # colored to match state
    )
