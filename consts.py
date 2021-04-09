from config import *

with open("./screen_info.txt", "r") as f:
    screen_width, screen_height = map(int, f.readline().split(","))

normal_prayers = ['FAJAR', 'SUNRISE', 'MAGHRIB', 'ASAR', 'MAGHRIB', 'ISHA']
friday_prayers = ['FAJAR', 'SUNRISE', 'JUMMAH', 'ASAR', 'MAGHRIB', 'ISHA']

# Prayers Arrays
prayers = ['FAJAR', 'ZUHR', 'ASAR', 'MAGHRIB', 'ISHA']
arabic_prayers = ["فجر", "ظهر", "عصر", "مغرب", "عشاء"]

# Background and Foregounrd Colors
WHITE = "#ffffff"
BLACK = "#000000"
RED = "#FF0000"
separator_bg = "#693821"

# Fonts
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
