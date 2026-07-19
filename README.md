# AI Eye Controlled Mouse

Control your mouse cursor with your eyes using real-time face landmark tracking.
Move the cursor with your iris, left-click with a single blink, right-click with
a double blink, and scroll by tilting your head.

## Features
- **Cursor movement** — tracked via iris position (MediaPipe FaceLandmarker)
- **Left-click** — single blink
- **Right-click** — double blink (within 0.5s)
- **Scroll** — tilt your head up/down
- **Smoothed motion** — jitter filtering + exponential smoothing for stable control
- **Live status overlay** — FPS, tracking state, blink state

## Tech Stack
- Python 3.11
- [MediaPipe](https://developers.google.com/mediapipe) — face landmark detection
- OpenCV — webcam capture and preview rendering
- PyAutoGUI — cursor and click control

## Project Structure
```
eye_controlled_mouse/
├── main.py                        # entry point, ties everything together
├── modules/
│   ├── config.py                  # all tunable constants
│   ├── camera.py                  # webcam open/read helpers
│   ├── face_tracker.py            # MediaPipe model loading + detection
│   ├── cursor_controller.py       # iris position -> smoothed cursor movement
│   ├── blink_detector.py          # blink detection -> click / right-click
│   ├── scroll_controller.py       # head tilt -> scroll
│   └── ui_overlay.py              # status panel / control box drawing
├── face_landmarker.task           # MediaPipe model file (download separately)
└── requirements.txt
```

## Setup
1. Clone the repo and install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Download `face_landmarker.task` from
   [MediaPipe's model index](https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker)
   and place it in the project root.
3. Run:
   ```
   python main.py
   ```
4. Press **ESC** to quit.

## Tuning
All thresholds (blink sensitivity, click cooldown, scroll sensitivity, smoothing)
live in `modules/config.py` — no need to touch the logic files to adjust behavior.

## Notes
This project was built as an accessibility-focused hands-free mouse control tool,
iterated through several versions to add double-blink right-click, head-scroll,
and jitter stabilization.
