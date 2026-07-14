import cv2
import mediapipe as mp
import pyautogui

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Get screen size
screen_width, screen_height = pyautogui.size()

# Load Face Landmarker model
base_options = python.BaseOptions(
    model_asset_path="face_landmarker.task"
)

options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.IMAGE,
    num_faces=1
)

# Create detector
detector = vision.FaceLandmarker.create_from_options(options)

# Open webcam
cam = cv2.VideoCapture(0)

while True:

    ret, frame = cam.read()

    if not ret:
        break

    # Mirror the camera
    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    result = detector.detect(mp_image)

    if result.face_landmarks:

        face = result.face_landmarks[0]

        iris = face[468]

        h, w, _ = frame.shape

        x = int(iris.x * w)
        y = int(iris.y * h)

        cv2.circle(frame, (x, y), 8, (0, 255, 0), -1)

        # Convert eye position to screen position
        screen_x = int(iris.x * screen_width)
        screen_y = int(iris.y * screen_height)

        # Move mouse
        pyautogui.moveTo(screen_x, screen_y)

    cv2.imshow("Eye Controlled Mouse", frame)

    if cv2.waitKey(1) == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()