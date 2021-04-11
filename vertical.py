import tkinter as tk
from PIL import Image, ImageTk
import csv
from config import *
import pygame
import os

isHorizontal = orientation == "Horizontal"
isDebugging = True

master = tk.Tk()

screen_height = master.winfo_screenheight() if False else 1000
screen_width = master.winfo_screenwidth() if False else 562

master.geometry(f"{screen_width}x{screen_height}+0+0")
if not isDebugging:
    master.attributes("-fullscreen", True)

# Saving config of data into a text file
with open("./screen_info.txt", "w") as f:
    f.writelines(f"{screen_width},{screen_height},{int(isHorizontal)}")

# Importing the helper files after saving the screen info into screen_info.txt
from vertical_helpers import *
from title_scroller import TitleScroller
from consts import *
from events import *
from vertical_images import *

os.remove("./screen_info.txt")

master.bind("<Escape>", lambda event: kill_window(master))
csv_rows = read_csv_rows("csv/Full2020csv.csv")

def vertical_app():
    gregorianDateVar = tk.StringVar()
    islamicDateVar = tk.StringVar()
    titleVar = tk.StringVar()
    titleVar.set("MASJID ALFURQAN")
    timeVar = tk.StringVar()
    jummahVar = tk.StringVar()
    seherVar = tk.StringVar()
    sunriseVar = tk.StringVar()
    zawalVar = tk.StringVar()
    athanVar = tk.StringVar()
    noPhoneVar = tk.StringVar()
    blackenVar = tk.StringVar()

    # Loading the sounds
    pygame.mixer.init()
    beginSound = pygame.mixer.Sound(config.beginSound)
    prayerSound = pygame.mixer.Sound(config.prayerSound)
    fridaySound = pygame.mixer.Sound(config.fridaySound)
    daySound = pygame.mixer.Sound(config.daySound)


    def blackenScreen():
        today = getDayInfo(time.localtime()[7], csv_rows)
        for row, start in enumerate(today["StartTimes"]):
            if (not row == 1 or not time.localtime()[6] == 4):
                currentSeconds = time.localtime(
                )[5] + time.localtime()[4] * 60 + time.localtime()[3] * 3600
                startSeconds = minuteTime(start) * 60
                dif = startSeconds - currentSeconds
                if (dif > 0 and dif <= 2*60):
                    athanVar.set("Athan Al " + today["PrayerNames"][row])
                    athanLabelArabic.config(image=blackenImages[row][1])
                    return True, dif
        for row, prayer in enumerate(today["PrayerTimes"]):
            if (not row == 1 or not time.localtime()[6] == 4):
                currentSeconds = time.localtime(
                )[5] + time.localtime()[4] * 60 + time.localtime()[3] * 3600
                startSeconds = minuteTime(prayer) * 60
                dif = startSeconds - currentSeconds
                if (dif > 0 and dif <= 2*60):
                    athanVar.set(today["PrayerNames"][row] + " prayer")
                    athanLabelArabic.config(image=blackenImages[row+7][1])
                    return True, dif
        currentSeconds = time.localtime(
        )[5] + time.localtime()[4] * 60 + time.localtime()[3] * 3600
        startSeconds = minuteTime(today["Sunrise"]) * 60
        dif = startSeconds - currentSeconds
        if (dif > 0 and dif <= 2 * 60):
            athanVar.set("Sunrise")
            athanLabelArabic.config(image=blackenImages[6][1])
            return True, dif
        athanVar.set("Nothing")
        athanLabelArabic.config(image=blackenImages[0][1])
        return False, 0 - (time.localtime()[5] + time.localtime()[4] * 60 + time.localtime()[3] * 3600)


    timeVar.set(currentStringTime())


    today = getDayInfo(time.localtime()[7], csv_rows)

    backLabel = tk.Label(master, bg=GREY)
    timeCanvas = tk.Canvas(master, width=int(master.winfo_screenwidth(
    ) / 2), height=int(master.winfo_screenheight()/10), bg=BLACK)
    gregorianDateLabel = tk.Label(
        master, textvariable=gregorianDateVar, bg=BLACK, fg=WHITE, font=dateFont)
    create_rounded_rect(timeCanvas, [int(master.winfo_screenwidth() / 2 * 0.1), int(master.winfo_screenheight() / 10 * 0.25), int(
        master.winfo_screenwidth() / 2 * 0.9), int(master.winfo_screenheight() / 10 * 0.95)], 16, WHITE)
    create_rounded_rect(timeCanvas, [int(master.winfo_screenwidth() / 2 * 0.105), int(master.winfo_screenheight() / 10 * 0.26), int(
        master.winfo_screenwidth() / 2 * 0.8975), int(master.winfo_screenheight() / 10 * 0.94)], 16, BLACK)
    timeText = timeCanvas.create_text([int(master.winfo_screenwidth(
    ) / 4), int(master.winfo_screenheight() / 17)], text="", fill=WHITE, font=timeFont)
    islamicDateLabel = tk.Label(
        master, textvariable=islamicDateVar, bg=BLACK, fg=WHITE, font=dateFont)
    headerFrame = tk.Frame(master)
    startHeaderLabel = tk.Label(
        headerFrame, text="BEGINNING", font=prayerFont, bg=WHITE)
    namesHeaderLabel = tk.Label(headerFrame, text="PRAYER",
                                font=prayerFont, bg=WHITE)
    prayerHeaderLabel = tk.Label(
        headerFrame, text="JAMAAT", font=prayerFont, bg=WHITE)
    startHeaderLabel.place(relx=0, rely=0, relwidth=1/3, relheight=1)
    namesHeaderLabel.place(relx=1/3, rely=0, relwidth=1/3, relheight=1)
    prayerHeaderLabel.place(relx=2/3, rely=0, relwidth=1/3, relheight=1)
    prayerFrames = []
    prayerArabicLabels = []
    prayerStartPrayerTimes = []
    prayerStringvars = []
    for row in range(5):
        tempFrame = tk.Frame(master)
        tmpArr = []
        sv = tk.StringVar()
        nv = tk.StringVar()
        pv = tk.StringVar()
        startLabel = tk.Label(tempFrame, textvariable=sv,
                            font=timeFont, bg=LIGHT_GREY)
        tmpArr.append(startLabel)
        startLabel.place(relx=0, rely=0, relwidth=1/3, relheight=1)
        nameFrame = tk.Frame(tempFrame)
        nameFrame.place(relx=1/3, rely=0, relwidth=1/3, relheight=1)
        arabicNameLabel = tk.Label(nameFrame, bg=LIGHT_GREY)
        arabicNameLabel.place(relx=0, rely=0, relwidth=1, relheight=0.5)
        prayerArabicLabels.append(arabicNameLabel)
        englishNameLabel = tk.Label(
            nameFrame, textvariable=nv, font=prayerFont, bg=LIGHT_GREY)
        englishNameLabel.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)
        prayerLabel = tk.Label(tempFrame, textvariable=pv,
                            font=timeFont, bg=LIGHT_GREY)
        tmpArr.append(prayerLabel)
        prayerLabel.place(relx=2/3, rely=0, relwidth=1/3, relheight=1)
        prayerStartPrayerTimes.append(tmpArr)
        stringvars = [sv, nv, pv]
        prayerFrames.append(tempFrame)
        prayerStringvars.append(stringvars)
    jummahFrame = tk.Frame(master)
    jummahLabelArabic = tk.Label(jummahFrame, image=renderjummah, bg=GREY)
    jummahLabel = tk.Label(jummahFrame, text="Jummah",
                        font=prayerBottomFont, bg=GREY)
    jummahLabelTime = tk.Label(
        jummahFrame, textvariable=jummahVar, font=prayerBottomFontTime, bg=GREY)
    jummahLabelArabic.place(relx=0, rely=0, relwidth=1, relheight=1/4)
    jummahLabel.place(relx=0, rely=1/4, relwidth=1, relheight=1/4)
    jummahLabelTime.place(relx=0, rely=1/2, relwidth=1, relheight=1/2)
    seherFrame = tk.Frame(master)
    seherLabelArabic = tk.Label(seherFrame, image=renderseher, bg=GREY)
    seherLabel = tk.Label(seherFrame, text="Seher End",
                        font=prayerBottomFont, bg=GREY)
    seherLabelTime = tk.Label(seherFrame, textvariable=seherVar,
                            font=prayerBottomFontTime, bg=GREY)
    seherLabelArabic.place(relx=0, rely=0, relwidth=1, relheight=1/4)
    seherLabel.place(relx=0, rely=1/4, relwidth=1, relheight=1/4)
    seherLabelTime.place(relx=0, rely=1/2, relwidth=1, relheight=1/2)
    sunriseFrame = tk.Frame(master)
    sunriseLabelArabic = tk.Label(sunriseFrame, image=rendersunrise, bg=GREY)
    sunriseLabel = tk.Label(sunriseFrame, text="Sunrise",
                            font=prayerBottomFont, bg=GREY)
    sunriseLabelTime = tk.Label(
        sunriseFrame, textvariable=sunriseVar, font=prayerBottomFontTime, bg=GREY)
    sunriseLabelArabic.place(relx=0, rely=0, relwidth=1, relheight=1/4)
    sunriseLabel.place(relx=0, rely=1/4, relwidth=1, relheight=1/4)
    sunriseLabelTime.place(relx=0, rely=1/2, relwidth=1, relheight=1/2)
    zawalFrame = tk.Frame(master)
    zawalLabelArabic = tk.Label(zawalFrame, image=renderzawal, bg=GREY)
    zawalLabel = tk.Label(zawalFrame, text="Zawal",
                        font=prayerBottomFont, bg=GREY)
    zawalLabelTime = tk.Label(zawalFrame, textvariable=zawalVar,
                            font=prayerBottomFontTime, bg=GREY)
    zawalLabelArabic.place(relx=0, rely=0, relwidth=1, relheight=1/4)
    zawalLabel.place(relx=0, rely=1/4, relwidth=1, relheight=1/4)
    zawalLabelTime.place(relx=0, rely=1/2, relwidth=1, relheight=1/2)
    bottomLabelArabic = tk.Label(master, bg=BLACK,
                                image=rendertitle, fg=WHITE, anchor=S)
    bottomLabelEnglish = tk.Label(master, bg=BLACK, text="MASJID ALFURQAN",
                                fg=WHITE, font=prayerBottomFont, anchor=N)
    logoLabel = tk.Label(master, bg=BLACK, image=renderLogo)
    socialFrame = tk.Frame(master, bg=BLACK)
    fbLabel = tk.Label(socialFrame, image=renderfb, bg=BLACK)
    fbLabel.place(relx=0, rely=0, relwidth=0.5, relheight=0.4)
    twLabel = tk.Label(socialFrame, image=rendertw, bg=BLACK)
    twLabel.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.4)
    inLabel = tk.Label(socialFrame, image=renderin, bg=BLACK)
    inLabel.place(relx=0, rely=0.4, relwidth=0.5, relheight=0.4)
    ytLabel = tk.Label(socialFrame, image=renderyt, bg=BLACK)
    ytLabel.place(relx=0.5, rely=0.4, relwidth=0.5, relheight=0.4)
    atLabel = tk.Label(master, text="@AlfurqanMCR",
                    fg=WHITE, bg=BLACK, font=atFont)

    hadithArabicLabel = tk.Label(master, image=renderhadith, bg=BLACK)
    hadithLabel = tk.Label(master, text="The messenger of Allah (peace be\n upon him) said, \"When the Imam\n is delivering the Khutba, and\n you ask your companion to\n keep quiet and listen, then no\n doubt you have done an evil act.\"",
                        bg=BLACK, fg=WHITE, font=hadithPrayerFont)
    imageLabel = tk.Label(master, bg=BLACK, image=renderNoPhone)
    warningLabel = tk.Label(master, text="Turn off/silence\nyour phone",
                            bg=BLACK, fg=WHITE, font=noPhoneFont)
    prayerLabel = tk.Label(master, textvariable=noPhoneVar,
                        bg=BLACK, fg=WHITE, font=noPhonePrayerFont)

    athanLabel = tk.Label(master, textvariable=athanVar,
                        bg=BLACK, fg=WHITE, font=athanFont, anchor=S)
    athanLabelArabic = tk.Label(master, bg=BLACK,
                                fg=WHITE, font=athanFont, anchor=N)
    blackLabel = tk.Label(master, textvariable=blackenVar,
                        bg=BLACK, fg=WHITE, font=countdownFont)
    athanImageLabel = tk.Label(master, bg=BLACK,
                            fg=WHITE, image=renderNoPhoneAthan)


    # Rendering functions
    def blackenScreen():
        today = getDayInfo(time.localtime()[7], csv_rows)
        for row, start in enumerate(today["StartTimes"]):
            if (not row == 1 or not time.localtime()[6] == 4):
                currentSeconds = time.localtime(
                )[5] + time.localtime()[4] * 60 + time.localtime()[3] * 3600
                startSeconds = minuteTime(start) * 60
                dif = startSeconds - currentSeconds
                if (dif > 0 and dif <= 2*60):
                    athanVar.set("Athan Al " + today["PrayerNames"][row])
                    athanLabelArabic.config(image=blackenImages[row][1])
                    return True, dif
        for row, prayer in enumerate(today["PrayerTimes"]):
            if (not row == 1 or not time.localtime()[6] == 4):
                currentSeconds = time.localtime(
                )[5] + time.localtime()[4] * 60 + time.localtime()[3] * 3600
                startSeconds = minuteTime(prayer) * 60
                dif = startSeconds - currentSeconds
                if (dif > 0 and dif <= 2*60):
                    athanVar.set(today["PrayerNames"][row] + " prayer")
                    athanLabelArabic.config(image=blackenImages[row+7][1])
                    return True, dif
        currentSeconds = time.localtime(
        )[5] + time.localtime()[4] * 60 + time.localtime()[3] * 3600
        startSeconds = minuteTime(today["Sunrise"]) * 60
        dif = startSeconds - currentSeconds
        if (dif > 0 and dif <= 2 * 60):
            athanVar.set("Sunrise")
            athanLabelArabic.config(image=blackenImages[6][1])
            return True, dif
        athanVar.set("Nothing")
        athanLabelArabic.config(image=blackenImages[0][1])
        return False, 0 - (time.localtime()[5] + time.localtime()[4] * 60 + time.localtime()[3] * 3600)


    def updateStringvars():
        today = getDayInfo(time.localtime()[7], csv_rows)
        islamicDateVar.set(today["IslamicDate"])
        tomorrow = getDayInfo(time.localtime()[7] + 1, csv_rows)
        gregorianDateVar.set(today["GregorianDate"])
        keys = ["StartTimes", "PrayerNames", "PrayerTimes"]
        timeVar.set(currentStringTime())
        for row in range(5):
            for col, key in enumerate(keys):
                try:
                    if (not alreadyDone(today[key][row])):
                        prayerStringvars[row][col].set(today[key][row])
                    else:
                        prayerStringvars[row][col].set(tomorrow[key][row])
                except:
                    if (not alreadyDone(today["PrayerTimes"][row])):
                        prayerStringvars[row][col].set(today[key][row])
                    else:
                        prayerStringvars[row][col].set(tomorrow[key][row])
        for row, label in enumerate(prayerArabicLabels):
            if ((row == 1 and alreadyDone(today["PrayerTimes"][row]) and time.localtime()[6] == 3) or (row == 1 and time.localtime()[6] == 4) and not alreadyDone(today["PrayerTimes"][row])):
                row = 5
            label.config(image=prayerImages[row][1])
        jummahVar.set(stringTime(minuteTime(
            today["PrayerTimes"][1])-config.jummahLength))
        if (not alreadyDone(today["StartTimes"][0])):
            seherVar.set(today["Seher"])
        else:
            seherVar.set(tomorrow["Seher"])
        sunriseVar.set(today["Sunrise"])
        zawalVar.set(stringTime(minuteTime(today["StartTimes"][1])-10))

        try:
            noPhoneVar.set(str(silenceMobile(csv_rows)[
                        0]) + "\n" + silenceMobile(csv_rows)[1])
        except:
            print(silenceMobile(csv_rows))
        nextIndex = 0
        try:
            while (minuteTime(today["StartTimes"][nextIndex]) < minuteTime(currentStringTime())):
                nextIndex += 1
        except:
            nextIndex = 0

        blackenVar.set(str(int(blackenScreen()[
            1]/60 % 60)) + ":" + str(int(blackenScreen()[1] % 60)).rjust(2, "0"))


    def updateColors():
        today = getDayInfo(time.localtime()[7], csv_rows)
        for row, start in enumerate(today["StartTimes"]):
            if (minuteTime(currentStringTime()) < minuteTime(start) and minuteTime(start) - minuteTime(
                    currentStringTime()) < 2 and int(time.time()) % 2 == 0):
                prayerStartPrayerTimes[row][0].config(fg=RED)
            else:
                prayerStartPrayerTimes[row][0].config(fg=BLACK)
        for row, prayer in enumerate(today["PrayerTimes"]):
            if (minuteTime(currentStringTime()) < minuteTime(prayer) and minuteTime(prayer) - minuteTime(
                    currentStringTime()) < 2 and int(time.time()) % 2 == 0):
                prayerStartPrayerTimes[row][1].config(fg=RED)
            else:
                prayerStartPrayerTimes[row][1].config(fg=BLACK)
        if (int(time.time()) % 2 == 0):
            blackLabel.config(fg=RED)
        else:
            blackLabel.config(fg=LIGHT_GREY)


    def placeRegularScreen():
        backLabel.place(relx=0, rely=0, relwidth=1, relheight=1)
        timeCanvas.place(relx=0.24, rely=-0.01, relwidth=0.52, relheight=0.12)
        gregorianDateLabel.place(relx=0, rely=0, relwidth=0.25, relheight=0.1)
        islamicDateLabel.place(relx=0.75, rely=0, relwidth=0.25, relheight=0.1)
        headerFrame.place(relx=0, rely=0.1, relwidth=1, relheight=0.05)
        for row in range(5):
            prayerFrames[row].place(
                relx=0, rely=0.15 + ((0.6 * row) / 5), relwidth=1, relheight=0.59 / 5)
        jummahFrame.place(relx=0, rely=0.75, relwidth=0.25, relheight=0.125)
        seherFrame.place(relx=0.25, rely=0.75, relwidth=0.25, relheight=0.125)
        sunriseFrame.place(relx=0.5, rely=0.75, relwidth=0.25, relheight=0.125)
        zawalFrame.place(relx=0.75, rely=0.75, relwidth=0.25, relheight=0.125)
        logoLabel.place(relx=0, rely=0.875, relwidth=0.2, relheight=0.125)
        socialFrame.place(relx=0.775, rely=0.875,
                        relwidth=0.2, relheight=0.105)
        atLabel.place(relx=0.775, rely=0.965, relwidth=0.2, relheight=0.02)
        bottomLabelArabic.place(
            relx=0, rely=0.875, relwidth=1, relheight=0.125/2)
        bottomLabelEnglish.place(
            relx=0, rely=0.875+(0.125/2), relwidth=1, relheight=0.125/2)


    def forgetRegularScreen():
        backLabel.place_forget()
        gregorianDateLabel.place_forget()
        timeCanvas.place_forget()
        islamicDateLabel.place_forget()
        headerFrame.place_forget()
        for row in range(5):
            prayerFrames[row].place_forget()
        jummahFrame.place_forget()
        seherFrame.place_forget()
        sunriseFrame.place_forget()
        zawalFrame.place_forget()
        logoLabel.place_forget()
        bottomLabelEnglish.place_forget()
        bottomLabelArabic.place_forget()
        atLabel.place_forget()
        socialFrame.place_forget()


    def placeNoMobile():
        imageLabel.place(relx=0, rely=2/5, relwidth=1, relheight=1/5)
        warningLabel.place(relx=0, rely=0, relwidth=1, relheight=2/5)
        prayerLabel.place(relx=0, rely=3/5, relwidth=1, relheight=2/5)


    def forgetNoMobile():
        imageLabel.place_forget()
        warningLabel.place_forget()
        prayerLabel.place_forget()


    def placeNoMobileHadith():
        hadithArabicLabel.place(relx=0, rely=0/5, relwidth=1, relheight=1/10)
        hadithLabel.place(relx=0, rely=1/10, relwidth=1, relheight=3/10)
        imageLabel.place(relx=0, rely=3/5, relwidth=1, relheight=1/5)
        warningLabel.place(relx=0, rely=2/5, relwidth=1, relheight=1/5)
        prayerLabel.place(relx=0, rely=4/5, relwidth=1, relheight=1/5)


    def forgetNoMobileHadith():
        hadithArabicLabel.place_forget()
        hadithLabel.place_forget()
        imageLabel.place_forget()
        warningLabel.place_forget()
        prayerLabel.place_forget()


    def placeNoScreen():
        blackLabel.place(relx=0, rely=2/3, relwidth=1, relheight=1/3)
        athanLabel.place(relx=0, rely=0, relwidth=1, relheight=1/6)
        athanImageLabel.place(relx=0, rely=1/3, relwidth=1, relheight=1/3)
        athanLabelArabic.place(relx=0, rely=1/6, relwidth=1, relheight=1/6)


    def forgetNoScreen():
        blackLabel.place_forget()
        athanLabel.place_forget()
        athanLabelArabic.place_forget()
        athanImageLabel.place_forget()


    prev = -1
    curr = 1
    fridayCooldown = False
    dayCooldown = False

    while (True):
        current_time = datetime.datetime.fromtimestamp(time.mktime(time.localtime()))
        timeCanvas.itemconfig(timeText, text=f"{current_time.hour:02}:{current_time.minute:02}:{current_time.second:02}")
        updateStringvars()
        updateColors()

        if time.localtime()[6] == 4 and minuteTime(config.fridaySoundTime) == minuteTime(currentStringTime()):
            if fridayCooldown == False:
                fridaySound.play()
            fridayCooldown = True
        else:
            fridayCooldown = False

        if time.localtime()[6] != 4 and minuteTime(config.daySoundTime) == minuteTime(currentStringTime()):
            if dayCooldown == False:
                fridaySound.play()
            dayCooldown = True
        else:
            dayCooldown = False

        if (silenceMobile(csv_rows)[0]):
            curr = 2
        elif (blackenScreen()[0]):
            curr = 1
        else:
            curr = 0
        if (curr != prev):
            if (curr == 0):
                if (prev == 1):
                    beginSound.play()
                forgetNoScreen()
                forgetNoMobileHadith()
                placeRegularScreen()
            elif (curr == 1):
                forgetRegularScreen()
                forgetNoMobileHadith()
                placeNoScreen()
            elif (curr == 2):
                prayerSound.play()
                if (silenceMobile(csv_rows)[5]):
                    forgetRegularScreen()
                    forgetNoScreen()
                    placeNoMobileHadith()
                else:
                    forgetRegularScreen()
                    forgetNoScreen()
                    placeNoMobile()
        prev = curr
        master.update_idletasks()
        master.update()

