import pyautogui

# Get the size of the primary monitor.
screenWidth, screenHeight = pyautogui.size()
screenWidth, screenHeight
(2560, 1440)

# Get the XY position of the mouse.
currentMouseX, currentMouseY = pyautogui.position()
currentMouseX, currentMouseY
(1314, 345)

pyautogui.moveTo(100, 150)  # Move the mouse to XY coordinates.

pyautogui.click()          # Click the mouse.
pyautogui.click(100, 200)  # Move the mouse to XY coordinates and click it.
# Find where button.png appears on the screen and click it.
pyautogui.click('button.png')

# Move the mouse 400 pixels to the right of its current position.
pyautogui.move(400, 0)
pyautogui.doubleClick()     # Double click the mouse.
# Use tweening/easing function to move mouse over 2 seconds.
pyautogui.moveTo(500, 500, duration=2, tween=pyautogui.easeInOutQuad)

# type with quarter-second pause in between each key
pyautogui.write('Hello world!', interval=0.25)
# Press the Esc key. All key names are in pyautogui.KEY_NAMES
pyautogui.press('esc')

with pyautogui.hold('shift'):  # Press the Shift key down and hold it.
    # Press the left arrow key 4 times.
    pyautogui.press(['left', 'left', 'left', 'left'])
# Shift key is released automatically.

pyautogui.hotkey('ctrl', 'c')  # Press the Ctrl-C hotkey combination.

# Make an alert box appear and pause the program until OK is clicked.
pyautogui.alert('This is the message to display.')
