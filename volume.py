import cv2
import numpy as np
import HandTrackingModule as htm
# import handTracingModule_raw as htm
import time
from pynput.keyboard import Key, Controller
from pynput.mouse import Button, Controller as mouseController
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import keyboard as kboard
############## PyCaw #####################

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
min_vol = volRange[0]
max_vol = volRange[1]
# volume.SetMasterVolumeLevel(-20.0, None)
######################################
###########################################
wCam, hCam = 640, 480
pTime = 0
frameR = 100  # Frame Reduction
smoothening = 10
#############################################
#############################################
keyboard = Controller()
mouse_ = mouseController()
############################################
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.handDetector(maxHands=2)
wScr, hScr = autopy.screen.size()
print(wScr, hScr)

while True:
    # 1. Find hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, 0)
    # lmList_2 = []
    # lmList_2 = detector.findPosition(img,1)
    # try:
    #     lmList_2 = detector.findPosition(img, 1)
    # except:
    #     lmList_2 = []
    # print(lmList)
    # print("two")
    # print("Hand two : ",lmList_2)
    # 2. Get the tip of the index and middle finger
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # print(x1,y1,x2,y2)
    # 3. Check which fingers are up
        fingers = detector.fingerUp()
        # print(fingers)
        cv2.rectangle(img, (frameR, frameR),
                      (wCam-frameR, hCam-frameR), (255, 0, 255), 2)
        # 4. Only Index Finger : Moving Mode
        if fingers[1] == 1 and fingers[2] == 0:
            # 5. Convert Coordinates
           x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
           y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))
           # 6. Smoothen value
           clocX = plocX + (x3-plocX)/smoothening
           clocY = plocY + (x3 - plocY) / smoothening

           # 7. Move Mouse
           autopy.mouse.move(wScr-x3, y3)
           cv2.circle(img, (x1, y1), 8, (255, 0, 255), cv2.FILLED)
           plocX, plocY = clocX, clocY

        '''## Drag and Drop
        if fingers[1] == 1 and fingers[0] == 1 and fingers[2] == 0:
            # 5. Convert Coordinates
           x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
           y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))
           # 6. Smoothen value
           clocX = plocX + (x3-plocX)/smoothening
           clocY = plocY + (x3 - plocY) / smoothening'''

        '''#7. Move Mouse
           # autopy.mouse.move(wScr-x3,y3)
           mouseController.position = (wScr-x3, y3)
           length, img, lineInfo = detector.findDistance(4, 8, img)
           # print("len ",length)
           # cv2.circle(img,(x1,y1),8,(255,0,255),cv2.FILLED)
           plocX, plocY = clocX, clocY
           while mouseController.position != (wScr-x3, y3):
               pass

          # print(length)'''

        '''# 10.Click mouse if distance short
           print(length)
           if (length < 50):
               cv2.circle(img, (lineInfo[4], lineInfo[5]),
                          9, (0, 255, 0), cv2.FILLED)
               mouse_.press(Button.left)
           else:
               mouse_.release(Button.left)'''
               
        # Volume Control
        if fingers[0] == 1 and fingers[2] == 1 and fingers[3] == 0:
            length, img, lineInfo = detector.findDistance(4, 12, img)
            if (length < 100):
                cv2.circle(img, (lineInfo[4], lineInfo[5]),
                           9, (0, 255, 0), cv2.FILLED)
            vol = np.interp(length, [15, 170], [min_vol, max_vol])
            volBar = np.interp(length, [50, 200], [400, 150])
            volPar = np.interp(length, [50, 200], [0, 100])
            # print('len ',vol)
            volume.SetMasterVolumeLevel(vol, None)
            cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
            cv2.rectangle(img, (50, int(volBar)), (85, 400),
                          (0, 255, 0), cv2.FILLED)
            cv2.putText(img, f'{int(volPar)} %', (40, 450),
                        cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

            print(volBar)
            
        '''#8. Both Index and Middle fingers are up : Clicking Mode
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0:
            # 9. Find distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)
            # print(length)
            # 10.Click mouse if distance short
            if(length < 40):
                cv2.circle(img, (lineInfo[4], lineInfo[5]),
                           9, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()'''

        # Scroll Up
        '''if fingers[4] == 1:
            kboard.press_and_release("down arrow")
        # Scroll Down
        if fingers[0] == 1:
            kboard.press_and_release("up arrow")
        # select and move
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] ==1:
            # 5. Convert Coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            # 6. Smoothen value
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (x3 - plocY) / smoothening

            # 7. Move Mouse
            autopy.mouse.click()
            autopy.mouse.move(wScr - x3, y3)
            cv2.circle(img, (x1, y1), 8, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY'''
        # Copy
        '''if fingers[4] == 1:
            autopy.mouse.click()
            kboard.press_and_release('ctrl+c')
        if fingers[3] == 1 and fingers[4] == 1:
            kboard.press('ctrl+v')'''

    # 11. Frame Rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
