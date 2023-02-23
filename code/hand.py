import cv2
import time
import os
import numpy as np
import mediapipe as mp


mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils


class HandDetector:
    def __init__(
        self, mode=False, maxHands=2, complexity=1, detectCon=0.5, trackCon=0.5
    ):

        self.mode = mode
        self.maxHands = int(maxHands)
        self.complexity = complexity
        self.detectCon = float(detectCon)
        self.trackCon = float(trackCon)

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            self.mode, self.maxHands, self.complexity, self.detectCon, self.trackCon
        )

        self.mpDraw = mp.solutions.drawing_utils

    def FindHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
        return img

    def FindPosition(self, img, handNo=0, draw=True):
        lmList = []

        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(hand.landmark):
                height, width, channel = img.shape
                cx, cy = int(lm.x * width), int(lm.y * height)
                lmList.append([id, cx, cy])

                # Print all landmarks
                # print(id, cx, cy)

                if draw:
                    cv2.circle(img, (cx, cy), 1, (255, 0, 255), cv2.FILLED)

        return lmList

    def FindMeanPosition(self, img):
        lmList = self.FindPosition(img)
        x_sum = y_sum = 0

        for lm in lmList:
            cx = lm[1]
            cy = lm[2]
            x_sum += cx
            y_sum += cy

        x_mean = x_sum / 21
        y_mean = y_sum / 21
        return lmList, round(x_mean), round(y_mean)


def main():
    capture = cv2.VideoCapture(0)
    previous_time = 0
    current_time = 0

    current_pos = (0, 0)
    previous_pos = (0, 0)

    Detector = HandDetector()

    while True:
        success, orignal_img = capture.read()
        # Flip image
        img = cv2.flip(orignal_img, 1)
        img = Detector.FindHands(img)
        # lmList = Detector.FindPosition(img)

        lmList, x_mean, y_mean = Detector.FindMeanPosition(img)

        # print(lmList)
        # if hand is detected

        current_pos = (x_mean, y_mean)
        change_pos = tuple(np.subtract(previous_pos, current_pos))
        previous_pos = current_pos

        if len(lmList) != 0:
            # print(lmList[4])
            print(x_mean, y_mean)
            print(change_pos)

        current_time = time.time()
        fps = 1 / (current_time - previous_time)
        previous_time = current_time

        cv2.putText(
            img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 3
        )

        cv2.imshow("Image", img)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
