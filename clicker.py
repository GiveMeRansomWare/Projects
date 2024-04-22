import time
import threading
import keyboard
from pynput.mouse import Button, Controller # make sure to install pynput, to do so: pip install pynput

class AutoClicker:
    def __init__(self):
        self.is_clicking = False
        self.click_delay = 0
        self.stop_event = threading.Event()
        self.click_thread = None

    def toggle_clicking(self, cps):
        self.is_clicking = not self.is_clicking
        if self.is_clicking:
            if not self.click_thread or not self.click_thread.is_alive():
                self.start_clicking(cps)
        else:
            self.stop_clicking()

    def start_clicking(self, cps):
        self.click_delay = 1 / cps
        self.stop_event.clear()
        self.click_thread = threading.Thread(target=self.click_loop, daemon=True)
        self.click_thread.start()

    def click_loop(self):
        mouse = Controller()
        while not self.stop_event.is_set():
            mouse.click(Button.left)
            time.sleep(self.click_delay)

    def stop_clicking(self):
        self.stop_event.set()

auto_clicker = AutoClicker()

print("Auto Clicker is ready.")
print("Press Ctrl + C to exit the program.")
print("Press '1' key to toggle auto clicking.")

cps = 75 # do any number you want here

try:
    while True:
        if keyboard.is_pressed('ctrl+c'):
            auto_clicker.stop_clicking()
            print("Auto Clicker stopped.")
            break

        if keyboard.is_pressed('1'):
            auto_clicker.toggle_clicking(cps)
            print("Auto Clicker is now", "active." if auto_clicker.is_clicking else "inactive.")
            time.sleep(0.2)

except KeyboardInterrupt:
    auto_clicker.stop_clicking()
    print("\nAuto Clicker stopped.")
