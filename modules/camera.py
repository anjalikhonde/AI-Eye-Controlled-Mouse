"""
Thin wrapper around cv2.VideoCapture so main.py doesn't touch cv2 directly.
"""

import cv2                                    # OpenCV, used for camera access and frame flipping
from modules import config                    # shared settings (camera index, resolution, etc.)


def open_camera():
    """Open the webcam and set its resolution. Returns a cv2.VideoCapture object."""
    cam = cv2.VideoCapture(config.CAMERA_INDEX)          # start capturing from the configured camera
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)    # request the configured width
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)  # request the configured height
    return cam                                            # hand the open camera back to the caller


def read_frame(cam):
    """Grab one frame and mirror it so it behaves like a mirror, not a security cam."""
    success, frame = cam.read()               # pull the next frame from the camera
    if not success:                            # camera disconnected or failed to read
        return False, None                     # tell the caller nothing usable came through
    frame = cv2.flip(frame, 1)                 # flip horizontally so movement feels natural
    return True, frame                         # return the mirrored frame