# csv_rows = []


# clock24hr = config.clock24hr

# with open('Full2020csv.csv') as csvFile:
#     reader = csv.DictReader(csvFile)
#     for row in reader:
#         csv_rows.append(row)

# master = Tk()
# master.geometry(
#     "{0}x{1}+0+0".format(master.winfo_screenwidth(), master.winfo_screenheight()))
# master.attributes("-fullscreen", True)

# blackenImages = []
# blackenImageKeys = ['fajar', 'zuhr', 'asar',
#                     'maghrib', 'isha', "seher", "sunrise"]
# for i in range(7):
#     tmpArr = []
#     tmpArr.append(Image.open(f"images/{blackenImageKeys[0]} Athan.png").resize(
#         (int(master.winfo_screenwidth() * 0.4), int(master.winfo_screenheight() * 0.075))))
#     tkImage = ImageTk.PhotoImage(tmpArr[0])
#     tmpArr.append(tkImage)
#     l = tk.Label(master)
#     l.image = tkImage
#     blackenImages.append(tmpArr)
# for i in range(5):
#     tmpArr = []
#     tmpArr.append(Image.open("images/{blackenImageKeys[i]}Prayer.png").resize(
#         (int(master.winfo_screenwidth() * 0.4), int(master.winfo_screenheight() * 0.075))))
#     tkImage = ImageTk.PhotoImage(tmpArr[0])
#     tmpArr.append(tkImage)
#     l = tk.Label(master)
#     l.image = tkImage
#     blackenImages.append(tmpArr)

