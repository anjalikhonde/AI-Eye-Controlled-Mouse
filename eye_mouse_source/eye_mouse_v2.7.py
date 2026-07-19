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
SMOOTHENING = 5
MOVEMENT_THRESHOLD = 10

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# ============================================================
# CONTROL AREA
# ============================================================

LEFT_BOUND = 0.30
RIGHT_BOUND = 0.70

TOP_BOUND = 0.30
BOTTOM_BOUND = 0.70

# ============================================================
# SCREEN SIZE
# ============================================================

screen_width, screen_height = pyautogui.size()

# ============================================================
# GLOBAL VARIABLES
# ============================================================

prev_x = 0
prev_y = 0

eye_closed = False

CLICK_COOLDOWN = 0.5
last_click_time = 0

DOUBLE_BLINK_TIME = 0.5
blink_count = 0
first_blink_time = 0

SCROLL_THRESHOLD = 0.04

scroll_reference = None

SCROLL_COOLDOWN = 0.3
last_scroll_time = 0

fps = 0
frame_count = 0
start_time = time.time()

# ============================================================
# LOAD AI MODEL
# ============================================================

base_options = python.BaseOptions(
    model_asset_path="face_landmarker.task"
)

options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.IMAGE,
    num_faces=1
)

detector = vision.FaceLandmarker.create_from_options(options)

# ============================================================
# OPEN CAMERA
# ============================================================

cam = cv2.VideoCapture(0)

cam.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)


# ============================================================
# DRAW STATUS PANEL
# ============================================================

def draw_status(frame, fps_value, tracking, blink):

    color = (0,255,0) if tracking else (0,0,255)

    cv2.rectangle(frame,(10,10),(250,140),(40,40,40),-1)

    cv2.putText(
        frame,
        f"FPS : {fps_value}",
        (20,35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255,255,255),
        2
    )

    if tracking:

        status = "Tracking"

    else:

        status = "No Face"

    cv2.putText(
        frame,
        f"Status : {status}",
        (20,70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        color,
        2
    )

    if blink:

        cv2.putText(
            frame,
            "Blink : YES",
            (20,105),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0,255,255),
            2
        )

    else:

        cv2.putText(
            frame,
            "Blink : NO",
            (20,105),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255,255,255),
            2
        )


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    success, frame = cam.read()

    if not success:
        break

    frame = cv2.flip(frame,1)

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    result = detector.detect(mp_image)

    tracking = False
    blink = False

    frame_count += 1

    elapsed = time.time() - start_time

    if elapsed >= 1:

        fps = frame_count

        frame_count = 0

        start_time = time.time()

    if result.face_landmarks:

        tracking = True

        face = result.face_landmarks[0]

        h,w,_ = frame.shape

        # ============================================================
        # DRAW CONTROL AREA
        # ============================================================

        left = int(LEFT_BOUND * w)
        right = int(RIGHT_BOUND * w)

        top = int(TOP_BOUND * h)
        bottom = int(BOTTOM_BOUND * h)

        cv2.rectangle(
            frame,
            (left, top),
            (right, bottom),
            (255, 255, 0),
            2
        )

        iris = face[468]
        nose = face[1]

        eye_x = int(iris.x * w)
        eye_y = int(iris.y * h)

        cv2.circle(
            frame,
            (eye_x,eye_y),
            8,
            (0,0,255),
            -1
        )

        # ============================================================
        # BETTER CURSOR MAPPING
        # ============================================================

        mapped_x = (iris.x - LEFT_BOUND) / (RIGHT_BOUND - LEFT_BOUND)
        mapped_y = (iris.y - TOP_BOUND) / (BOTTOM_BOUND - TOP_BOUND)

        mapped_x = max(
            0,
            min(1, mapped_x)
        )

        mapped_y = max(
            0,
            min(1, mapped_y)
        )

        screen_x = mapped_x * screen_width
        screen_y = mapped_y * screen_height

        curr_x = prev_x + (
            screen_x - prev_x
        ) / SMOOTHENING

        curr_y = prev_y + (
            screen_y - prev_y
        ) / SMOOTHENING

        # ============================================================
        # CURSOR STABILIZATION
        # ============================================================

        if (
                abs(curr_x - prev_x) > MOVEMENT_THRESHOLD
                or
                abs(curr_y - prev_y) > MOVEMENT_THRESHOLD
        ):
            pyautogui.moveTo(curr_x, curr_y)

            prev_x = curr_x
            prev_y = curr_y

            # ============================================================
            # HEAD SCROLL CONTROL
            # ============================================================

            if scroll_reference is None:
                scroll_reference = nose.y

            current_time = time.time()

            difference = nose.y - scroll_reference

            if current_time - last_scroll_time > SCROLL_COOLDOWN:

                if difference > SCROLL_THRESHOLD:

                    pyautogui.scroll(-300)

                    last_scroll_time = current_time

                elif difference < -SCROLL_THRESHOLD:

                    pyautogui.scroll(300)

                    last_scroll_time = current_time

        top_eye = face[159]
        bottom_eye = face[145]


        eye_distance=abs(
            top_eye.y -
            bottom_eye.y
        )


        if eye_distance < BLINK_THRESHOLD:

            blink = True

            if not eye_closed:

                current_time = time.time()

                if blink_count == 0:

                    blink_count = 1
                    first_blink_time = current_time

                elif current_time - first_blink_time <= DOUBLE_BLINK_TIME:

                    pyautogui.rightClick()

                    blink_count = 0

                    last_click_time = current_time

                else:

                    blink_count = 1
                    first_blink_time = current_time

                if current_time - last_click_time > CLICK_COOLDOWN:
                    pyautogui.click()

                    last_click_time = current_time

                eye_closed = True

        else:

            eye_closed = False

    draw_status(
        frame,
        fps,
        tracking,
        blink
    )

    cv2.imshow(
        "AI Eye Controlled Mouse",
        frame
    )

    key = cv2.waitKey(1)

    if key == 27:
        break

# ============================================================
# CLEANUP
# ============================================================

cam.release()

cv2.destroyAllWindows()