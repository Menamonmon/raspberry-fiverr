import tkinter as tk
import csv
from config import *
import pygame
import os

isHorizontal = orientation == "Horizontal"
isDebugging = True

master = tk.Tk()

screen_height = master.winfo_screenheight()
screen_width = master.winfo_screenwidth() 

master.geometry(f"{screen_width}x{screen_height}+0+0")
if not isDebugging:
    master.attributes("-fullscreen", True)

with open("./screen_info.txt", "w") as f:
    f.writelines(f"{screen_width},{screen_height},{int(isHorizontal)}")

# Importing the helper files after saving the screen info into screen_info.txt
from events import *
from consts import *
from title_scroller import TitleScroller
from horizontal_helpers import *
from horizontal_images import *

os.remove("./screen_info.txt")

master.bind("<Escape>", lambda event: kill_window(master))
csv_rows = read_csv_rows("csv/Full2020csv.csv")

def horizontal_app():
    # Loading the varaibles that will be used by both modes
    gregorianDateVar = tk.StringVar()
    islamicDateVar = tk.StringVar()
    titleVar = tk.StringVar()
    titleVar.set("MASJID ALFURQAN")
    timeVar = tk.StringVar()



    # String Variables
    nextPrayerVar = tk.StringVar()
    nextPrayerArabicVar = tk.StringVar()
    nextPrayerTimeVar = tk.StringVar()
    blinkColor = tk.StringVar()
    seherVar = tk.StringVar()
    countdownVar = tk.StringVar()

    master.configure(background=WHITE)
    # master.configure(foreground=BLACK)
    blinkColor.set(BLACK)

    def text_label(textvar, font, bg=WHITE, fg=BLACK):
        return tk.Label(master, textvariable=textvar, font=font, bg=bg, fg=bg)

    # logoLabelLeft = tk.Label(master, image=renderL, anchor=w bg=WHITE)
    # logoLabelLeft.image = renderL
    logoLabelRight = tk.Label(master, image=renderR, anchor=E, bg=WHITE)
    logoLabelRight.image = renderR
    addressLabel = tk.Label(
        master, text="42 Great Southern St, Manchester M14 4EZ", bg=WHITE, font=addressFont)
    dateLabelGregorian = text_label(gregorianDateVar, dateFont)
    dateLabelIslamic = text_label(islamicDateVar, dateFont)
    # titleLabel = text_label(titleVar, titleFont)
    titleFrame = tk.Frame(master)
    timeLabel = text_label(timeVar, timeFont)
    largeTimerFrame = tk.Frame(master, bg=WHITE)
    nextLabel = tk.Label(largeTimerFrame, text="Next Salaah",
                            fg=BLACK, bg=WHITE, font=smallNextFont)
    nextPrayerLabel = tk.Label(largeTimerFrame, textvariable=nextPrayerVar,
                                fg=BLACK, bg=WHITE, font=bigishNextFont)
    nextPrayerArabicLabel = tk.Label(largeTimerFrame, textvariable=nextPrayerArabicVar,
                                        fg=BLACK, bg=WHITE, font=smallNextFont)
    nextPrayerTimeLabel = tk.Label(largeTimerFrame, textvariable=nextPrayerTimeVar,
                                    fg=BLACK, bg=WHITE, font=bigNextFont)
    countdownLabel = tk.Label(largeTimerFrame, textvariable=countdownVar,
                                fg=BLACK, bg=WHITE, font=smallNextFont)

    seherLabel = tk.Label(master, textvariable=seherVar,
                            fg=BLACK, bg=WHITE, font=big_timesFont)

    timesFrame = tk.Frame(master, bg=WHITE)

    def updatePrayerTimes():
        tm = time.localtime()
        yearDay = tm[7] - 1
        prayers = friday_prayers if tm[6] == 4 else normal_prayers
        keys = [('FAJR start', 'FAJR prayer'), ('SUN RISE', 'SUN RISE'), ('DUHR start', 'DUHR prayer'),
                ('ASAR start', 'ASAR prayer'), ('M/RIB start', 'M/RIB prayer'), ('ISHA start', 'ISHA prayer')]
        prayerTopLabel = tk.Label(timesFrame, text='Jamaat Times',
                                    fg=BLACK, bg=WHITE, font=timesFont)
        startTopLabel = tk.Label(timesFrame, text='Beginning Time',
                                    fg=BLACK, bg=WHITE, font=timesFont)
        prayerTopLabel.place(
            relx=(3/5), rely=0, relwidth=(2 / 5), relheight=(1 / (len(prayers)+1)))
        startTopLabel.place(relx=0, rely=0, relwidth=(
            2 / 5), relheight=(1 / (len(prayers)+1)))
        alreadyDone = 1
        nPrayer, _, _ = getNextPrayer(csv_rows)
        for index, prayer in enumerate(prayers):
            if (prayer == nPrayer):
                alreadyDone = 0
            pTime = csv_rows[yearDay+alreadyDone][keys[index][1]]
            phm = pTime.split(":")
            if clock24hr:
                phm = [int(phm[0]) + 12 * (index != 0 and index != 1 and (index !=
                                                                            2 or (index == 2 and phm[0] == "1"))), int(phm[1])]
            sTime = csv_rows[yearDay+alreadyDone][keys[index][0]]
            shm = sTime.split(":")
            if (clock24hr):
                shm = [int(shm[0]) + 12 * (index != 0 and index != 1 and (index !=
                                                                            2 or (index == 2 and shm[0] == "1"))), int(shm[1])]
            prayerLabel = tk.Label(timesFrame, text=str(phm[0]) + ":" + str(phm[1]).rjust(
                2, '0'), fg=BLACK, bg=WHITE, font=big_timesFont)
            nameLabel = tk.Label(timesFrame, text=prayer, fg=BLACK,
                                    bg=WHITE, font=big_timesFont)
            startLabel = tk.Label(timesFrame, text=str(shm[0]) + ":" + str(shm[1]).rjust(
                2, '0'), fg=BLACK, bg=WHITE, font=big_timesFont)
            prayerLabel.place(relx=(2.25/3), rely=((index+1)/(len(prayers)+1)),
                                relwidth=(0.75/3), relheight=(1/(len(prayers)+1)))
            nameLabel.place(relx=(0.75/3), rely=((index+1)/(len(prayers)+1)),
                            relwidth=(1.5/3), relheight=(1/(len(prayers)+1)))
            startLabel.place(relx=0, rely=((index+1)/(len(prayers)+1)),
                                relwidth=(0.75/3), relheight=(1/(len(prayers)+1)))
        sTime = csv_rows[yearDay+alreadyDone]['FAJR start']
        sTime = sTime.split(':')
        sTime[1] = str(int(sTime[1]) - 0)
        if (int(sTime[1]) < 0):
            sTime[0] = str(int(sTime[0]) - 1)
            sTime[1] = str(int(sTime[1]) + 60)
        seherVar.set("Suhoor end: " + sTime[0] + ":" + sTime[1].rjust(2, '0'))

    # logoLabelLeft.place(relx=0, rely=0, relwidth=(2/15), relheight=(2/15))
    addressLabel.place(relx=0.5, rely=(13/15), relwidth=0.5, relheight=(2/15))
    dateLabelGregorian.place(
        relx=0, rely=0, relwidth=(2.5/15), relheight=(1/15))
    dateLabelIslamic.place(relx=0, rely=(
        1/15), relwidth=(2.5/15), relheight=(1/15))
    titleFrame.place(relx=(2.5/15), rely=0,
                        relwidth=(8.85/15), relheight=(2/15))
    timeLabel.place(relx=(11.5/15), rely=0,
                    relwidth=(2.35/15), relheight=(2/15))

    largeTimerFrame.place(relx=0, rely=(2/15), relwidth=0.5, relheight=(11/15))
    nextLabel.place(relx=0, rely=0, relwidth=1, relheight=(0.75/5))
    nextPrayerLabel.place(relx=0, rely=(1.25/5), relwidth=1, relheight=(1.5/5))
    # nextPrayerArabicLabel.place(relx=0, rely=(3/5), relwidth=1, relheight=(0.5/5))
    nextPrayerTimeLabel.place(relx=0, rely=(
        2.75/5), relwidth=1, relheight=(2.25/5))
    countdownLabel.place(relx=0, rely=(0.75/5), relwidth=1, relheight=(0.5/5))

    timesFrame.place(relx=0.5, rely=(2/15), relwidth=0.5, relheight=(11/15))

    topSeparator = tk.Label(master, bg=separator_bg)
    topSeparator.place(relx=0, rely=(2/15), relwidth=1, relheight=(1/15)/5)
    bottomSeparator = tk.Label(master, bg=separator_bg)
    bottomSeparator.place(relx=0, rely=(13/15)-((1/15)/5),
                            relwidth=1, relheight=(1/15)/5)
    topLeftSeparator = tk.Label(master, bg=separator_bg)
    topLeftSeparator.place(relx=(2.5/15), rely=0,
                            relwidth=(1/15)/5, relheight=(2/15))
    topRightSeparator = tk.Label(master, bg=separator_bg)
    topRightSeparator.place(relx=(11.35/15), rely=0,
                            relwidth=(1/15)/5, relheight=(2/15))

    seherLabel.place(relx=0, rely=(13/15), relwidth=0.5, relheight=(2/15))
    logoLabelRight.place(relx=(13/15), rely=0,
                            relwidth=(2/15), relheight=(2/15))

    english_prayer, prayer_time, arabic_prayer = getNextPrayer(csv_rows)
    updatePrayerTimes()
    nextPrayerVar.set(english_prayer)
    # nextPrayerArabicVar.set(arabic_prayer)

    prayer_hour, prayer_minute = prayer_time
    prayer_time = datetime.time(hour=prayer_hour, minute=prayer_minute)
    next_prayer_time_str = prayer_time.strftime(
        f"{'%H' if clock24hr else '%I'}:%M")
    nextPrayerTimeVar.set(next_prayer_time_str)

    title = TitleScroller(titleFrame, "images/title.jpg")
    events = EventArray()
    if (int(time.time()) % 2 == 0 and blinkText(csv_rows)):
        nextPrayerTimeLabel.config(fg=RED)
    else:
        nextPrayerTimeLabel.config(fg=BLACK)

    tm = time.localtime()
    yearDay = tm[7] - 1
    dt = datetime.date.today()
    um = HijriDate(dt.year, dt.month, dt.day, gr=True)
    gregorianDateVar.set(getDayInfo(
        time.localtime()[7], csv_rows)['GregorianDate'])
    islamicDateVar.set(getDayInfo(
        time.localtime()[7], csv_rows)['IslamicDate'])
    updateClock(timeVar)
    if (int(time.time()) % 600 == 0):
        updatePrayerTimes()
    nextPrayerVar.set(getNextPrayer(csv_rows)[0])
    # nextPrayerArabicVar.set(getNextPrayer(csv_rows)[2])
    if (clock24hr):
        nextPrayerTimeVar.set("{}:{}".format(
            getNextPrayer(csv_rows)[1][0], str(getNextPrayer(csv_rows)[1][1]).rjust(2, '0')))
    else:
        if (getNextPrayer(csv_rows)[1][0] % 12 == 0):
            nextPrayerTimeVar.set("{}:{}".format(
                12, str(getNextPrayer(csv_rows)[1][1]).rjust(2, '0')))
        else:
            nextPrayerTimeVar.set("{}:{}".format(
                getNextPrayer(csv_rows)[1][0] % 12, str(getNextPrayer(csv_rows)[1][1]).rjust(2, '0')))

    playingSound = False
    pygame.mixer.init()
    audio_file = "./audio/prayerSound.wav"
    try:
        pygame.mixer.music.load(audio_file)
    except:
        pass

    noPhoneDisplayed = False

    while(True):
        if(int(time.time()*10) % 10 == 0):
            updateClock(timeVar)
            updateCountdown(csv_rows, countdownVar)
            if (int(time.time()) % 2 == 0 and blinkText(csv_rows)):
                nextPrayerTimeLabel.config(fg=RED)
                nextPrayerLabel.config(fg=RED)
                countdownLabel.config(fg=RED)
            else:
                nextPrayerTimeLabel.config(fg=BLACK)
                nextPrayerLabel.config(fg=BLACK)
                countdownLabel.config(fg=BLACK)
        if(silenceMobile(csv_rows)[0]):
            try:
                if(playingSound == False):
                    pygame.mixer.music.play()
                    playingSound = True
            except:
                pass
            if(noPhoneDisplayed == False):
                imageLabel = tk.Label(master, bg=BLACK, image=renderM)
                warningLabel = tk.Label(
                    master, text="Turn off/silence\nyour phone", bg=BLACK, fg=WHITE, font=noPhoneFont)
                prayerLabel = tk.Label(master, text=(str(silenceMobile(csv_rows)[
                    1]) + "\n" + silenceMobile(csv_rows)[2]), bg=BLACK, fg=WHITE, font=noPhoneFontBigger)
                imageLabel.place(relx=0, rely=0, relwidth=0.5, relheight=1)
                warningLabel.place(
                    relx=0.5, rely=0, relwidth=0.5, relheight=0.5)
                prayerLabel.place(relx=0.5, rely=0.5,
                                    relwidth=0.5, relheight=0.5)
                noPhoneDisplayed = True
        elif(int(time.time()*10) % 600 == 0):
            playingSound = False
            noPhoneDisplayed = False
            try:
                imageLabel.place_forget()
                warningLabel.place_forget()
                prayerLabel.place_forget()
            except:
                pass
            if (int(time.time()) % 600 == 0):
                updatePrayerTimes()
                tm = time.localtime()
                yearDay = tm[7] - 1
                dt = datetime.date.today()
                um = HijriDate(dt.year, dt.month, dt.day, gr=True)
                gregorianDateVar.set(
                    "{}/{}/{}".format(dt.day, dt.month, dt.year))
                islamicDateVar.set(
                    "{}/{}/{}".format(um.day, um.month, um.year))
            nextPrayerVar.set(getNextPrayer(csv_rows)[0])
            # nextPrayerArabicVar.set(getNextPrayer(csv_rows)[2])
            if (clock24hr):
                nextPrayerTimeVar.set("{}:{}".format(
                    getNextPrayer(csv_rows)[1][0], str(getNextPrayer(csv_rows)[1][1]).rjust(2, '0')))
            else:
                if (getNextPrayer(csv_rows)[1][0] % 12 == 0):
                    nextPrayerTimeVar.set("{}:{}".format(
                        12, str(getNextPrayer(csv_rows)[1][1]).rjust(2, '0')))
                else:
                    nextPrayerTimeVar.set("{}:{}".format(
                        getNextPrayer(csv_rows)[1][0] % 12, str(getNextPrayer(csv_rows)[1][1]).rjust(2, '0')))
        try:
            events.showEvent()
        except:
            pass
        title.update()
        master.update_idletasks()
        master.update()
        time.sleep(0.01)
