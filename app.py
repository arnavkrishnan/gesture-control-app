import cv2
import mediapipe as mp
import pyautogui
import math

# Initialize MediaPipe hands model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Get screen width and height
screen_width, screen_height = pyautogui.size()

# Start webcam
cap = cv2.VideoCapture(0)

# Function to calculate distance between two points
def calculate_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

while True:
    # Read frame from webcam
    ret, frame = cap.read()

    if not ret:
        break

    # Flip the image for a later selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame and detect hands
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            # Get the positions of specific landmarks (fingertips, palm center, etc.)
            thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_tip = landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_tip = landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
            wrist = landmarks.landmark[mp_hands.HandLandmark.WRIST]

            # Get hand center (for moving cursor)
            hand_center_x = int((wrist.x + index_tip.x) * screen_width / 2)
            hand_center_y = int((wrist.y + index_tip.y) * screen_height / 2)

            # Map the hand coordinates to screen coordinates
            screen_x = int(screen_width * hand_center_x)
            screen_y = int(screen_height * hand_center_y)

            # Move the cursor based on the hand center
            pyautogui.moveTo(screen_x, screen_y)

            # Check for hand gesture: open vs. closed (fist vs. open hand)
            # Distance between the index and thumb tips to check for fist (closed hand)
            distance_thumb_index = calculate_distance((thumb_tip.x, thumb_tip.y), (index_tip.x, index_tip.y))

            if distance_thumb_index < 0.05:  # Small distance = fist (closed hand)
                # Scroll down when fist is detected
                pyautogui.scroll(-10)  # Adjust scroll speed as necessary
                print("Scrolling down (fist detected)")

            elif distance_thumb_index > 0.2:  # Large distance = open hand
                # Scroll up when open hand is detected
                pyautogui.scroll(10)  # Adjust scroll speed as necessary
                print("Scrolling up (open hand detected)")

            # Optionally detect clicking based on hand open/close:
            if distance_thumb_index < 0.05 and len(landmarks) > 0:  # Fist -> Click
                pyautogui.click()
                print("Click detected (fist)")

    # Show the webcam feed with landmarks drawn on the hand
    cv2.imshow("Hand Gesture Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to quit
        break

cap.release()
cv2.destroyAllWindows()
