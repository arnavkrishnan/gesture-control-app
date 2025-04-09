#!/bin/bash

# Define the environment name
ENV_NAME="gesture-control-app"

# Check if the environment exists
conda info --envs | grep $ENV_NAME

if [ $? -eq 0 ]; then
    echo "Environment '$ENV_NAME' already exists, activating..."
else
    echo "Environment '$ENV_NAME' not found, creating a new one..."
    # Create a new Conda environment with Python 3.9 (you can adjust the Python version)
    conda create --name $ENV_NAME python=3.9 -y
fi

# Activate the Conda environment
source ~/miniconda3/bin/activate $ENV_NAME

# Install the necessary dependencies (you can include a requirements.txt file or install packages directly)
pip install opencv-python mediapipe pyautogui numpy

# Run the Python script
python app.py

# Deactivate the Conda environment after execution
conda deactivate