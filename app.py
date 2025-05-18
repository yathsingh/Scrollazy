import cv2
import mediapipe as mp
import pyautogui 
import keyboard

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands = 1, min_detection_confidence = 0.8)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0) 

prev_y = 0
scroll_sensitivity = 10
cooldown = 0    

scroll_speed = 80
def increase_scroll_speed():
    global scroll_speed
    scroll_speed += 10
def decrease_scroll_speed():
    global scroll_speed
    scroll_speed = max(10, scroll_speed - 10)
keyboard.on_press_key('up', lambda _: increase_scroll_speed())
keyboard.on_press_key('down', lambda _: decrease_scroll_speed())

while True: 
    success, img=cap.read()
    if not success:
        break
    img = cv2.flip(img, 1)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_img)

    if results.multi_hand_landmarks: 
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            index_finger_tip = hand_landmarks.landmark[8]
            h, w, c = img.shape 
            x, y = int(index_finger_tip.x * w), int(index_finger_tip.y * h)
            index_finger_base = hand_landmarks.landmark[5]
            base_x, base_y = int(index_finger_base.x * w), int(index_finger_base.y * h)

            cv2.circle(img, (x,y), 10, (0,255,0), cv2.FILLED)
            cv2.circle(img, (base_x, base_y), 10, (255, 0, 0), cv2.FILLED)

            cv2.line(img, (base_x, base_y), (x, y), (0, 0, 255), 2)

            if cooldown <= 0:  
                if y < base_y:  
                    pyautogui.scroll(scroll_speed)
                    cv2.putText(img, "Scrolling Up", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                    cooldown = 40
                elif y > base_y:  
                    pyautogui.scroll(-scroll_speed) 
                    cv2.putText(img, "Scrolling Down", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    cooldown = 40

    if cooldown > 0:
        cooldown -= 1

    cv2.imshow("Scrollazy",img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()