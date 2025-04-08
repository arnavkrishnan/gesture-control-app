import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)
            landmarks = hand.landmark

            # Index finger tip
            index_finger_tip = landmarks[8]
            x = int(index_finger_tip.x * width)
            y = int(index_finger_tip.y * height)

            screen_x = screen_width / width * x
            screen_y = screen_height / height * y

            pyautogui.moveTo(screen_x, screen_y)

            # Scroll if thumb and index touch
            thumb_tip = landmarks[4]
            distance = ((thumb_tip.x - index_finger_tip.x) ** 2 + (thumb_tip.y - index_finger_tip.y) ** 2) ** 0.5

            if distance < 0.03:
                pyautogui.scroll(-20)

    cv2.imshow("Hand Tracking", frame)

    if cv2.waitKey(1) == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