# prayerImages = []
# prayerImageKeys = ['fajar', 'zuhr', 'asar', 'maghrib', 'isha', 'jummah']
# for i in range(6):
#     tmpArr = []
#     tmpArr.append(Image.open("images/{prayerImageKeys[i]}Arabic.png").resize(
#         (int(master.winfo_screenwidth() * 0.175), int(master.winfo_screenheight() * 0.033))))
#     tkImage = ImageTk.PhotoImage(tmpArr[0])
#     tmpArr.append(tkImage)
#     l = tk.Label(master)
#     l.image = tkImage
#     prayerImages.append(tmpArr)

# def killWindow(event):
#     master.destroy()

# master.bind("<Escape>", killWindow)

# loadLogo = Image.open("images/logoNoText.png").resize(
#     (int(master.winfo_screenheight() * (0.1125)), int(master.winfo_screenheight() * (0.1125))))
# renderLogo = ImageTk.PhotoImage(loadLogo)

# loadNoPhone = Image.open("images/nophone.png").resize(
#     (int(master.winfo_screenwidth() / 3), int(master.winfo_screenwidth() / 3)))
# renderNoPhone = ImageTk.PhotoImage(loadNoPhone)

# loadNoPhoneAthan = Image.open("images/nophone.png").resize(
#     (int(master.winfo_screenheight() / 3), int(master.winfo_screenheight() / 3)))
# renderNoPhoneAthan = ImageTk.PhotoImage(loadNoPhoneAthan)

