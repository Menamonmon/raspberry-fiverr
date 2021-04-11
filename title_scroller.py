from PIL import Image, ImageTk
import tkinter as tk

with open("./screen_info.txt", "r") as f:
    screen_width, screen_height, _ = map(int, f.readline().split(","))


class TitleScroller:
    def __init__(self, master, image):
        self.master = master
        self.image = image
        loadTitle = Image.open(self.image).resize(
            (int(screen_width * (8.85/15)), int(screen_height * (2/15))))
        renderTitle = ImageTk.PhotoImage(loadTitle)
        self.labelLeft = tk.Label(self.master, image=renderTitle)
        self.labelLeft.image = renderTitle
        self.labelRight = tk.Label(self.master, image=renderTitle)
        self.labelRight.image = renderTitle
        self.n = 0

    def draw(self):
        self.labelLeft.place(relx=-self.n, rely=0, relwidth=1, relheight=1)
        self.labelRight.place(relx=1-self.n, rely=0,
                              relwidth=1, relheight=1)

    def update(self):
        if (self.n < 1):
            self.n += 0.001
        else:
            self.n = 0
        self.draw()
