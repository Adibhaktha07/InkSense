# ✍️ InkSense — AI-Powered Virtual Drawing with Hand Gestures

**InkSense** is an interactive real-time drawing application that uses **hand gestures** to draw on the screen — no touch or stylus needed! Powered by **OpenCV** and **MediaPipe**, it allows users to paint using their **index finger**, erase using their **palm**, and even switch brush colors using custom gestures.

---

## 🎯 Features

- 🖐️ Finger-tracking powered by MediaPipe
- 🎨 Draw on screen using your index finger
- ✋ Erase using your palm (5-finger gesture)
- 🌈 Change colors with hand gesture (0th + 4th fingers)
- 🖼️ Fullscreen UI with smooth, clean canvas
- 🧠 No mouse, stylus, or touchscreen required

---

## 🚀 Technologies Used

- **Python**
- **OpenCV**
- **MediaPipe**
- **NumPy**

---

## 📂 Folder Structure
inksense/
│
├── inksense.py # Main application script
├── utils/ # Helper functions (drawing, gesture handling)
├── assets/ # Brush icons, UI overlays (optional)
├── README.md # Project description
└── requirements.txt # Required Python packages

```
1. Clone the Repository
git clone https://github.com/Adibhaktha07/inksense.git
cd inksense

2. Install Dependencies
pip install -r requirements.txt

3. Run the Application
python inksense.py

🧠 Gesture Controls

Gesture	                                  Action
Index Finger                              Only	Draw
All Five Fingers (Palm)                  	Erase Mode
Thumb + Pinky Extended	                  Change Color

🤖 How It Works
Uses MediaPipe Hands to detect hand landmarks in real-time.
Detects which fingers are raised using landmark logic.
Maps fingertip position to screen coordinates.
Draws lines or erases based on the active gesture.

🙋‍♂️ Author
Adithya Bhaktha
