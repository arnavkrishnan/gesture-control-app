#!/bin/bash

ENV_NAME="gesture-control-app"
conda info --envs | grep $ENV_NAME

if [ $? -eq 0 ]; then
    echo "✅ Environment '$ENV_NAME' found. Activating..."
else
    echo "⚙️ Environment '$ENV_NAME' not found. Creating..."
    conda create --name $ENV_NAME python=3.9 -y
fi

source ~/miniconda3/bin/activate $ENV_NAME
pip install -r requirements.txt

echo "Which script do you want to run?"
select option in "Gesture Control" "3D Hand Viewer" "Quit"; do
    case $option in
        "Gesture Control")
            python app.py
            break
            ;;
        "3D Hand Viewer")
            python hand_3d_visualizer.py
            break
            ;;
        "Quit")
            break
            ;;
        *) echo "Invalid option $REPLY";;
    esac
done

conda init
conda deactivate