# loadfb = Image.open("images/facebook.png").resize(
#     (int(master.winfo_screenheight() * 0.03), int(master.winfo_screenheight() * 0.03)))
# renderfb = ImageTk.PhotoImage(loadfb)
# loadtw = Image.open("images/twitter.png").resize(
#     (int(master.winfo_screenheight() * 0.03), int(master.winfo_screenheight() * 0.03)))
# rendertw = ImageTk.PhotoImage(loadtw)
# loadin = Image.open("images/instagram.png").resize(
#     (int(master.winfo_screenheight() * 0.03), int(master.winfo_screenheight() * 0.03)))
# renderin = ImageTk.PhotoImage(loadin)
# loadyt = Image.open("images/youtube.png").resize(
#     (int(master.winfo_screenheight() * 0.03), int(master.winfo_screenheight() * 0.03)))
# renderyt = ImageTk.PhotoImage(loadyt)
# loadjummah = Image.open("images/jummahArabic.png").resize(
#     (int(master.winfo_screenwidth() * 0.175), int(master.winfo_screenheight() * 0.033)))
# renderjummah = ImageTk.PhotoImage(loadjummah)
# loadseher = Image.open("images/seherArabic.png").resize(
#     (int(master.winfo_screenwidth() * 0.175), int(master.winfo_screenheight() * 0.033)))
# renderseher = ImageTk.PhotoImage(loadseher)
# loadsunrise = Image.open("images/sunriseArabic.png").resize(
#     (int(master.winfo_screenwidth() * 0.175), int(master.winfo_screenheight() * 0.033)))
# rendersunrise = ImageTk.PhotoImage(loadsunrise)
# loadzawal = Image.open("images/zawalArabic.png").resize(
#     (int(master.winfo_screenwidth() * 0.175), int(master.winfo_screenheight() * 0.033)))
# renderzawal = ImageTk.PhotoImage(loadzawal)
# loadtitle = Image.open("images/titleArabic.png").resize(
#     (int(master.winfo_screenwidth() * 0.4), int(master.winfo_screenheight() * 0.05)))
# rendertitle = ImageTk.PhotoImage(loadtitle)
# loadhadith = Image.open("images/hadithArabic.png").resize(
#     (int(master.winfo_screenwidth() * 0.9), int(master.winfo_screenheight() * 0.1)))
# renderhadith = ImageTk.PhotoImage(loadhadith)
# gregorianDateVar = tk.StringVar()
# islamicDateVar = tk.StringVar()
# titleVar = tk.StringVar()
# titleVar.set("MASJID ALFURQAN")
# timeVar = tk.StringVar()
# jummahVar = tk.StringVar()
# seherVar = tk.StringVar()
# sunriseVar = tk.StringVar()
# zawalVar = tk.StringVar()
# athanVar = tk.StringVar()
# noPhoneVar = tk.StringVar()
# blackenVar = tk.StringVar()

