import cv2 # type: ignore
import time
import pyautogui # type: ignore
import mediapipe as mp # type: ignore
import numpy as np # type: ignore
import configparser  # Import configparser to read INI files

def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    scroll_speed = int(config['settings']['scroll_speed'])
    mouse_sensitivity = int(config['settings']['mouse_sensitivity'])
    click_cooldown_duration = float(config['settings']['click_cooldown'])
    exit_time = float(config['settings']['exit_time'])
    
    return scroll_speed, mouse_sensitivity, click_cooldown_duration, exit_time

scroll_speed, mouse_sensitivity, click_cooldown_duration, exit_time = load_config()

wCam, hCam = 640, 480
frameR = 100
smoothening = mouse_sensitivity

plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.8)
mpDraw = mp.solutions.drawing_utils

wScr, hScr = pyautogui.size()

gesture_name = None
gesture_start = None
click_cooldown = False
exit_start = None

def fingers_up(hand_landmarks):
    fingers = []

    if hand_landmarks.landmark[mpHands.HandLandmark.THUMB_TIP].x < hand_landmarks.landmark[mpHands.HandLandmark.THUMB_IP].x:
        fingers.append(1)
    else:
        fingers.append(0)

    tips_ids = [mpHands.HandLandmark.INDEX_FINGER_TIP,
                mpHands.HandLandmark.MIDDLE_FINGER_TIP,
                mpHands.HandLandmark.RING_FINGER_TIP,
                mpHands.HandLandmark.PINKY_TIP]

    dip_ids = [mpHands.HandLandmark.INDEX_FINGER_PIP,
               mpHands.HandLandmark.MIDDLE_FINGER_PIP,
               mpHands.HandLandmark.RING_FINGER_PIP,
               mpHands.HandLandmark.PINKY_PIP]

    for tip, pip in zip(tips_ids, dip_ids):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    gesture = None

    if results.multi_hand_landmarks:
        handLms = results.multi_hand_landmarks[0]
        mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

        fingers = fingers_up(handLms)
        print("Fingers:", fingers)

        if fingers == [0, 0, 0, 0, 0]:
            gesture = "fist"
            print("🧠 Detected: Fist gesture")
            
        elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
            gesture = "scroll_up"
            print("🧠 Detected: Scroll Up gesture")

        elif fingers[1] == 0 and fingers[2] == 0:
            gesture = "scroll_down"
            print("🧠 Detected: Scroll Down gesture")

        elif fingers == [1, 1, 1, 1, 1]:
            gesture = "move_cursor"
            print("🧠 Detected: Move Cursor gesture")

        elif fingers == [0, 1, 0, 0, 0] and not click_cooldown:
            gesture = "click"
            print("🧠 Detected: Click gesture")

        current_time = time.time()
        if gesture == gesture_name:
            duration = current_time - gesture_start if gesture_start else 0
        else:
            gesture_name = gesture
            gesture_start = current_time
            duration = 0

        if gesture == "scroll_up":
            pyautogui.scroll(scroll_speed)

        elif gesture == "scroll_down":
            pyautogui.scroll(-scroll_speed)

        elif gesture == "move_cursor":
            lm = handLms.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
            x = int(lm.x * wCam)
            y = int(lm.y * hCam)

            x3 = np.interp(x, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y, (frameR, hCam - frameR), (0, hScr))

            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            pyautogui.moveTo(clocX, clocY)
            plocX, plocY = clocX, clocY

        elif gesture == "click" and duration > click_cooldown_duration:
            pyautogui.click()
            print("🖱️ Clicked!")
            click_cooldown = True
            click_time = time.time()

        elif gesture == "fist":
            if exit_start is None:
                exit_start = current_time
            elif current_time - exit_start > exit_time:
                print("👊 Fist held — Exiting!")
                break
        else:
            exit_start = None

    else:
        gesture = None
        gesture_name = None
        gesture_start = None

    if click_cooldown and time.time() - click_time > click_cooldown_duration:
        click_cooldown = False

    cv2.imshow("Gesture Control Overlay", img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()