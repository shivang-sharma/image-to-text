import time
from tkinter import *
from PIL import ImageGrab
import cv2
import numpy as np
import datetime


def take_bounded_screenshot(x1, y1, x2, y2):
    image = np.array(ImageGrab.grab(bbox=(x1, y1, x2, y2)))
    file_name = datetime.datetime.now().strftime("%f")
    # image.save("snips/" + file_name + ".png")
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imwrite("snips/" + file_name + ".png", image)


class Application:
    def __init__(self, master, capture_coordinates):
        self.snip_surface = None
        self.master = master
        self.start_x = None
        self.start_y = None
        self.current_x = None
        self.current_y = None
        self.capture_coordinates = capture_coordinates
        root.geometry('400x50+200+200')  # set new geometry
        root.title('Lil Snippy')

        self.menu_frame = Frame(master)
        self.menu_frame.pack(fill=BOTH, expand=YES, padx=1, pady=1)

        self.buttonBar = Frame(self.menu_frame, bg="")
        self.buttonBar.pack()

        self.snipButton = Button(self.buttonBar, width=5, height=5, command=self.create_screen_canvas, text="Snip")
        self.snipButton.pack()

        self.captureShotButton = Button(self.buttonBar, width=5, height=5, command=self.capture_shot,
                                        text="Capture")

        self.master_screen = Toplevel(root)
        self.master_screen.withdraw()
        self.picture_frame = Frame(self.master_screen)
        self.picture_frame.pack(fill=BOTH, expand=YES)

    def capture_shot(self):
        root.withdraw()
        time.sleep(1)
        take_bounded_screenshot(
            self.capture_coordinates[0], self.capture_coordinates[1],
            self.capture_coordinates[2], self.capture_coordinates[3])
        self.captureShotButton.pack_forget()
        self.snipButton.pack()
        root.deiconify()

    def create_screen_canvas(self):
        self.master_screen.deiconify()
        root.withdraw()

        self.snip_surface = Canvas(self.picture_frame, cursor="cross")
        self.snip_surface.pack(fill=BOTH, expand=YES)

        self.snip_surface.bind("<ButtonPress-1>", self.on_button_press)
        self.snip_surface.bind("<B1-Motion>", self.on_snip_drag)
        self.snip_surface.bind("<ButtonRelease-1>", self.on_button_release)

        self.master_screen.attributes('-fullscreen', True)
        self.master_screen.attributes('-alpha', .1)
        self.master_screen.lift()
        self.master_screen.attributes("-topmost", True)

    def on_button_release(self, event):
        self.display_rectangle_position()
        if self.start_x <= self.current_x and self.start_y <= self.current_y:
            print("right down")
            take_bounded_screenshot(self.start_x, self.start_y, self.current_x - self.start_x, self.current_y - self.start_y)
            self.capture_coordinates.append(self.start_x)
            self.capture_coordinates.append(self.start_y)
            self.capture_coordinates.append(self.current_x - self.start_x)
            self.capture_coordinates.append(self.current_y - self.start_y)

        elif self.start_x >= self.current_x and self.start_y <= self.current_y:
            print("left down")
            take_bounded_screenshot(self.current_x, self.start_y, self.start_x - self.current_x, self.current_y - self.start_y)
            self.capture_coordinates.append(self.current_x)
            self.capture_coordinates.append(self.start_y)
            self.capture_coordinates.append(self.start_x - self.current_x)
            self.capture_coordinates.append(self.current_y - self.start_y)

        elif self.start_x <= self.current_x and self.start_y >= self.current_y:
            print("right up")
            take_bounded_screenshot(self.start_x, self.current_y, self.current_x - self.start_x, self.start_y - self.current_y)
            self.capture_coordinates.append(self.start_x)
            self.capture_coordinates.append(self.current_y)
            self.capture_coordinates.append(self.current_x - self.start_x)
            self.capture_coordinates.append(self.start_y - self.current_y)

        elif self.start_x >= self.current_x and self.start_y >= self.current_y:
            print("left up")
            take_bounded_screenshot(self.current_x, self.current_y, self.start_x - self.current_x, self.start_y - self.current_y)
            self.capture_coordinates.append(self.current_x)
            self.capture_coordinates.append(self.current_y)
            self.capture_coordinates.append(self.start_x - self.current_x)
            self.capture_coordinates.append(self.start_y - self.current_y)

        self.exit_screenshot_mode()
        if len(self.capture_coordinates) == 4:
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

    def display_rectangle_position(self):
        print(self.start_x)
        print(self.start_y)
        print(self.current_x)
        print(self.current_y)


if __name__ == '__main__':
    output = list()
    root = Tk()
    app = Application(root, output)
    root.mainloop()
    print(output)