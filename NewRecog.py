# Import Modules...
import configparser
import os
import time
from turtle import left
import uuid
from datetime import datetime
import datetime
from tkinter import *
from tkinter import messagebox

from matplotlib.pyplot import text
import HandGestures as hg
# import "home/vikasjoshis001/Desktop/Handtracking/HandGestures"

import cv2
import face_recognition
import numpy as np
from PIL import ImageTk, Image
from pymongo import MongoClient
import Train


def isAccepted():
    print("yes")


def videoStream(frame, name):
    # _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    # mycursor = mydb.cursor()
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(name + datetime.datetime.now().strftime(frame_name))
    fname = config['test']['save_images'] + "/" + name + \
        datetime.datetime.now().strftime(frame_name)
    print(fname)
    cv2.imwrite(fname, frame)


def recognizeFace():
    video_capture = cv2.VideoCapture(0)
    while True:
        process_this_frame = True
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
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
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35),
                          (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            if(name != 'Unknown'):
                frameName = "Face authenticated"
            else:
                frameName = "Unauthenticated Face"
            cv2.putText(frame, frameName, (left + 6, bottom - 6),
                        font, 0.7, (0, 0, 0), 1)
            face_names = list(dict.fromkeys(face_names))
            videoStream(frame, name)

            if '_'.join(face_names) == 'Unknown':
                button1['text'] = "Register"
                button1['bg'] = "blue"
                button1['command'] = lambda: createRegisterFrame()
            else:
                button1['text'] = "Register"
                button1['bg'] = "blue"
                button1['command'] = lambda: createRegisterFrame()
                # button1['text'] = '_'.join(face_names)
                # button1['bg'] = "green"
                # button1['command'] = lambda: donothing()

        name = '_'.join(face_names)

        temp = name
        if temp == 'Unknown':
            print("Face is not authenticated...")
        elif len(temp) == 0:
            print("Unable to detect face...")
        else:
            print("Detecting Gestures...")
            # gesture.handGestures(frame)

        temptime = datetime.datetime.now()
        temp_encodings = frame
        root.update()

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit()

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()


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
    print("Connected...")

    # Get data from frame...
    def open_details_frame(name):
        qwerty = collection.find_one({'key': name})

    return cur


def createRegisterFrame():
    global new_window
    new_window = Toplevel(root)
    new_window.geometry("250x250")
    new_window.title("Register")
    new_window.resizable(False, False)
    leb = Label(new_window, text="Enter Name")
    global inp
    inp = Entry(new_window, width=40)
    inp.pack()

    # app = Frame(root, bg="white")
    register_button = Button(new_window, text="", command=registerFace)
    # app.grid()
    register_button.pack()
    # register_button['command'] = lambda: registerFace(inp)
    leb.pack()
    # entry1 = root.Entry(root)
    # canvas1.create_window(200, 140, window=entry1)
    # face_name = entry1.get()
    # clickImages()

# Function to click images for registering user...


def clickImages(face_name):
    # exit()
    print("Clickcing Images")
    messagebox.showinfo(title=None, message=str(face_name))
    uuid_name = face_name+'-'+str(datetime.datetime.now())
    print(uuid_name)
    train_images = Train.Train()
    os.mkdir(IMAGES_PATH + "/" + uuid_name)
    messagebox.showinfo(title=None, message="Starting")
    cap = cv2.VideoCapture(0)
    messagebox.showinfo(title=None, message="Continuing...")
    # time.sleep(2)
    for images in range(5):
        messagebox.showinfo(title=None, message="Cliclking Images...")
        success, img = cap.read()
        image_name = os.path.join(
            IMAGES_PATH, uuid_name, face_name + '.' + '{}.jpeg'.format(str(uuid.uuid1())))
        messagebox.showinfo(title=None, message="Image Clicked...")
        # cv2.imwrite(image_name, img)
        messagebox.showinfo(title=None, message="Exit 1..")
        # cv2.imshow('image', img)
        messagebox.showinfo(title=None, message="Exit 2s..")
        # time.sleep(1)

        if cv2.waitKey(1) and 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    train_images.trainImages()


def registerFace():
    face_name = inp.get()
    messagebox.showinfo(title=None, message=str(face_name))
    clickImages(face_name)
    messagebox.showinfo(title=None, message="face registered successfully")
    new_window.destroy()
    print("face_name: ", face_name)
    exit()


if __name__ == "__main__":
    # Variables for config file...
    frame_name = '%H_%M_%S_%d_%m_%Y.jpg'
    config = configparser.ConfigParser()
    config.read('config.ini')

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
    IMAGES_PATH = "images_to_train"
    number_of_images = 5
    temp_face_encodes = []
    root = Tk()

    # Create a frame...
    app = Frame(root, bg="white")
    button1 = Button(app, text="", command=isAccepted)
    app.grid()
    button1.grid()

    app2 = Frame(root, bg="white")
    button2 = Button(app2, text="Register", command=isAccepted)
    app2.grid()
    button2.grid()

    # Create a label in the frame...
    lmain = Label(app)
    lmain.grid()

    # Capture from camera...
    print("video")
    temp_encodings = []
    temp_time = datetime.datetime.now()
    old_face_encodings = []

    # Variables for registering face...
    #ace_name = "unknown"cha
    register_face = True
    if register_face:
        print('Enter your name?')
        face_name = input()
        # face_name = "Vikas"
        clickImages(face_name)

    # clickImages()
    global inp
    gesture = hg.HandGesture()
    recognizeFace()
