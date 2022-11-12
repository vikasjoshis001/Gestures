#!/usr/bin/python

# Import Modules...
import configparser
import os
import time
from turtle import home
import uuid
from datetime import datetime
import datetime
from tkinter import *

from matplotlib.pyplot import title
import HandGestures as hg
from tkinter import messagebox
import sys

import cv2
import face_recognition
import numpy as np
from PIL import ImageTk, Image
from pymongo import MongoClient
import Train


def isAccepted():
    print("yes")


def videoStream(frame,name):
    # _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    #mycursor = mydb.cursor()
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(name+datetime.datetime.now().strftime(frame_name))
    fname=config['test']['save_images']+"/"+name+datetime.datetime.now().strftime(frame_name)
    print(fname)
    cv2.imwrite(fname, frame)


def recognizeFace():
    while True:
        process_this_frame = True
        ret, frame = video_capture.read()
        small_frame = cv2.resize(
            frame, (0, 0), fx=0.25, fy=0.25, interpolation=cv2.INTER_CUBIC)
        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations)

            face_names = []

            name = " blank"
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)

                matches = face_recognition.compare_faces(
                    known_face_encodings, face_encoding, tolerance=0.46)
                name = "Unknown"

                face_distances = face_recognition.face_distance(
                    known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        # Display the results

        # temp_encodings=frame
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            # if len(face_encodings) == 1:

            font = cv2.FONT_HERSHEY_DUPLEX
            if(name != 'Unknown'):
                # Draw a box around the face
                cv2.rectangle(frame, (left, top),
                              (right, bottom), (0, 255, 0), 2)
                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35),
                              (right, bottom), (0, 255, 0), cv2.FILLED)
                frameName = "Face authenticated"
            else:
                # Draw a box around the face
                cv2.rectangle(frame, (left, top),
                              (right, bottom), (0, 0, 255), 2)
                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35),
                              (right, bottom), (0, 0, 255), cv2.FILLED)
                frameName = "Unauthenticated Face"
            cv2.putText(frame, frameName, (left + 6, bottom - 6),
                        font, 0.7, (0, 0, 0), 1)
            face_names = list(dict.fromkeys(face_names))

            # Video Window
            # videoStream(frame, name)

            if '_'.join(face_names) == 'Unknown':
                # Draw a box around the face
                name_button['text'] = "Unknown"
                name_button['bg'] = "blue"
                name_button['command'] = lambda: open_details_frame()
            else:
                # Draw a box around the face
                name_button['text'] = face_names[0].split("-")[0]
                name_button['bg'] = "blue"
                name_button['command'] = lambda: open_details_frame()

        name = '_'.join(face_names)
        videoStream(frame, name)

        temp = name
        if temp == 'Unknown':
            print("Face is not authenticated...")
        elif len(temp) == 0:
            print("Unable to detect face...")
        else:
            print("Detecting Gestures...")
            gesture.handGestures(frame)

        temptime = datetime.datetime.now()
        temp_encodings = frame
        home_window.update()

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit()

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

# Get data from frame...
def open_details_frame(name):
    qwerty = collection.find_one({'key': name})

def connectDatabase():
    # Connecting Database...
    try:
        conn = MongoClient()
        print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")

    # Creating Database...
    db = conn.face
    collection = db.face
    cur = collection.find()

    return cur


def createRegisterFrame():
    # home_window.destroy()
    # root.destroy
    # root.pack_forget()
    # video_capture.release()
    # input_window = Tk()
    pass_window.destroy()
    global new_window
    new_window = Toplevel(home_window)
    # new_window.eval('tk::PlaceWindow . center')
    # new_window.geometry("500x150")
    centerWindow(500, 150, new_window)
    new_window.title("Register")
    # new_window.resizable(False, False)
    leb = Label(new_window, text="Enter Name :- ")
    leb.config(font=("Courier", 14))
    global inp
    inp = Entry(new_window, width=60)

    # app = Frame(root, bg="white")
    register_button = Button(
        new_window, text="Click Image", command=registerFace)
    # app.grid()
    # register_button['command'] = lambda: registerFace(inp)
    # leb.grid(padx=10, pady=10)
    # inp.grid(padx=6, pady=8)
    # register_button.grid(padx=10, pady=10)
    leb.grid(sticky='w', padx=10, pady=10)
    inp.grid(padx=10, pady=10)
    register_button.grid(padx=10, pady=10)
    print(" Create Regster Frame...")

    # entry1 = root.Entry(root)
    # canvas1.create_window(200, 140, window=entry1)
    # face_name = entry1.get()
    # clickImages()

