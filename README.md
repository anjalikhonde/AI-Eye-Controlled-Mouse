# 👁️ AI Eye Controlled Mouse

Control your computer mouse using only your eye movements! 🚀

This project uses **Computer Vision**, **MediaPipe Face Landmarker**, **OpenCV**, and **PyAutoGUI** to move the mouse cursor based on eye position.

---

## 📌 Features

- 👀 Real-time eye tracking
- 🖱️ Control the mouse cursor using eye movement
- 🎯 Face landmark detection using MediaPipe
- ⚡ Smooth webcam processing with OpenCV
- 🤖 Beginner-friendly AI + Computer Vision project

---

## 🛠️ Technologies Used

- Python 3.11+
- OpenCV
- MediaPipe
- PyAutoGUI

---

## 📂 Project Structure

```
AI-Eye-Controlled-Mouse/
│
├── images/
│   ├── demo.png
│   └── tracking.png
│
├── main.py
├── face_landmarker.task
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 📸 Project Demo

### Eye Tracking

![Eye Tracking](images/demo.png)

---

### Cursor Tracking

![Cursor Tracking](images/tracking.png)

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/anjalikhonde/AI-Eye-Controlled-Mouse.git
```

Move into the project

```bash
cd AI-Eye-Controlled-Mouse
```

Create Virtual Environment

```bash
python -m venv .venv
```

Activate Virtual Environment

Windows

```bash
.venv\Scripts\activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

Run the Project

```bash
python main.py
```

---

## 🧠 How It Works

1. Webcam captures your face.
2. MediaPipe detects facial landmarks.
3. The position of your eye is tracked.
4. Eye coordinates are mapped to the screen.
5. PyAutoGUI moves the mouse cursor accordingly.

---

## 📷 Output

- Detects your face in real time.
- Tracks eye movement.
- Moves the mouse pointer based on your eye position.

---

## 📦 Requirements

```
opencv-python
mediapipe
pyautogui
```

or simply install using

```bash
pip install -r requirements.txt
```

---

## 🚀 Future Improvements

- Left-click using eye blink
- Right-click using wink detection
- Scroll using head movement
- Better cursor smoothing
- Multi-monitor support

---

## 🙋‍♀️ Author

**Anjali Khonde**

Computer Engineering Student

GitHub: https://github.com/anjalikhonde

---

⭐ If you found this project helpful, consider giving it a **Star** on GitHub!
