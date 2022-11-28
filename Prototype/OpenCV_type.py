import cv2
import time
import os
import numpy as np
import mediapipe as mp


cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    success, orignal_img = cap.read()
    # Flip image
    img = cv2.flip(orignal_img, 1)
    
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)

    
    if results.multi_hand_landmarks:
        for handLMs in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLMs, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