# atFont = ("Arial", int(master.winfo_screenwidth() / 54))
# dateFont = ("Arial", int(master.winfo_screenwidth() / 32), "bold")
# timeFont = ("Arial", int(master.winfo_screenwidth() / 15))
# prayerFont = ("Arial", int(master.winfo_screenwidth() / 25), "bold")
# prayerBottomFont = ("Arial", int(master.winfo_screenwidth() / 30), "bold")
# prayerBottomFontTime = ("Arial", int(master.winfo_screenwidth() / 18))
# prayerTimeFont = ("Arial", int(master.winfo_screenwidth() / 15), "bold")
# noPhoneFont = ("Arial", int(master.winfo_screenwidth() / 12), "bold")
# noPhonePrayerFont = ("Arial", int(master.winfo_screenwidth() / 16), "bold")
# countdownFont = ("Arial", int(master.winfo_screenwidth() / 5))
# athanFont = ("Arial", int(master.winfo_screenwidth() / 15))
# hadithPrayerFont = ("Arial", int(master.winfo_screenwidth() / 24), "bold")

# def isRamadan():
#     tm = time.localtime()
#     yearDay = tm[7] - 1
#     leap = (tm[0] % 4 == 0)
#     return (yearDay >= 112 + leap and yearDay <= 142 + leap)

# def silenceMobile(csv_rows):
#     today = getDayInfo(time.localtime()[7], csv_rows)
#     prayerTimes = today['PrayerTimes']
#     currentTime = minuteTime(currentStringTime())
#     if (time.localtime()[6] == 4 and minuteTime(currentStringTime()) >= minuteTime(config.fridayPrayerStart) and minuteTime(currentStringTime()) < minuteTime(config.fridayPrayerEnd)):
#         return True, "{}:{}:{}".format(time.localtime()[3], str(time.localtime()[4]).rjust(2, "0"), str(time.localtime()[5]).rjust(2, "0")), "Asar\n" + str(today['StartTimes'][2]), "1st", "2nd", True
#     for index, prayerTime in enumerate(prayerTimes):
#         prayerTime = minuteTime(prayerTime)
#         if (currentTime - prayerTime < config.noMobileTimes[index] and currentTime - prayerTime >= 0):
#             return True, today['PrayerNames'][index], stringTime(prayerTime), "None", "None", False
#     return False, "No Prayer", "No Time", "None", "None", False

# def blackenScreen():
#     today = getDayInfo(time.localtime()[7], csv_rows)
#     for row, start in enumerate(today["StartTimes"]):
#         if (not row == 1 or not time.localtime()[6] == 4):
#             currentSeconds = time.localtime(
#             )[5] + time.localtime()[4] * 60 + time.localtime()[3] * 3600
#             startSeconds = minuteTime(start) * 60
#             dif = startSeconds - currentSeconds
#             if (dif > 0 and dif <= 2*60):
#                 athanVar.set("Athan Al " + today["PrayerNames"][row])
#                 athanLabelArabic.config(image=blackenImages[row][1])
#                 return True, dif
#     for row, prayer in enumerate(today["PrayerTimes"]):
#         if (not row == 1 or not time.localtime()[6] == 4):
#             currentSeconds = time.localtime(
#             )[5] + time.localtime()[4] * 60 + time.localtime()[3] * 3600
#             startSeconds = minuteTime(prayer) * 60
#             dif = startSeconds - currentSeconds
#             if (dif > 0 and dif <= 2*60):
#                 athanVar.set(today["PrayerNames"][row] + " prayer")
#                 athanLabelArabic.config(image=blackenImages[row+7][1])
#                 return True, dif
#     currentSeconds = time.localtime(
#     )[5] + time.localtime()[4] * 60 + time.localtime()[3] * 3600
#     startSeconds = minuteTime(today["Sunrise"]) * 60
#     dif = startSeconds - currentSeconds
#     if (dif > 0 and dif <= 2 * 60):
#         athanVar.set("Sunrise")
#         athanLabelArabic.config(image=blackenImages[6][1])
#         return True, dif
#     athanVar.set("Nothing")
#     athanLabelArabic.config(image=blackenImages[0][1])
#     return False, 0 - (time.localtime()[5] + time.localtime()[4] * 60 + time.localtime()[3] * 3600)

