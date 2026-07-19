import cv2
import mediapipe as mp
import pyautogui
import time

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# ============================================================
# SETTINGS
# ============================================================

BLINK_THRESHOLD = 0.008
CLICK_DELAY = 0.8
SMOOTHENING = 5

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# ============================================================
# SCREEN SIZE
# ============================================================

screen_width, screen_height = pyautogui.size()

# ============================================================
# GLOBAL VARIABLES
# ============================================================

prev_x = 0
prev_y = 0

last_click_time = 0

# ============================================================
# LOAD MODEL
# ============================================================

def load_model():

    base_options = python.BaseOptions(
        model_asset_path="face_landmarker.task"
    )

    options = vision.FaceLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.IMAGE,
        num_faces=1
    )

    return vision.FaceLandmarker.create_from_options(options)


# ============================================================
# OPEN CAMERA
# ============================================================

def open_camera():

    cam = cv2.VideoCapture(0)

    cam.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

    return cam


# ============================================================
# MOVE CURSOR
# ============================================================

def move_cursor(iris):

    global prev_x
    global prev_y

    screen_x = iris.x * screen_width
    screen_y = iris.y * screen_height

    curr_x = prev_x + (
        screen_x - prev_x
    ) / SMOOTHENING

    curr_y = prev_y + (
        screen_y - prev_y
    ) / SMOOTHENING

    pyautogui.moveTo(curr_x, curr_y)

    prev_x = curr_x
    prev_y = curr_y


# ============================================================
# DETECT BLINK
# ============================================================

def detect_blink(face, frame):

    global last_click_time

    top = face[159]
    bottom = face[145]

    eye_distance = abs(
        top.y - bottom.y
    )

    cv2.putText(
        frame,
        f"Eye Distance : {eye_distance:.5f}",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    current_time = time.time()

    if eye_distance < BLINK_THRESHOLD:

        cv2.putText(
            frame,
            "BLINK",
            (20, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

        if current_time - last_click_time > CLICK_DELAY:

            pyautogui.click()

            last_click_time = current_time


# ============================================================
# INITIALIZE
# ============================================================

detector = load_model()
cam = open_camera()

# ============================================================
# PROCESS FRAME
# ============================================================

def process_frame(frame):

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    result = detector.detect(mp_image)

    if result.face_landmarks:

        face = result.face_landmarks[0]

        h, w, _ = frame.shape

        # LEFT IRIS

        iris = face[468]

        eye_x = int(iris.x * w)
        eye_y = int(iris.y * h)

        cv2.circle(
            frame,
            (eye_x, eye_y),
            8,
            (0, 0, 255),
            -1
        )

        move_cursor(iris)

        detect_blink(
            face,
            frame
        )

    return frame


# ============================================================
# MAIN FUNCTION
# ============================================================

def main():

    while True:

        success, frame = cam.read()

        if not success:
            break

        frame = process_frame(frame)

        cv2.imshow(
            "AI Eye Controlled Mouse",
            frame
        )

        key = cv2.waitKey(1)

        if key == ord("q"):
            break

    cam.release()

    cv2.destroyAllWindows()


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":

    main()