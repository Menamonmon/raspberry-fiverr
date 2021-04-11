from PIL import Image, ImageTk
from consts import screen_height, screen_width

# loadL = Image.open("logo.png").resize((int(screen_height*(2/15)), int(screen_height*(2/15))))
# renderL = ImageTk.PhotoImage(loadL)
loadR = Image.open(
    "images/logo.png").resize((int(screen_height * (2/15)), int(screen_height*(2/15))))
renderR = ImageTk.PhotoImage(loadR)

loadM = Image.open("images/nophone.png").resize(
    (int(screen_width/2), int(screen_height)))
renderM = ImageTk.PhotoImage(loadM)