# timeVar.set(currentStringTime())

# def alreadyDone(prayerTime):
#     return (minuteTime(prayerTime) < minuteTime(currentStringTime()))

# def create_rounded_rect(c, bounding_box, radius, color):
#     c.create_arc([bounding_box[0], bounding_box[1], bounding_box[0] + radius * 2, bounding_box[1] + radius * 2],
#                  start=90, fill=color, outline=color)
#     c.create_arc([bounding_box[0], bounding_box[3], bounding_box[0] + radius * 2, bounding_box[3] - radius * 2],
#                  start=180, fill=color, outline=color)
#     c.create_arc([bounding_box[2], bounding_box[1], bounding_box[2] - radius * 2, bounding_box[1] + radius * 2],
#                  start=0, fill=color, outline=color)
#     c.create_arc([bounding_box[2], bounding_box[3], bounding_box[2] - radius * 2, bounding_box[3] - radius * 2],
#                  start=270, fill=color, outline=color)
#     c.create_rectangle([bounding_box[0], bounding_box[1] + radius, bounding_box[2], bounding_box[3] - radius],
#                        fill=color, outline=color)
#     c.create_rectangle(
#         [bounding_box[0] + radius, bounding_box[1], bounding_box[2] - radius, bounding_box[1] + radius], fill=color,
#         outline=color)
#     c.create_rectangle(
#         [bounding_box[0] + radius, bounding_box[3], bounding_box[2] - radius, bounding_box[3] - radius], fill=color,
#         outline=color)

# today = getDayInfo(time.localtime()[7], csv_rows)

# backLabel = tk.Label(master, bg=GREY)
# timeCanvas = tk.Canvas(master, width=int(master.winfo_screenwidth(
# ) / 2), height=int(master.winfo_screenheight()/10), bg=BLACK)
# gregorianDateLabel = tk.Label(
#     master, textvariable=gregorianDateVar, bg=BLACK, fg=WHITE, font=dateFont)
# create_rounded_rect(timeCanvas, [int(master.winfo_screenwidth() / 2 * 0.1), int(master.winfo_screenheight() / 10 * 0.25), int(
#     master.winfo_screenwidth() / 2 * 0.9), int(master.winfo_screenheight() / 10 * 0.95)], 16, WHITE)
# create_rounded_rect(timeCanvas, [int(master.winfo_screenwidth() / 2 * 0.105), int(master.winfo_screenheight() / 10 * 0.26), int(
#     master.winfo_screenwidth() / 2 * 0.8975), int(master.winfo_screenheight() / 10 * 0.94)], 16, BLACK)
# timeText = timeCanvas.create_text([int(master.winfo_screenwidth(
# ) / 4), int(master.winfo_screenheight() / 17)], text="", fill=WHITE, font=timeFont)
# islamicDateLabel = tk.Label(
#     master, textvariable=islamicDateVar, bg=BLACK, fg=WHITE, font=dateFont)
# headerFrame = tk.Frame(master)
# startHeaderLabel = tk.Label(
#     headerFrame, text="BEGINNING", font=prayerFont, bg=WHITE)
# namesHeaderLabel = tk.Label(headerFrame, text="PRAYER",
#                             font=prayerFont, bg=WHITE)
# prayerHeaderLabel = tk.Label(
#     headerFrame, text="JAMAAT", font=prayerFont, bg=WHITE)
# startHeaderLabel.place(relx=0, rely=0, relwidth=1/3, relheight=1)
# namesHeaderLabel.place(relx=1/3, rely=0, relwidth=1/3, relheight=1)
# prayerHeaderLabel.place(relx=2/3, rely=0, relwidth=1/3, relheight=1)
# prayerFrames = []
# prayerArabicLabels = []
# prayerStartPrayerTimes = []
# prayerStringvars = []
# for row in range(5):
#     tempFrame = tk.Frame(master)
#     tmpArr = []
#     sv = tk.StringVar()
#     nv = tk.StringVar()
#     pv = tk.StringVar()
#     startLabel = tk.Label(tempFrame, textvariable=sv,
#                           font=timeFont, bg=LIGHT_GREY)
#     tmpArr.append(startLabel)
#     startLabel.place(relx=0, rely=0, relwidth=1/3, relheight=1)
#     nameFrame = tk.Frame(tempFrame)
#     nameFrame.place(relx=1/3, rely=0, relwidth=1/3, relheight=1)
#     arabicNameLabel = tk.Label(nameFrame, bg=LIGHT_GREY)
#     arabicNameLabel.place(relx=0, rely=0, relwidth=1, relheight=0.5)
#     prayerArabicLabels.append(arabicNameLabel)
#     englishNameLabel = tk.Label(
#         nameFrame, textvariable=nv, font=prayerFont, bg=LIGHT_GREY)
#     englishNameLabel.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)
#     prayerLabel = tk.Label(tempFrame, textvariable=pv,
#                            font=timeFont, bg=LIGHT_GREY)
#     tmpArr.append(prayerLabel)
#     prayerLabel.place(relx=2/3, rely=0, relwidth=1/3, relheight=1)
#     prayerStartPrayerTimes.append(tmpArr)
#     stringvars = [sv, nv, pv]
#     prayerFrames.append(tempFrame)
#     prayerStringvars.append(stringvars)
# jummahFrame = tk.Frame(master)
# jummahLabelArabic = tk.Label(jummahFrame, image=renderjummah, bg=GREY)
# jummahLabel = tk.Label(jummahFrame, text="Jummah",
#                        font=prayerBottomFont, bg=GREY)
# jummahLabelTime = tk.Label(
#     jummahFrame, textvariable=jummahVar, font=prayerBottomFontTime, bg=GREY)
# jummahLabelArabic.place(relx=0, rely=0, relwidth=1, relheight=1/4)
# jummahLabel.place(relx=0, rely=1/4, relwidth=1, relheight=1/4)
# jummahLabelTime.place(relx=0, rely=1/2, relwidth=1, relheight=1/2)
# seherFrame = tk.Frame(master)
# seherLabelArabic = tk.Label(seherFrame, image=renderseher, bg=GREY)
# seherLabel = tk.Label(seherFrame, text="Seher End",
#                       font=prayerBottomFont, bg=GREY)
# seherLabelTime = tk.Label(seherFrame, textvariable=seherVar,
#                           font=prayerBottomFontTime, bg=GREY)
# seherLabelArabic.place(relx=0, rely=0, relwidth=1, relheight=1/4)
# seherLabel.place(relx=0, rely=1/4, relwidth=1, relheight=1/4)
# seherLabelTime.place(relx=0, rely=1/2, relwidth=1, relheight=1/2)
# sunriseFrame = tk.Frame(master)
# sunriseLabelArabic = tk.Label(
#     sunriseFrame, image=rendersunrise, bg=GREY)
# sunriseLabel = tk.Label(sunriseFrame, text="Sunrise",
#                         font=prayerBottomFont, bg=GREY)
# sunriseLabelTime = tk.Label(
#     sunriseFrame, textvariable=sunriseVar, font=prayerBottomFontTime, bg=GREY)
# sunriseLabelArabic.place(relx=0, rely=0, relwidth=1, relheight=1/4)
# sunriseLabel.place(relx=0, rely=1/4, relwidth=1, relheight=1/4)
# sunriseLabelTime.place(relx=0, rely=1/2, relwidth=1, relheight=1/2)
# zawalFrame = tk.Frame(master)
# zawalLabelArabic = tk.Label(zawalFrame, image=renderzawal, bg=GREY)
# zawalLabel = tk.Label(zawalFrame, text="Zawal",
#                       font=prayerBottomFont, bg=GREY)
# zawalLabelTime = tk.Label(zawalFrame, textvariable=zawalVar,
#                           font=prayerBottomFontTime, bg=GREY)
# zawalLabelArabic.place(relx=0, rely=0, relwidth=1, relheight=1/4)
# zawalLabel.place(relx=0, rely=1/4, relwidth=1, relheight=1/4)
# zawalLabelTime.place(relx=0, rely=1/2, relwidth=1, relheight=1/2)
# bottomLabelArabic = tk.Label(master, bg=BLACK,
#                              image=rendertitle, fg=WHITE, anchor=S)
# bottomLabelEnglish = tk.Label(master, bg=BLACK, text="MASJID ALFURQAN",
#                               fg=WHITE, font=prayerBottomFont, anchor=N)
# logoLabel = tk.Label(master, bg=BLACK, image=renderLogo)
# socialFrame = tk.Frame(master, bg=BLACK)
# fbLabel = tk.Label(socialFrame, image=renderfb, bg=BLACK)
# fbLabel.place(relx=0, rely=0, relwidth=0.5, relheight=0.4)
# twLabel = tk.Label(socialFrame, image=rendertw, bg=BLACK)
# twLabel.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.4)
# inLabel = tk.Label(socialFrame, image=renderin, bg=BLACK)
# inLabel.place(relx=0, rely=0.4, relwidth=0.5, relheight=0.4)
# ytLabel = tk.Label(socialFrame, image=renderyt, bg=BLACK)
# ytLabel.place(relx=0.5, rely=0.4, relwidth=0.5, relheight=0.4)
# atLabel = tk.Label(master, text="@AlfurqanMCR",
#                    fg=WHITE, bg=BLACK, font=atFont)

