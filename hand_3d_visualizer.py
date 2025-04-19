import cv2
import mediapipe as mp
import numpy as np
import open3d as o3d

# Setup MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

# Landmark connections
connections = mp_hands.HAND_CONNECTIONS

# OpenCV Capture
cap = cv2.VideoCapture(0)

# Open3D Visualizer Setup
vis = o3d.visualization.Visualizer()
vis.create_window(window_name="3D Hand Skeleton")
pcd = o3d.geometry.PointCloud()
lines = o3d.geometry.LineSet()

vis.add_geometry(pcd)
vis.add_geometry(lines)

def update_geometry(points, conn_indices):
    pcd.points = o3d.utility.Vector3dVector(points)
    lines.points = o3d.utility.Vector3dVector(points)
    lines.lines = o3d.utility.Vector2iVector(conn_indices)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        landmarks = result.multi_hand_landmarks[0]

        points = []
        for lm in landmarks.landmark:
            # Flip Z because Open3D coordinate system is different
            points.append([lm.x, -lm.y, -lm.z * 0.5])

        conn_indices = []
        for c in connections:
            conn_indices.append([c[0], c[1]])

        update_geometry(points, conn_indices)
        vis.update_geometry(pcd)
        vis.update_geometry(lines)
        vis.poll_events()
        vis.update_renderer()

    cv2.imshow("Webcam", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
vis.destroy_window()
cv2.destroyAllWindows()
