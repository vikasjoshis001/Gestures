# Import required libraries
from tkinter import *
from PIL import ImageTk, Image


# class IndexWindow:
#     def helperWindow(self):
help_window = Tk()
help_window.geometry("700x500")

frame1 = Frame(help_window, width=0, height=50)
frame1.grid()
frame1.place(anchor='w', rely=0.4)

# Exit Image
img1 = ImageTk.PhotoImage(Image.open("FingerImages/exit.png"))
image_label_exit = Label(frame1, image=img1)
alt_label_exit = Label(frame1, text="Exit")
alt_label_exit.config(font=("Courier", 14))
image_label_exit.grid(row=0, column=0, padx=50, pady=10)
alt_label_exit.grid(row=1, column=0, padx=10, pady=10)

# LockUnlock Image
img2 = ImageTk.PhotoImage(Image.open("FingerImages/lockunlock.png"))
image_label_lockunlock = Label(frame1, image=img2)
alt_label_lockunlock = Label(frame1, text="Screen Lock/Unlock")
alt_label_lockunlock.config(font=("Courier", 14))
image_label_lockunlock.grid(row=0, column=1, padx=30, pady=5)
alt_label_lockunlock.grid(row=1, column=1, padx=30, pady=10)

# Restart
img3 = ImageTk.PhotoImage(Image.open("FingerImages/restart.png"))
image_label_restart = Label(frame1, image=img3)
alt_label_restart = Label(frame1, text="System Restart")
alt_label_restart.config(font=("Courier", 14))
image_label_restart.grid(row=0, column=2, padx=10, pady=10)
alt_label_restart.grid(row=1, column=2, padx=10, pady=10)

# Save
img4 = ImageTk.PhotoImage(Image.open("FingerImages/save.png"))
image_label_save = Label(frame1, image=img4)
alt_label_save = Label(frame1, text="Save File")
alt_label_save.config(font=("Courier", 14))
image_label_save.grid(row=2, column=0, padx=10, pady=10)
alt_label_save.grid(row=3, column=0, padx=10, pady=10)

# Shutdown
img5 = ImageTk.PhotoImage(Image.open("FingerImages/shutdown.png"))
image_label_shutdown = Label(frame1, image=img5)
alt_label_shutdown = Label(frame1, text="System Shutdown")
alt_label_shutdown.config(font=("Courier", 14))
image_label_shutdown.grid(row=2, column=1, padx=10, pady=10)
alt_label_shutdown.grid(row=3, column=1, padx=10, pady=10)

help_window.mainloop()
