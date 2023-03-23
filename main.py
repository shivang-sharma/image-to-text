import time
import tkinter as tk
from PIL import ImageGrab, ImageTk
import cv2
import numpy as np
import datetime
from extract_text_util import extract_text
import os
import sys


class Application:
    def __init__(self, master):
        if not os.path.exists('snips/'):
            os.mkdir("snips/")
        self.snip_surface = None
        self.master = master
        self.start_x = None
        self.start_y = None
        self.current_x = None
        self.current_y = None
        self.captured_image_name = None
        self.capture_coordinates = list()
        self.image = None
        root.geometry('800x500+200+200')  # set new geometry
        root.title('CaptureAndExtract')

        self.menu_frame = tk.Frame(master)
        self.menu_frame.pack(fill=tk.BOTH, expand=tk.YES, padx=1, pady=1)

        self.buttonBar = tk.Frame(self.menu_frame, bg="")
        self.buttonBar.pack()

        self.snipButton = tk.Button(self.buttonBar, width=15, height=5, command=self.create_screen_canvas,
                                    text="Select Area")
        self.snipButton.pack()

        self.captureShotButton = tk.Button(self.buttonBar, width=5, height=5, command=self.capture_shot,
                                           text="Capture")
        self.extractTextFromImageButton = tk.Button(self.buttonBar, width=5, height=5, command=self.extract_text,
                                                    text="Extract text")
        self.captured_image_box = tk.Label(self.master)
        self.captured_image_box.pack()
        self.extracted_text_box = tk.Text(self.master)
        self.extracted_text_box.pack()
        self.master_screen = tk.Toplevel(root)
        self.master_screen.withdraw()
        self.picture_frame = tk.Frame(self.master_screen)
        self.picture_frame.pack(fill=tk.BOTH, expand=tk.YES)
        self.h = tk.Scrollbar(root, orient='horizontal')
        self.h.pack(side=tk.BOTTOM, fill=tk.X)
        self.v = tk.Scrollbar(root)
        self.v.pack(side=tk.RIGHT, fill=tk.Y)

    def extract_text(self):
        extracted_string = extract_text(self.captured_image_name)
        self.extracted_text_box.insert(tk.END, extracted_string)

    def capture_shot(self):
        root.withdraw()
        time.sleep(1)
        # self.take_bounded_screenshot(self.capture_coordinates[0], self.capture_coordinates[1],
        #                              self.capture_coordinates[2], self.capture_coordinates[3])
        self.take_bounded_screenshot(self.start_x, self.start_y, self.current_x, self.current_y)
        self.captureShotButton.pack_forget()
        self.snipButton.pack()
        if self.image is not None:
            self.extractTextFromImageButton.pack()
            img = ImageTk.PhotoImage(file="snips/" + self.captured_image_name)
            self.captured_image_box.config(image=img)
            self.captured_image_box.image = img
        self.capture_coordinates = list()
        root.deiconify()

    def create_screen_canvas(self):
        self.master_screen.deiconify()
        root.withdraw()

        self.snip_surface = tk.Canvas(self.picture_frame, cursor="cross")
        self.snip_surface.pack(fill=tk.BOTH, expand=tk.YES)

        self.snip_surface.bind("<ButtonPress-1>", self.on_button_press)
        self.snip_surface.bind("<B1-Motion>", self.on_snip_drag)
        self.snip_surface.bind("<ButtonRelease-1>", self.on_button_release)

        self.master_screen.attributes('-fullscreen', True)
        self.master_screen.attributes('-alpha', .1)
        self.master_screen.lift()
        self.master_screen.attributes("-topmost", True)

    def on_button_release(self, event):
        self.display_rectangle_position()
        if self.start_x > self.current_x and self.start_y > self.current_y:
            temp = self.start_x
            self.start_x = self.current_x
            self.current_x = temp
            temp = self.start_y
            self.start_y = self.current_y
            self.current_y = temp

        elif self.start_x > self.current_x and self.start_y < self.current_y:
            temp = self.start_x
            self.start_x = self.current_x
            self.current_x = temp

        elif self.start_x < self.current_x and self.start_y > self.current_y:
            temp = self.start_y
            self.start_y = self.current_y
            self.current_y = temp

        self.exit_screenshot_mode()
        self.captureShotButton.pack()
        self.snipButton.pack_forget()
        return event

    def exit_screenshot_mode(self):
        self.snip_surface.destroy()
        self.master_screen.withdraw()
        root.deiconify()

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = self.snip_surface.canvasx(event.x)
        self.start_y = self.snip_surface.canvasy(event.y)
        self.snip_surface.create_rectangle(0, 0, 1, 1, outline='red', width=3)

    def on_snip_drag(self, event):
        self.current_x, self.current_y = (event.x, event.y)
        # expand rectangle as you drag the mouse
        self.snip_surface.coords(1, self.start_x, self.start_y, self.current_x, self.current_y)

    def take_bounded_screenshot(self, x1, y1, x2, y2):
        self.image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        file_name = str(datetime.datetime.now().strftime("%f") + ".png")
        # image.save("snips/" + file_name + ".png")
        image_to_be_saved = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR)
        cv2.imwrite("snips/" + file_name, image_to_be_saved)
        self.captured_image_name = file_name
        print("Saved")

    def display_rectangle_position(self):
        print(self.start_x)
        print(self.start_y)
        print(self.current_x)
        print(self.current_y)


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
