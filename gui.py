import tkinter as tk
from tkinter import messagebox
import cv2
import os
import numpy as np
from PIL import ImageTk, Image


window = tk.tk()
window.title("Face Recognition")

l1 = tk.Label(window, text="Name:")
l1.grid(column=0, row=0)
t1 = tk.Entry(window, width=50,bd=5)
t1.grid(column=1, row=0)

window.geometry('500x500')
window.mainloop()
