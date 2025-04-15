#!/bin/bash

ENV_NAME="gesture-control-app"
conda info --envs | grep $ENV_NAME

if [ $? -eq 0 ]; then
    echo "Environment '$ENV_NAME' already exists, activating..."
else
    echo "Environment '$ENV_NAME' not found, creating a new one..."
    conda create --name $ENV_NAME python=3.9 -y
fi

source ~/miniconda3/bin/activate $ENV_NAME
pip install opencv-python mediapipe pyautogui numpy

python app.py

conda init
conda deactivate