# hadithArabicLabel = tk.Label(master, image=renderhadith, bg=BLACK)
# hadithLabel = tk.Label(master, text="The messenger of Allah (peace be\n upon him) said, \"When the Imam\n is delivering the Khutba, and\n you ask your companion to\n keep quiet and listen, then no\n doubt you have done an evil act.\"",
#                        bg=BLACK, fg=WHITE, font=hadithPrayerFont)
# imageLabel = tk.Label(master, bg=BLACK, image=renderNoPhone)
# warningLabel = tk.Label(master, text="Turn off/silence\nyour phone",
#                         bg=BLACK, fg=WHITE, font=noPhoneFont)
# prayerLabel = tk.Label(master, textvariable=noPhoneVar,
#                        bg=BLACK, fg=WHITE, font=noPhonePrayerFont)

# athanLabel = tk.Label(master, textvariable=athanVar,
#                       bg=BLACK, fg=WHITE, font=athanFont, anchor=S)
# athanLabelArabic = tk.Label(master, bg=BLACK,
#                             fg=WHITE, font=athanFont, anchor=N)
# blackLabel = tk.Label(master, textvariable=blackenVar,
#                       bg=BLACK, fg=WHITE, font=countdownFont)
# athanImageLabel = tk.Label(master, bg=BLACK,
#                            fg=WHITE, image=renderNoPhoneAthan)

# def updateStringvars():
#     today = getDayInfo(time.localtime()[7], csv_rows)
#     islamicDateVar.set(today["IslamicDate"])
#     tomorrow = getDayInfo(time.localtime()[7] + 1, csv_rows)
#     gregorianDateVar.set(today["GregorianDate"])
#     keys = ["StartTimes", "PrayerNames", "PrayerTimes"]
#     timeVar.set(currentStringTime())
#     for row in range(5):
#         for col, key in enumerate(keys):
#             try:
#                 if (not alreadyDone(today[key][row])):
#                     prayerStringvars[row][col].set(today[key][row])
#                 else:
#                     prayerStringvars[row][col].set(tomorrow[key][row])
#             except:
#                 if (not alreadyDone(today["PrayerTimes"][row])):
#                     prayerStringvars[row][col].set(today[key][row])
#                 else:
#                     prayerStringvars[row][col].set(tomorrow[key][row])
#     for row, label in enumerate(prayerArabicLabels):
#         if ((row == 1 and alreadyDone(today["PrayerTimes"][row]) and time.localtime()[6] == 3) or (row == 1 and time.localtime()[6] == 4) and not alreadyDone(today["PrayerTimes"][row])):
#             row = 5
#         label.config(image=prayerImages[row][1])
#     jummahVar.set(stringTime(minuteTime(
#         today["PrayerTimes"][1])-config.jummahLength))
#     if (not alreadyDone(today["StartTimes"][0])):
#         seherVar.set(today["Seher"])
#     else:
#         seherVar.set(tomorrow["Seher"])
#     sunriseVar.set(today["Sunrise"])
#     zawalVar.set(stringTime(minuteTime(today["StartTimes"][1])-10))

#     noPhoneVar.set(str(silenceMobile(csv_rows)[1]) + "\n" + silenceMobile(csv_rows)[2])

#     nextIndex = 0
#     try:
#         while (minuteTime(today["StartTimes"][nextIndex]) < minuteTime(currentStringTime())):
#             nextIndex += 1
#     except:
#         nextIndex = 0

#     blackenVar.set(str(int(blackenScreen()[
#                    1]/60 % 60)) + ":" + str(int(blackenScreen()[1] % 60)).rjust(2, "0"))

