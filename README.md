# 👁️ AI Eye Controlled Mouse

An AI-powered Eye Controlled Mouse built using **Python**, **OpenCV**, and **Google MediaPipe**.

This project detects facial landmarks in real-time using a webcam and serves as the foundation for controlling a computer mouse with eye movements.

---

## 🚀 Features

- 🎥 Real-time webcam capture
- 😊 AI Face Landmark Detection
- 👁️ Detects 478 facial landmarks
- ⚡ Fast and lightweight using MediaPipe
- 🖥️ Built with OpenCV
- 🐍 Beginner-friendly Python project

---

## 🛠️ Technologies Used

- Python 3.11
- OpenCV
- MediaPipe
- PyAutoGUI
- Computer Vision

---

## 📂 Project Structure

```
AI-Eye-Controlled-Mouse/
│
├── main.py
├── face_landmarker.task
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 📸 Output

> **Add your project screenshot here**

Example:

```
images/
    output.png
```

Then add:

```markdown
![Output](images/output.png)
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/anjalikhonde/AI-Eye-Controlled-Mouse.git
```

### 2. Open the project

```bash
cd AI-Eye-Controlled-Mouse
```

### 3. Create Virtual Environment

```bash
py -3.11 -m venv .venv
```

### 4. Activate Virtual Environment

**Windows**

```bash
.venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Project

```bash
python main.py
```

---

## 📖 How It Works

1. Opens the webcam using OpenCV.
2. Captures frames in real time.
3. Converts BGR images to RGB.
4. Sends each frame to the MediaPipe Face Landmarker model.
5. Detects facial landmarks.
6. Draws landmarks on the face.
7. Displays the live camera feed.

---

## 📌 Future Improvements

- Eye-controlled mouse cursor
- Blink detection
- Left click
- Right click
- Double click
- Scroll using eye movement
- Drag and Drop
- Improved tracking accuracy

---

## 🎯 Learning Outcomes

Through this project, I learned:

- Python Programming
- OpenCV Basics
- Computer Vision
- MediaPipe Face Landmarker
- Real-time Video Processing
- AI-based Facial Landmark Detection
- Git & GitHub

---

## 👩‍💻 Author

**Anjali Khonde**

GitHub:
https://github.com/anjalikhonde

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