# Function to click images for registering user...


def clickImages(face_name):
    home_window.destroy()
    video_capture.release()
    uuid_name = face_name+'-'+str(datetime.datetime.now())
    print(uuid_name)
    train_images = Train.Train()
    os.mkdir(IMAGES_PATH + "/" + uuid_name)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 300)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)

    # time.sleep(2)
    index = 1
    for images in range(5):
        success, img = cap.read()
        # frame = imutils.resize(frame, width=320)
        h, w, c = img.shape
        offset = 0
        offset += int(h / 5) - 10
        cv2.putText(img, "Image Clicked - "+str(index), (10, offset),
                    cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 3)
        index += 1
        image_name = os.path.join(
            IMAGES_PATH, uuid_name, face_name + '.' + '{}.jpeg'.format(str(uuid.uuid1())))
        cv2.imwrite(image_name, img)
        cv2.imshow('image', img)
        cv2.moveWindow('image', 500, 250)
        time.sleep(1)
        if cv2.waitKey(1) and 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    train_images.trainImages()


def registerFace():
    face_name = inp.get()
    clickImages(face_name)
    success_window = Tk()
    # success_window.geometry("0x0")
    centerWindow(0, 0, success_window)
    messagebox.showinfo('Success', 'Face Registered Successfully\nReopen application to see changes')
    print("Registering Face...")
    os.system("python3 newFile.py")
    # success_window.destroy()
    # new_window.destroy()

# def exitCode():
#     sys.exit()


def startProject():
    global gesture
    gesture = hg.HandGesture()
    global video_capture
    video_capture = cv2.VideoCapture(0)
    recognizeFace()


def enterPassword():
    global pass_window
    pass_window = Tk()
    # new_window.eval('tk::PlaceWindow . center')
    # pass_window.geometry("500x150")
    centerWindow(500, 150, pass_window)
    pass_window.title("Authentication using Password")
    # new_window.resizable(False, False)
    pass_leb = Label(pass_window, text="Enter System Password :- ")
    pass_leb.config(font=("Courier", 14))
    # global inp
    pass_inp = Entry(pass_window, show="*", width=60)

    # app = Frame(root, bg="white")
    pass_button = Button(
        pass_window, text="Verify", command=createRegisterFrame)
    # app.grid()
    # register_button['command'] = lambda: registerFace(inp)
    # leb.grid(padx=10, pady=10)
    # inp.grid(padx=6, pady=8)
    # register_button.grid(padx=10, pady=10)
    pass_leb.grid(sticky='w', padx=10, pady=10)
    pass_inp.grid(padx=10, pady=10)
    pass_button.grid(padx=10, pady=10)