# def updateColors():
#     today = getDayInfo(time.localtime()[7], csv_rows)
#     for row, start in enumerate(today["StartTimes"]):
#         if (minuteTime(currentStringTime()) < minuteTime(start) and minuteTime(start) - minuteTime(
#                 currentStringTime()) < 2 and int(time.time()) % 2 == 0):
#             prayerStartPrayerTimes[row][0].config(fg=RED)
#         else:
#             prayerStartPrayerTimes[row][0].config(fg=BLACK)
#     for row, prayer in enumerate(today["PrayerTimes"]):
#         if (minuteTime(currentStringTime()) < minuteTime(prayer) and minuteTime(prayer) - minuteTime(
#                 currentStringTime()) < 2 and int(time.time()) % 2 == 0):
#             prayerStartPrayerTimes[row][1].config(fg=RED)
#         else:
#             prayerStartPrayerTimes[row][1].config(fg=BLACK)
#     if (int(time.time()) % 2 == 0):
#         blackLabel.config(fg=RED)
#     else:
#         blackLabel.config(fg=LIGHT_GREY)

# def placeRegularScreen():
#     backLabel.place(relx=0, rely=0, relwidth=1, relheight=1)
#     timeCanvas.place(relx=0.24, rely=-0.01, relwidth=0.52, relheight=0.12)
#     gregorianDateLabel.place(relx=0, rely=0, relwidth=0.25, relheight=0.1)
#     islamicDateLabel.place(relx=0.75, rely=0, relwidth=0.25, relheight=0.1)
#     headerFrame.place(relx=0, rely=0.1, relwidth=1, relheight=0.05)
#     for row in range(5):
#         prayerFrames[row].place(
#             relx=0, rely=0.15 + ((0.6 * row) / 5), relwidth=1, relheight=0.59 / 5)
#     jummahFrame.place(relx=0, rely=0.75, relwidth=0.25, relheight=0.125)
#     seherFrame.place(relx=0.25, rely=0.75, relwidth=0.25, relheight=0.125)
#     sunriseFrame.place(relx=0.5, rely=0.75, relwidth=0.25, relheight=0.125)
#     zawalFrame.place(relx=0.75, rely=0.75, relwidth=0.25, relheight=0.125)
#     logoLabel.place(relx=0, rely=0.875, relwidth=0.2, relheight=0.125)
#     socialFrame.place(relx=0.775, rely=0.875,
#                       relwidth=0.2, relheight=0.105)
#     atLabel.place(relx=0.775, rely=0.965, relwidth=0.2, relheight=0.02)
#     bottomLabelArabic.place(
#         relx=0, rely=0.875, relwidth=1, relheight=0.125/2)
#     bottomLabelEnglish.place(
#         relx=0, rely=0.875+(0.125/2), relwidth=1, relheight=0.125/2)

# def forgetRegularScreen():
#     backLabel.place_forget()
#     gregorianDateLabel.place_forget()
#     timeCanvas.place_forget()
#     islamicDateLabel.place_forget()
#     headerFrame.place_forget()
#     for row in range(5):
#         prayerFrames[row].place_forget()
#     jummahFrame.place_forget()
#     seherFrame.place_forget()
#     sunriseFrame.place_forget()
#     zawalFrame.place_forget()
#     logoLabel.place_forget()
#     bottomLabelEnglish.place_forget()
#     bottomLabelArabic.place_forget()
#     atLabel.place_forget()
#     socialFrame.place_forget()

# def placeNoMobile():
#     imageLabel.place(relx=0, rely=2/5, relwidth=1, relheight=1/5)
#     warningLabel.place(relx=0, rely=0, relwidth=1, relheight=2/5)
#     prayerLabel.place(relx=0, rely=3/5, relwidth=1, relheight=2/5)

# def forgetNoMobile():
#     imageLabel.place_forget()
#     warningLabel.place_forget()
#     prayerLabel.place_forget()

# def placeNoMobileHadith():
#     hadithArabicLabel.place(relx=0, rely=0/5, relwidth=1, relheight=1/10)
#     hadithLabel.place(relx=0, rely=1/10, relwidth=1, relheight=3/10)
#     imageLabel.place(relx=0, rely=3/5, relwidth=1, relheight=1/5)
#     warningLabel.place(relx=0, rely=2/5, relwidth=1, relheight=1/5)
#     prayerLabel.place(relx=0, rely=4/5, relwidth=1, relheight=1/5)

# def forgetNoMobileHadith():
#     hadithArabicLabel.place_forget()
#     hadithLabel.place_forget()
#     imageLabel.place_forget()
#     warningLabel.place_forget()
#     prayerLabel.place_forget()

# def placeNoScreen():
#     blackLabel.place(relx=0, rely=2/3, relwidth=1, relheight=1/3)
#     athanLabel.place(relx=0, rely=0, relwidth=1, relheight=1/6)
#     athanImageLabel.place(relx=0, rely=1/3, relwidth=1, relheight=1/3)
#     athanLabelArabic.place(relx=0, rely=1/6, relwidth=1, relheight=1/6)

# def forgetNoScreen():
#     blackLabel.place_forget()
#     athanLabel.place_forget()
#     athanLabelArabic.place_forget()
#     athanImageLabel.place_forget()

# prev = -1
# curr = 1
# fridayCooldown = False
# dayCooldown = False
# while (True):
#     timeCanvas.itemconfig(timeText, text="{}:{}:{}".format(time.localtime()[3], str(
#         time.localtime()[4]).rjust(2, "0"), str(time.localtime()[5]).rjust(2, "0")))
#     updateStringvars()
#     updateColors()

#     if time.localtime()[6] == 4 and minuteTime(config.fridaySoundTime) == minuteTime(currentStringTime()):
#         if fridayCooldown == False:
#             fridaySound.play()
#         fridayCooldown = True
#     else:
#         fridayCooldown = False

#     if time.localtime()[6] != 4 and minuteTime(config.daySoundTime) == minuteTime(currentStringTime()):
#         if dayCooldown == False:
#             fridaySound.play()
#         dayCooldown = True
#     else:
#         dayCooldown = False

#     if (silenceMobile(csv_rows)[0]):
#         curr = 2
#     elif (blackenScreen()[0]):
#         curr = 1
#     else:
#         curr = 0
#     if (curr != prev):
#         if (curr == 0):
#             if (prev == 1):
#                 beginSound.play()
#             forgetNoScreen()
#             forgetNoMobileHadith()
#             placeRegularScreen()
#         elif (curr == 1):
#             forgetRegularScreen()
#             forgetNoMobileHadith()
#             placeNoScreen()
#         elif (curr == 2):
#             prayerSound.play()
#             if (silenceMobile(csv_rows)[5]):
#                 forgetRegularScreen()
#                 forgetNoScreen()
#                 placeNoMobileHadith()
#             else:
#                 forgetRegularScreen()
#                 forgetNoScreen()
#                 placeNoMobile()
#     prev = curr
#     master.update_idletasks()
#     master.update()
