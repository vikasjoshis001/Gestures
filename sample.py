from pynput.keyboard import Controller as keyboardController
from pynput.keyboard import Key
import time 

keyboard = keyboardController()
time.sleep(5)
keyboard.type("Hello World")
keyboard.press(Key.enter)

























































































