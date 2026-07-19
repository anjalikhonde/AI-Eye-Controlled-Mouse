"""
Central place for every tunable value used across the app.
Change numbers here instead of hunting through the other files.
"""

# ---------- MODEL ----------
MODEL_PATH = "face_landmarker.task"          # path to the MediaPipe face landmark model file

# ---------- CAMERA ----------
CAMERA_INDEX = 0                              # which webcam to open (0 = default)
CAMERA_WIDTH = 640                            # capture width in pixels
CAMERA_HEIGHT = 480                           # capture height in pixels

# ---------- LANDMARK INDICES ----------
IRIS_LANDMARK = 468                           # index of the left-eye iris center point
NOSE_LANDMARK = 1                             # index of the nose tip, used for head-scroll
TOP_EYELID_LANDMARK = 159                     # index of the upper eyelid point (blink math)
BOTTOM_EYELID_LANDMARK = 145                  # index of the lower eyelid point (blink math)

# ---------- CURSOR MAPPING ----------
LEFT_BOUND = 0.30                             # left edge of the "active" eye-movement box (0-1 normalized)
RIGHT_BOUND = 0.70                            # right edge of the active box
TOP_BOUND = 0.30                              # top edge of the active box
BOTTOM_BOUND = 0.70                           # bottom edge of the active box
SMOOTHENING = 5                               # higher = smoother but laggier cursor motion
MOVEMENT_THRESHOLD = 10                       # ignore cursor jitter smaller than this many pixels

# ---------- BLINK / CLICK ----------
BLINK_THRESHOLD = 0.008                       # eyelid gap below this counts as "eye closed"
CLICK_COOLDOWN = 0.5                          # seconds to wait before allowing another click
DOUBLE_BLINK_TIME = 0.5                       # max seconds between two blinks to count as a double-blink

# ---------- HEAD SCROLL ----------
SCROLL_THRESHOLD = 0.04                       # how far the nose must move (normalized) to trigger a scroll
SCROLL_COOLDOWN = 0.3                         # seconds between scroll events
SCROLL_AMOUNT = 300                           # pyautogui scroll units per trigger

# ---------- UI ----------
WINDOW_NAME = "AI Eye Controlled Mouse"       # title of the OpenCV preview window
