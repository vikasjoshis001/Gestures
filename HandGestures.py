# Importing Modules..
import ctypes
import os
import time
import tkinter as tk
from subprocess import call
from tkinter import *
from tkinter import messagebox as mb

import cv2
import numpy as np
import PIL.Image
import pyautogui as pmouse
from PIL import ImageTk
from pynput.keyboard import Controller as keyboardController
from pynput.keyboard import Key
from pynput.mouse import Button
from pynput.mouse import Controller as mouseController

import AIMouse as ai
import HandTrackingModule as htm
import MouseHandTrackingModule as m_htm

mouse = mouseController()
keyboard = keyboardController()
wCam, hCam = 640, 480
smoothening = 10
detector = htm.handDetector()
m_detector = m_htm.handDetector()
frameR = 100
wScr, hScr = 1368, 768


class HandGesture:
    def handGestures(self, frame):
        flag = 0
        enableMouse = False
        img = detector.findHands(frame)
        # m_img = m_detector.findHands(frame)
        lmList, bbox = detector.findPosition(img)
        # m_lmList = m_detector.findPosition(m_img)

        if len(lmList) != 0:
            x1 = lmList[8][1:]
            y1 = lmList[12][1:]

            # m_x1, m_y1 = lmList[8][1:]

            fingers = detector.fingersUp()
            # m_fingers = m_detector.fingerUp()
            # print("m_fingers", m_fingers)

            # Scrolling Up Down Gesture...
            if fingers[1] == 1 and fingers[2] == 1:
                length, img, info = detector.findDistance(8, 12, img)
                if length <= 30:
                    keyboard.press(Key.up)
                    keyboard.release(Key.up)
                    time.sleep(0.5)
                    cv2.circle(img, (info[4], info[5]),
                               10, (0, 255, 0), cv2.FILLED)

                if length > 30:
                    keyboard.press(Key.down)
                    keyboard.release(Key.down)
                    time.sleep(0.5)

            # Enable Mouse
            # if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 1 and fingers[4] == 1:
            #     if not enableMouse:
            #         enableMouse = True
            #     else:
            #         enableMouse = False

            # if fingers[1] == 1 and fingers[2] == 0:
            #     ai.aiMouse(img,frame,fingers)

            # Volume Controller
            if fingers[0] == 1 and fingers[1] == 1 and fingers[3] == 0:
                length, img, lineInfo = detector.findDistance(4, 12, img)
                if (length < 100):
                    cv2.circle(img, (lineInfo[4], lineInfo[5]),
                               9, (0, 255, 0), cv2.FILLED)
                vol = np.interp(length, [15, 170], [0, 30])
                volBar = np.interp(length, [50, 200], [400, 150])
                volPar = np.interp(length, [50, 200], [0, 100])
                # print('len ',vol)
                hg = HandGesture()
                hg.Volume(vol)
                cv2.rectangle(frame, (50, 150), (85, 400), (0, 255, 0), 3)
                cv2.rectangle(frame, (50, int(volBar)), (85, 400),
                              (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, f'{int(volPar)} %', (40, 450),
                            cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

                print(volBar)

            # Save File Gesture...
            if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                print("Save Gesture running...")
                with keyboard.pressed(Key.ctrl):
                    keyboard.press("S")
                    keyboard.release("S")

            # Exit File Gesture...
            if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
                print("Exit Gesture running...")
                with keyboard.pressed(Key.ctrl):
                    keyboard.press(Key.f4)
                    keyboard.release(Key.f4)

            # Lock Unlock Screen Gesture...
            if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
                print("Lock Gesture running...")
                try:
                    os.popen('gnome-screensaver-command --lock')
                except:
                    ctypes.windll.user32.LockWorkStation()

            # Shutdown Gesture...
            if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0:
                print("Shutting Down...")
                cfrmCommand = "poweroff"
                cancelCommand = "shutdown -c"
                HandGesture().generateBox("Shutdown", cfrmCommand, cancelCommand)
                exit()

            # Restart Gesture...
            if fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                print("Restarting Down...")
                cfrmCommand = "reboot"
                cancelCommand = "shutdown -c"
                if flag == 0:
                    HandGesture().generateBox("Restart", cfrmCommand, cancelCommand)
                    flag = 1

            # im = cv2.imshow("Image", img)
            return img

    def msgBox(self, msg, cfrmCommand, cancelCommand):
        res = mb.askquestion('Exit Application',
                             'Do you really want to ' + msg)
        if res == 'yes':
            os.system(cfrmCommand)
        else:
            os.system(cancelCommand)

    def generateBox(self, msg, cfrmCommand, cancelCommand):
        HandGesture().msgBox(msg, cfrmCommand, cancelCommand)
        print("HELLO")

    def Volume(self, vol):
        valid = False
        while not valid:
            volume = vol
            try:
                volume = int(volume)
                if (volume <= 100) and (volume >= 0):
                    call(["amixer", "-D", "pulse", "sset",
                         "Master", str(volume)+"%"])
                    valid = True
            except ValueError:
                pass

# def main():
#     # Coding Gestures...
#     while True:
#         # Taking Image...
#         success, img = cap.read()
#         img = detector.findHands(img)
#         gesture = HandGesture()
#         gesture.handGestures(img)
#         cv2.imshow("Image", img)
#         cv2.waitKey(1)
# #
# if __name__ == "__main__":
#     main()
