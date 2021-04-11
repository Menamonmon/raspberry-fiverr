from config import *

with open("./screen_info.txt", "r") as f:
    screen_width, screen_height, isHorizontal = map(
        int, f.readline().split(","))

normal_prayers = ['FAJAR', 'SUNRISE', 'MAGHRIB', 'ASAR', 'MAGHRIB', 'ISHA']
friday_prayers = ['FAJAR', 'SUNRISE', 'JUMMAH', 'ASAR', 'MAGHRIB', 'ISHA']

# Prayers Arrays
prayers = ['FAJAR', 'ZUHR', 'ASAR', 'MAGHRIB', 'ISHA']
arabic_prayers = ["فجر", "ظهر", "عصر", "مغرب", "عشاء"]

# Background and Foregounrd Colors
WHITE = "#ffffff"
BLACK = "#000000"
GREY = "#cccccc"
LIGHT_GREY = "#f0f0f0"
RED = "#FF0000"
separator_bg = "#693821"

# Fonts
if isHorizontal:
    dateFont = ("Arial", int(screen_height/40), "bold")
    titleFont = ("Arial", int(screen_height/17), "bold")
    timeFont = ("Arial", int(screen_height/13), "bold")
    bigNextFont = ("Times", int(screen_height/4), "bold")
    bigishNextFont = ("Times", int(screen_height/8), "bold")
    nextFont = ("Times", int(screen_height/10), "bold")
    smallNextFont = ("Times", int(screen_height/20), "bold")

    big_timesFont = ("Arial", int(screen_height/20), "bold")
    timesFont = ("Arial", int(screen_height/30), "bold")
    smallTimesFont = dateFont

    noPhoneFont = ("Arial", int(screen_height/12), "bold")
    noPhoneFontBigger = ("Arial", int(screen_height/8), "bold")

    addressFont = ("Arial", int(screen_height/35), "bold")
else:
    atFont = ("Arial", int(screen_width / 54))
    dateFont = ("Arial", int(screen_width / 32), "bold")
    timeFont = ("Arial", int(screen_width / 15))
    prayerFont = ("Arial", int(screen_width / 25), "bold")
    prayerBottomFont = ("Arial", int(screen_width / 30), "bold")
    prayerBottomFontTime = ("Arial", int(screen_width / 18))
    prayerTimeFont = ("Arial", int(screen_width / 15), "bold")
    noPhoneFont = ("Arial", int(screen_width / 12), "bold")
    noPhonePrayerFont = ("Arial", int(screen_width / 16), "bold")
    countdownFont = ("Arial", int(screen_width / 5))
    athanFont = ("Arial", int(screen_width / 15))
    hadithPrayerFont = ("Arial", int(screen_width / 24), "bold")


# Tkinter directions
N = "n"
S = "s"
E = "e"
W = "w"
NE = "ne"
NW = "nw"
SE = "se"
SW = "sw"
C = "center"
CENTER = C