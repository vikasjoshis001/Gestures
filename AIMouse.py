import cv2
import numpy as np
import MouseHandTrackingModule as htm
import time
import pyautogui as pmouse
from pynput.keyboard import Key, Controller
from pynput.mouse import Button, Controller as mouseController


def aiMouse(img, frame, fingers):
    wCam, hCam = 640, 480
    pTime = 0
    frameR = 100
    smoothening = 50
    keyboard = Controller()
    mouse_ = mouseController()

    plocX, plocY = 0, 0
    clocX, clocY = 0, 0

    pTime = 0
    detector = htm.handDetector(maxHands=2)
    wScr, hScr = 1368, 768
    while True:
        img = detector.findHands(img)
        lmList = detector.findPosition(img, 0)

        if len(lmList) != 0:
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]

            fingers = detector.fingerUp()

            if fingers[1] == 1 and fingers[2] == 0:
                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (x3 - plocY) / smoothening
                pmouse.moveTo(int(wScr - x3), int(y3))
                cv2.circle(img, (x1, y1), 8, (255, 0, 255), cv2.FILLED)
                plocX, plocY = clocX, clocY

            # 8. Both Index and Middle fingers are up : Clicking Mode
            if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0:
                # 9. Find distance between fingers
                length, img, lineInfo = detector.findDistance(8, 12, img)
                # print(length)
                # 10.Click mouse if distance short
                if (length < 40):
                    mouse_.click(Button.left)

        # 11. Frame Rate
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.waitKey(1)
