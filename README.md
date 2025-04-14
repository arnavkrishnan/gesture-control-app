# ✋ Gesture-Controlled Web Interface

A hands-free Flask web app that uses your webcam to recognize real-time hand gestures — enabling you to scroll, click, and control the browser without a mouse or trackpad! 🧠📸

## 🔥 Features

- 🖐️ **Hand Gesture Recognition** powered by [MediaPipe](https://mediapipe.dev/)
- 🌐 **Live Webcam Feed** on the frontend for real-time feedback
- 🧠 **Gesture Classification Engine** that interprets hand landmarks
- 🖱️ **Built-in Actions**:
  - ✌️ **Peace sign** → Scroll up
  - 👇 **Inverted peace sign** → Scroll down
  - ✋ **Open hand** → Move cursor
  - ☝️ **Index finger only** → Click
  - ✊ **Fist** → Exit app

## 📸 Live Webcam Feed

The webpage shows a real-time video stream from your webcam with gesture overlays, so you can see what the model is detecting and how it maps gestures to actions.

---

## 🚀 Getting Started

### 0. Prerequisites

- **Python 3.9+**
- **Conda** (recommended) — [Miniconda Installation Guide](https://www.anaconda.com/docs/getting-started/miniconda/install)
- **pip** installed (`conda install pip` if you’re missing it)
- A webcam 📷

---

### 1. Clone the Repo

```bash
git clone https://github.com/arnavkrishnan/gesture-control-app.git
cd gesture-control-app
```

### 2. Allow Shell Script Execution
```bash
chmod +x run.sh
```

### 3. Run the App

```bash
./run.sh
```
###### This script will:
- ✅ Create (or activate) a Conda environment
- ✅ Install required Python packages
- ✅ Launch the Flask app and open the browser
- ✅ Start the gesture detection engine
###### Then you’re good to go!


## 💡 How It Works
Each hand gesture is converted into a binary list of five values representing whether each finger is extended:

| Gesture Name         | Finger Pattern     | Action        |
|----------------------|--------------------|---------------|
| Open Hand            | [1,1,1,1,1]         | Move cursor   |
| Peace Sign           | [0,1,1,0,0]         | Scroll up     |
| Inverted Peace Sign  | [0,0,0,1,1]         | Scroll down   |
| Index Finger Only    | [0,1,0,0,0]         | Click         |
| Fist                 | [0,0,0,0,0]         | Exit app      |

Gestures are recognized via MediaPipe’s hand landmark tracking and classified with custom logic, then sent to the frontend using WebSockets for interaction.

## Future Ideas
- Drag and drop with gestures 🖱️
- Multi-gesture combos (e.g., swipe + click)
- Browser integration using Selenium or Puppeteer
- Dark mode toggle via palm rotation 🌗
- Visual gesture timeline or heatmap
- AI model training for personalized gestures

## 🙌 Want to Contribute?
#### Pull Requests are welcome. You can contact me on GitHub or via [email](mailto:arnav.s.krishnan@gmail.com).

***

# Thanks!
