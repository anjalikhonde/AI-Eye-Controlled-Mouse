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

eye_closed = False

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

        iris = face[468]

        eye_x = int(iris.x * w)
        eye_y = int(iris.y * h)

        cv2.circle(
            frame,
            (eye_x,eye_y),
            8,
            (0,0,255),
            -1
        )

        screen_x = iris.x * screen_width
        screen_y = iris.y * screen_height

        curr_x = prev_x + (
            screen_x - prev_x
        ) / SMOOTHENING

        curr_y = prev_y + (
            screen_y - prev_y
        ) / SMOOTHENING

        pyautogui.moveTo(curr_x,curr_y)

        prev_x = curr_x
        prev_y = curr_y

        top_eye = face[159]
        bottom_eye = face[145]


        eye_distance=abs(
            top_eye.y -
            bottom_eye.y
        )

        print(eye_distance)

        if eye_distance < BLINK_THRESHOLD:

            blink = True

            if not eye_closed:
                print("BLINK DETECTED")

                pyautogui.click()

                print("CLICK SENT")

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