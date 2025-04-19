#!/bin/bash

ENV_NAME="gesture-control-app"
conda info --envs | grep $ENV_NAME

if [ $? -eq 0 ]; then
    echo "✅ Environment '$ENV_NAME' already exists, activating..."
else
    echo "⚙️ Environment '$ENV_NAME' not found, creating a new one..."
    conda create --name $ENV_NAME python=3.9 -y
fi

# Activate the environment
source ~/miniconda3/bin/activate $ENV_NAME

# Install dependencies
echo "📦 Installing dependencies..."
pip install opencv-python mediapipe pyautogui numpy open3d

# Run the app
echo "🚀 Launching Gesture Control with 3D Viewer..."
python app.py

# Optional: Clean exit
conda deactivate
