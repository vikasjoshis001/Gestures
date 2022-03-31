from tkinter import *
import HandGestures as hg
from tkinter import messagebox

root = Tk()
global new_window
new_window = Toplevel(root)
new_window.geometry("250x250")
new_window.title("Register")
# new_window.resizable(False, False)
leb = Label(new_window, text="Enter Name")
global inp
inp = Entry(new_window, width=40)
inp.grid(padx=10, pady=10)

# app = Frame(root, bg="white")
# register_button = Button(new_window, text="", command=registerFace)
# app.grid()
# register_button.pack()
# register_button['command'] = lambda: registerFace(inp)
leb.grid()
