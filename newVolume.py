import cv2
import numpy as np
import MouseHandTrackingModule as htm
import time
from pynput.keyboard import Key, Controller
from pynput.mouse import Button, Controller as mouseController
import keyboard as kboard
from subprocess import call

wCam, hCam = 640, 480
pTime = 0
frameR = 100  # Frame Reduction
smoothening = 10

keyboard = Controller()
mouse_ = mouseController()

plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.handDetector(maxHands=2)
wScr, hScr = 1368, 768
print(wScr, hScr)


def Volume(vol):
    valid = False
    while not valid:
        volume = vol
        try:
            volume = int(volume)
            if (volume <= 100) and (volume >= 0):
                call(["amixer", "-D", "pulse", "sset", "Master", str(volume)+"%"])
                valid = True
        except ValueError:
            pass


while True:
    # 1. Find hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, 0)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # print(x1,y1,x2,y2)
    # 3. Check which fingers are up
        fingers = detector.fingerUp()
        # print(fingers)
        cv2.rectangle(img, (frameR, frameR),
                      (wCam-frameR, hCam-frameR), (255, 0, 255), 2)

        # Volume Control
        if fingers[0] == 1 and fingers[1] == 1 and fingers[3] == 0:
            length, img, lineInfo = detector.findDistance(4, 12, img)
            if (length < 100):
                cv2.circle(img, (lineInfo[4], lineInfo[5]),
                           9, (0, 255, 0), cv2.FILLED)
            vol = np.interp(length, [15, 170], [0, 30])
            volBar = np.interp(length, [50, 200], [400, 150])
            volPar = np.interp(length, [50, 200], [0, 100])
            # print('len ',vol)
            Volume(vol)
            cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
            cv2.rectangle(img, (50, int(volBar)), (85, 400),
                          (0, 255, 0), cv2.FILLED)
            cv2.putText(img, f'{int(volPar)} %', (40, 450),
                        cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

            print(volBar)
    # 11. Frame Rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
