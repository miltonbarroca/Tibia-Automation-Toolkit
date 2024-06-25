import threading
import tkinter as tk
from ttkthemes import ThemedTk
from tkinter import ttk
from PIL import ImageGrab
import pyautogui as pg
import keyboard

LIFE_REGION = (1766, 304, 92, 5)
LIFE_COLOR = (218, 79, 79)
MANA_REGION = (1766, 316, 92, 5)
MANA_COLOR = (67, 64, 191)
WIDTH = 92

def calculate_width(percent):
    return int(WIDTH * percent / 100)

def pixel_matches_color(region, percent, color):
    result_width = calculate_width(percent)
    screenshot = ImageGrab.grab(bbox=(region[0], region[1], region[0] + region[2], region[1] + region[3]))
    pixel_color = screenshot.getpixel((result_width, region[3] - 1))
    return pixel_color == color

def manager_suplies(event, pause_event, life_threshold, life_button, exura_threshold, exura_button, mana_threshold, mana_button):
    while not event.is_set():
        if not pixel_matches_color(LIFE_REGION, life_threshold, LIFE_COLOR):
            pg.press(life_button)
        if event.is_set():
            return
        if not pixel_matches_color(LIFE_REGION, exura_threshold, LIFE_COLOR):
            pg.press(exura_button)
        if not pixel_matches_color(MANA_REGION, mana_threshold, MANA_COLOR):
            pg.press(mana_button)
        if event.is_set():
            return
        while pause_event.is_set():
            if event.is_set():
                return
            pass

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Supply Manager")
        self.root.geometry("400x500")  # Define a geometria da janela

        style = ttk.Style()
        style.theme_use('black')  # Use the 'clam' theme

        # Apply custom styles
        style.configure('TButton', font=("Roboto", 12))
        style.configure('Ativado.TButton', foreground="green")
        style.configure('Desativado.TButton', foreground="red")

        self.create_widgets()
        
        self.stop_event = threading.Event()
        self.pause_event = threading.Event()
        self.thread = None

        keyboard.add_hotkey('=', self.toggle_pause_resume)
        keyboard.add_hotkey('esc', self.stop)

    def create_widgets(self):
        options = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

        label_font = ('Helvetica', 12, 'bold')
        entry_font = ('Helvetica', 12)

        ttk.Label(self.root, text="Life Threshold:", font=label_font).pack(pady=(10, 0))
        self.life_threshold = tk.StringVar(self.root)
        self.life_threshold.set(options[6])  # default value is 70
        ttk.OptionMenu(self.root, self.life_threshold, *options).pack(pady=(0, 10))

        ttk.Label(self.root, text="Life Button:", font=label_font).pack(pady=(10, 0))
        self.life_button = ttk.Entry(self.root, font=entry_font)
        self.life_button.pack(pady=(0, 10))
        self.life_button.insert(0, "2")

        ttk.Label(self.root, text="Exura Threshold:", font=label_font).pack(pady=(10, 0))
        self.exura_threshold = tk.StringVar(self.root)
        self.exura_threshold.set(options[3])  # default value is 40
        ttk.OptionMenu(self.root, self.exura_threshold, *options).pack(pady=(0, 10))

        ttk.Label(self.root, text="Exura Button:", font=label_font).pack(pady=(10, 0))
        self.exura_button = ttk.Entry(self.root, font=entry_font)
        self.exura_button.pack(pady=(0, 10))
        self.exura_button.insert(0, "1")

        ttk.Label(self.root, text="Mana Threshold:", font=label_font).pack(pady=(10, 0))
        self.mana_threshold = tk.StringVar(self.root)
        self.mana_threshold.set(options[8])  # default value is 80
        ttk.OptionMenu(self.root, self.mana_threshold, *options).pack(pady=(0, 10))

        ttk.Label(self.root, text="Mana Button:", font=label_font).pack(pady=(10, 0))
        self.mana_button = ttk.Entry(self.root, font=entry_font)
        self.mana_button.pack(pady=(0, 20))
        self.mana_button.insert(0, "3")

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)

        self.start_button = ttk.Button(button_frame, text="Start", command=self.start, width=15, style='Ativado.TButton')
        self.start_button.pack(side="left", padx=5)

        # self.pause_button = ttk.Button(button_frame, text="Pause", command=self.pause, width=15, style='Desativado.TButton')
        # self.pause_button.pack(side="left", padx=5)

        # self.resume_button = ttk.Button(button_frame, text="Resume", command=self.resume, width=15, style='Ativado.TButton')
        # self.resume_button.pack(side="left", padx=5)

        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop, width=15, style='Desativado.TButton')
        self.stop_button.pack(side="left", padx=5)
        # Add signature
        signature_font = ('Helvetica', 10, 'italic')
        signature_label = ttk.Label(self.root, text="Tibia Tool Kit", font=signature_font)
        signature_label.pack(side="bottom", pady=(5, 5))

    def start(self):
        if self.thread is None or not self.thread.is_alive():
            self.stop_event.clear()
            self.pause_event.clear()
            life_threshold = int(self.life_threshold.get())
            life_button = self.life_button.get()
            exura_threshold = int(self.exura_threshold.get())
            exura_button = self.exura_button.get()
            mana_threshold = int(self.mana_threshold.get())
            mana_button = self.mana_button.get()
            self.thread = threading.Thread(target=manager_suplies, args=(self.stop_event, self.pause_event, life_threshold, life_button, exura_threshold, exura_button, mana_threshold, mana_button))
            self.thread.start()
            self.root.iconify()  # Minimize the window

    def pause(self):
        self.pause_event.set()

    def resume(self):
        self.pause_event.clear()

    def toggle_pause_resume(self):
        if self.pause_event.is_set():
            self.resume()
        else:
            self.pause()

    def stop(self):
        self.stop_event.set()
        self.pause_event.clear()  # Just to make sure it's not paused
        if self.thread is not None:
            self.thread.join()
        self.root.quit()

if __name__ == "__main__":
    root = ThemedTk(theme="black", themebg=True)
    app = App(root)
    root.mainloop()
