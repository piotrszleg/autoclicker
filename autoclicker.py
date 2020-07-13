import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode

delay = 0.1
button = Button.left
hold_key = KeyCode(char='b')
clicking_key = KeyCode(char='n')
exit_key = KeyCode(char='m')

class ClickingThread(threading.Thread):
    def __init__(self, delay, button):
        super(ClickingThread, self).__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running:
                mouse.click(self.button)
                time.sleep(self.delay)
            time.sleep(0.1)

mouse = Controller()
clicking_thread = ClickingThread(delay, button)
clicking_thread.start()
holding = False

def on_press(key):
    global holding
    if key == clicking_key:
        if clicking_thread.running:
            clicking_thread.stop_clicking()
        else:
            clicking_thread.start_clicking()
    elif key == hold_key:
        if not holding:
            mouse.press(Button.left)
        else:
            mouse.release(Button.left)
        holding=not holding
    elif key == exit_key:
        clicking_thread.exit()
        listener.stop()

with Listener(on_press=on_press) as listener:
    listener.join()