def helpFrame():
    help_window = Toplevel(home_window)
    help_window.title("System Commands and their Gestures")
    # help_window.geometry("700x500")
    centerWindow(700, 500, help_window)

    frame1 = Frame(help_window, width=0, height=50)
    frame1.grid()
    frame1.place(anchor='w', rely=0.4)

    # Exit Image
    img1 = ImageTk.PhotoImage(Image.open(
        "/home/vikasjoshis001/Desktop/Gestures/FingerImages/exit.png"))
    image_label_exit = Label(frame1, image=img1)
    alt_label_exit = Label(frame1, text="Exit")
    alt_label_exit.config(font=("Courier", 14))
    image_label_exit.grid(row=0, column=0, padx=50, pady=10)
    alt_label_exit.grid(row=1, column=0, padx=10, pady=10)

    # LockUnlock Image
    img2 = ImageTk.PhotoImage(Image.open(
        "/home/vikasjoshis001/Desktop/Gestures/FingerImages/lockunlock.png"))
    image_label_lockunlock = Label(frame1, image=img2)
    alt_label_lockunlock = Label(frame1, text="Screen Lock/Unlock")
    alt_label_lockunlock.config(font=("Courier", 14))
    image_label_lockunlock.grid(row=0, column=1, padx=30, pady=5)
    alt_label_lockunlock.grid(row=1, column=1, padx=30, pady=10)

    # Restart
    img3 = ImageTk.PhotoImage(Image.open(
        "/home/vikasjoshis001/Desktop/Gestures/FingerImages/restart.png"))
    image_label_restart = Label(frame1, image=img3)
    alt_label_restart = Label(frame1, text="System Restart")
    alt_label_restart.config(font=("Courier", 14))
    image_label_restart.grid(row=0, column=2, padx=10, pady=10)
    alt_label_restart.grid(row=1, column=2, padx=10, pady=10)

    # Save
    img4 = ImageTk.PhotoImage(Image.open(
        "/home/vikasjoshis001/Desktop/Gestures/FingerImages/save.png"))
    image_label_save = Label(frame1, image=img4)
    alt_label_save = Label(frame1, text="Save File")
    alt_label_save.config(font=("Courier", 14))
    image_label_save.grid(row=2, column=0, padx=10, pady=10)
    alt_label_save.grid(row=3, column=0, padx=10, pady=10)

    # Shutdown
    img5 = ImageTk.PhotoImage(Image.open(
        "/home/vikasjoshis001/Desktop/Gestures/FingerImages/shutdown.png"))
    image_label_shutdown = Label(frame1, image=img5)
    alt_label_shutdown = Label(frame1, text="System Shutdown")
    alt_label_shutdown.config(font=("Courier", 14))
    image_label_shutdown.grid(row=2, column=1, padx=10, pady=10)
    alt_label_shutdown.grid(row=3, column=1, padx=10, pady=10)
    
    # VolumeController
    img6 = ImageTk.PhotoImage(Image.open(
        "/home/vikasjoshis001/Desktop/Gestures/FingerImages/VolumeController.jpg"))
    image_label_shutdown = Label(frame1, image=img6)
    alt_label_shutdown = Label(frame1, text="Volume Controller")
    alt_label_shutdown.config(font=("Courier", 14))
    image_label_shutdown.grid(row=2, column=2, padx=10, pady=10)
    alt_label_shutdown.grid(row=3, column=2, padx=10, pady=10)

    help_window.mainloop()


def centerWindow(width, height, window):
    w = width
    h = height
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))


if __name__ == "__main__":
    # Variables for config file...
    frame_name = '%H_%M_%S_%d_%m_%Y.jpg'
    config = configparser.ConfigParser()
    config.read('/home/vikasjoshis001/Files/Projects/My_Projects/Gestures/config.ini')

    # Connecting Database...
    cur = connectDatabase()

    # Variables to store name and encodings of faces...
    known_face_names = []
    known_face_encodings = []

    # Fetch all the encodings and names from database...
    for i in list(cur):
        known_face_names.append(i['key'])
        known_face_encodings.append(i['encodings'])

    # Variables for clickImage function...
    process_this_frame = True
    IMAGES_PATH = "/home/vikasjoshis001/Files/Projects/My_Projects/Gestures/images_to_train/"
    number_of_images = 5
    temp_face_encodes = []

    # global root
    home_window = Tk()
    home_window.title("Home")
    # home_window.geometry("500x150")
    # home_window.eval('tk::PlaceWindow . center')
    # home_window.geometry("700x700")
    centerWindow(700, 700, home_window)

    # Create a frame...
    app = Frame(home_window, bg="white")
    # app.config(height=0,width=0)
    # Create a label in the frame...
    lmain = Label(app)
    # lmain.config(font=('Helvetica bold', 40))
    name_button = Button(app, text="", command=isAccepted)
    name_button.config(height=2, width=35)
    name_button.pack(padx=10, pady=10)

    lmain.pack()

    button1 = Button(app, bg="green", text="Register Face",
                     command=enterPassword)
    button1.config(height=2, width=15)

    button2 = Button(app, bg="yellow", text="Help",
                     command=helpFrame)
    button2.config(height=2, width=15)

    button3 = Button(app, bg="red", text="Exit", command=home_window.destroy)
    button3.config(height=2, width=15)

    app.pack(padx=10, pady=10)
    button1.pack(side=LEFT, padx=30, pady=20)
    button2.pack(side=LEFT, padx=30, pady=20)
    button3.pack(side=LEFT, padx=30, pady=20)

    # time.sleep(3)/
    # home_window.mainloop()
    # root.destroy

    # Capture from camera...
    print("video")
    temp_encodings = []
    temp_time = datetime.datetime.now()
    old_face_encodings = []

    startProject()

    # Variables for registering face...
    register_face = True
    if register_face:
        print('Enter your name?')
        face_name = input()
        # face_name = "Vikas"
        clickImages(face_name)

    # home_window.mainloop()

    # clickImages()
    startProject()
