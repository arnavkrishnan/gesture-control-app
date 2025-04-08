import cv2
import mediapipe as mp
import pyautogui

# Initialize camera and MediaPipe Hands detector
cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

# Get screen width and height
screen_width, screen_height = pyautogui.size()

while True:
    # Read the frame from the webcam
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)  # Flip frame horizontally for mirror view
    height, width, _ = frame.shape

    # Convert frame to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)
            landmarks = hand.landmark

            # Get index finger tip position (to move the cursor)
            index_finger_tip = landmarks[8]
            x = int(index_finger_tip.x * width)
            y = int(index_finger_tip.y * height)

            # Map the hand coordinates to screen coordinates
            screen_x = screen_width / width * x
            screen_y = screen_height / height * y

            # Move the cursor
            pyautogui.moveTo(screen_x, screen_y)

            # Get thumb and index finger for scroll detection
            thumb_tip = landmarks[4]
            distance = ((thumb_tip.x - index_finger_tip.x) ** 2 + (thumb_tip.y - index_finger_tip.y) ** 2) ** 0.5

            if distance < 0.03:  # If fingers are close enough, trigger scroll
                pyautogui.scroll(-20)

    # Display the webcam feed with hand tracking
    cv2.imshow("Hand Tracking", frame)

    if cv2.waitKey(1) == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
