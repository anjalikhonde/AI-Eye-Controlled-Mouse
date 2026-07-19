"""
Loads the MediaPipe FaceLandmarker model and turns a raw BGR frame
into a list of face landmarks (or None if no face is found).
"""

import cv2                                    # used to convert BGR -> RGB before feeding MediaPipe
import mediapipe as mp                        # the face landmark detection library
from mediapipe.tasks import python            # MediaPipe's task API base options
from mediapipe.tasks.python import vision     # MediaPipe's vision task options
from modules import config                    # shared settings (model path)


def load_model():
    """Build and return a ready-to-use FaceLandmarker detector."""
    base_options = python.BaseOptions(
        model_asset_path=config.MODEL_PATH     # point MediaPipe at the .task model file
    )
    options = vision.FaceLandmarkerOptions(
        base_options=base_options,             # pass the base options created above
        running_mode=vision.RunningMode.IMAGE, # we feed single frames, not a video stream
        num_faces=1                            # only track one face at a time
    )
    return vision.FaceLandmarker.create_from_options(options)   # build and return the detector


def get_face_landmarks(detector, frame):
    """Run detection on one frame. Returns a list of landmarks, or None if no face found."""
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)         # MediaPipe expects RGB, OpenCV gives BGR
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)  # wrap the array for MediaPipe
    result = detector.detect(mp_image)                    # run the actual face landmark detection

    if not result.face_landmarks:                         # nobody detected in this frame
        return None                                        # signal "no face" to the caller

    return result.face_landmarks[0]                        # return landmarks for the single tracked face
