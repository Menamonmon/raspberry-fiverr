from tkinter import *
from PIL import Image, ImageTk
import datetime
import time
from ummalqura.hijri_date import HijriDate
import csv
import config
import pygame
import math
import calendar

if (config.orientation=="Horizontal"):

    def minuteTime(s):
        return int(s.split(":")[0]) * 60 + int(s.split(":")[1])


    def stringTime(m):
        return str(math.floor(m / 60)) + ":" + str(math.floor(m % 60)).rjust(2, "0")


    def currentStringTime():
        return str(time.localtime()[3]) + ":" + str(time.localtime()[4]).rjust(2, "0")

    def getDayInfo(day):
        ret = {}
        day -= 1
        dt = datetime.date.fromordinal(day)
        td = datetime.date.today()
        um = HijriDate(td.year, dt.month, dt.day, gr=True)
        islamicMonths = ["Muharram", "Safar", "Rabi\' al-awwal", "Rabi\' al-thani", "Jumada al-awwal", "Jumada al-thani", "Rajab", "Sha\'ban", "Ramadan", "Shawwal", "Dhu al-Qi'dah", "Dhu al-Hijjah"]
        gregorianDate = ("{} {} {} {}".format(um.day_name_en[0:3].upper(), dt.day, um.month_name_gr[0:3].upper(), td.year))
        islamicDate = ("{} {} {}".format(um.day, islamicMonths[um.month-1], um.year))
        if (calendar.weekday(td.year, dt.month, dt.day) == 4):
            prayerNames = ['FAJAR', 'JUMMAH', 'ASAR', 'MAGHRIB', 'ISHA']
            prayerNamesArabic = ['فجر', 'جمعه', 'عصر', 'مغرب', 'عشاء']
        else:
            prayerNames = ['FAJAR', 'ZUHR', 'ASAR', 'MAGHRIB', 'ISHA']
            prayerNamesArabic = ['فجر', 'ظهر', 'عصر', 'مغرب', 'عشاء']
        prayerTimes = []
        prayerKeys = ['FAJR prayer', 'DUHR prayer', 'ASAR prayer', 'M/RIB prayer', 'ISHA prayer']
        for key in prayerKeys:
            prayerTimes.append(str(int(csvRows[day][key].split(":")[0]) + (12 * (key != "FAJR prayer"))) + ":" +
                               csvRows[day][key].split(":")[1])
        startTimes = []
        startKeys = ['FAJR start', 'DUHR start', 'ASAR start', 'M/RIB start', 'ISHA start']
        for key in startKeys:
            startTimes.append(str(int(csvRows[day][key].split(":")[0]) + (12 * (
                        key != "FAJR start" and key != "DUHR start" or (
                            key == "DUHR start" and int(csvRows[day][key].split(":")[0]) == 1)))) + ":" +
                              csvRows[day][key].split(":")[1])
        sunrise = csvRows[day]["SUN RISE"]
        seher = stringTime(minuteTime(csvRows[day]["FAJR start"])-0)
        ret["GregorianDate"] = gregorianDate
        ret["IslamicDate"] = islamicDate
        ret["PrayerNames"] = prayerNames
        ret["PrayerNamesArabic"] = prayerNamesArabic
        ret["PrayerTimes"] = prayerTimes
        ret["StartTimes"] = startTimes
        ret["Sunrise"] = sunrise
        ret["Seher"] = seher
        return ret

    csvRows = []

    clock24hr = config.clock24hr

    with open('Full2020csv.csv') as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            csvRows.append(row)

    master = Tk()
    master.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth(), master.winfo_screenheight()))
    master.attributes("-fullscreen", True)

    def killWindow(event):
        master.destroy()

    master.bind("<Escape>", killWindow)

    #loadL = Image.open("logo.png").resize((int(master.winfo_screenheight()*(2/15)), int(master.winfo_screenheight()*(2/15))))
    #renderL = ImageTk.PhotoImage(loadL)
    loadR = Image.open("logo.png").resize((int(master.winfo_screenheight()*(2/15)), int(master.winfo_screenheight()*(2/15))))
    renderR = ImageTk.PhotoImage(loadR)

    loadM = Image.open("nophone.png").resize((int(master.winfo_screenwidth()/2), int(master.winfo_screenheight())))
    renderM = ImageTk.PhotoImage(loadM)

    gregorianDateVar = StringVar()
    islamicDateVar = StringVar()
    titleVar = StringVar()
    titleVar.set("MASJID ALFURQAN")
    timeVar = StringVar()
    nextPrayerVar = StringVar()
    nextPrayerArabicVar = StringVar()
    nextPrayerTimeVar = StringVar()
    blinkColor = StringVar()
    seherVar = StringVar()
    countdownVar = StringVar()

    dateFont = ("Arial", int(master.winfo_screenheight()/40), "bold")
    dateBackground = "#ffffff"
    dateForeground = "#000000"

    titleFont = ("Arial", int(master.winfo_screenheight()/17), "bold")
    titleBackground = "#ffffff"
    titleForeground = "#000000"

    timeFont = ("Arial", int(master.winfo_screenheight()/13), "bold")
    timeBackground = "#ffffff"
    timeForeground = "#000000"

    bigNextFont = ("Times", int(master.winfo_screenheight()/4), "bold")
    bigishNextFont = ("Times", int(master.winfo_screenheight()/8), "bold")
    nextFont = ("Times", int(master.winfo_screenheight()/10), "bold")
    smallNextFont = ("Times", int(master.winfo_screenheight()/20), "bold")
    nextForeground = "#000000"
    blinkColor.set(nextForeground)

    bigTimesFont = ("Arial", int(master.winfo_screenheight()/20), "bold")
    timesFont = ("Arial", int(master.winfo_screenheight()/30), "bold")
    smallTimesFont = ("Arial", int(master.winfo_screenheight()/40), "bold")
    timesBackground = "#ffffff"
    timesForeground = "#000000"

    seherForeground = "#000000"
    seherBackground = "#ffffff"

    noPhoneFont = ("Arial", int(master.winfo_screenheight()/12), "bold")
    noPhoneFontBigger = ("Arial", int(master.winfo_screenheight()/8), "bold")

    logoBackground = "#ffffff"
    addressFont = ("Arial", int(master.winfo_screenheight()/35), "bold")

    #logoLabelLeft = Label(master, image=renderL, anchor=W, bg=logoBackground)
    #logoLabelLeft.image = renderL
    logoLabelRight = Label(master, image=renderR, anchor=E, bg=logoBackground)
    logoLabelRight.image = renderR
    addressLabel = Label(master, text="42 Great Southern St, Manchester M14 4EZ", bg=logoBackground, font=addressFont)
    dateLabelGregorian = Label(master, textvariable=gregorianDateVar, font=dateFont, bg=dateBackground, fg=dateForeground)
    dateLabelIslamic = Label(master, textvariable=islamicDateVar, font=dateFont, bg=dateBackground, fg=dateForeground)
    #titleLabel = Label(master, textvariable=titleVar, font=titleFont, bg=titleBackground, fg=titleForeground)
    titleFrame = Frame(master)
    timeLabel = Label(master, textvariable=timeVar, font=timeFont, bg=timeBackground, fg=timeForeground)

    largeTimerFrame = Frame(master, bg=timesBackground)
    nextLabel = Label(largeTimerFrame, text="Next Salaah", fg=nextForeground, bg=timesBackground, font=smallNextFont)
    nextPrayerLabel = Label(largeTimerFrame, textvariable=nextPrayerVar, fg=nextForeground, bg=timesBackground, font=bigishNextFont)
    nextPrayerArabicLabel = Label(largeTimerFrame, textvariable=nextPrayerArabicVar, fg=nextForeground, bg=timesBackground, font=smallNextFont)
    nextPrayerTimeLabel = Label(largeTimerFrame, textvariable=nextPrayerTimeVar, fg=nextForeground, bg=timesBackground, font=bigNextFont)
    countdownLabel = Label(largeTimerFrame, textvariable=countdownVar, fg=nextForeground, bg=timesBackground, font=smallNextFont)

    seherLabel = Label(master, textvariable=seherVar, fg=seherForeground, bg=seherBackground, font=bigTimesFont)

    timesFrame = Frame(master, bg=timesBackground)

    def updatePrayerTimes():
        tm = time.localtime()
        yearDay = tm[7] - 1
        if (tm[6]==4):
            prayers = ['FAJAR', 'SUNRISE', 'JUMMAH', 'ASAR', 'MAGHRIB', 'ISHA']
        else:
            prayers = ['FAJAR', 'SUNRISE','ZUHR', 'ASAR', 'MAGHRIB', 'ISHA']
        keys = [('FAJR start','FAJR prayer'),('SUN RISE','SUN RISE'),('DUHR start','DUHR prayer'),('ASAR start','ASAR prayer'),('M/RIB start','M/RIB prayer'),('ISHA start','ISHA prayer')]
        prayerTopLabel = Label(timesFrame, text='Jamaat Times', fg=timesForeground, bg=timesBackground, font=timesFont)
        startTopLabel = Label(timesFrame, text='Beginning Time', fg=timesForeground, bg=timesBackground, font=timesFont)
        prayerTopLabel.place(relx=(3/5), rely=0, relwidth=(2 / 5), relheight=(1 / (len(prayers)+1)))
        startTopLabel.place(relx=0, rely=0, relwidth=(2 / 5), relheight=(1 / (len(prayers)+1)))
        alreadyDone = 1
        nPrayer = getNextPrayer()[0]
        for index, prayer in enumerate(prayers):
            if (prayer == nPrayer):
                alreadyDone = 0
            pTime = csvRows[yearDay+alreadyDone][keys[index][1]]
            phm = pTime.split(":")
            if(clock24hr):
                phm = [int(phm[0]) + 12 * (index != 0 and index != 1 and (index != 2 or (index == 2 and phm[0] == "1"))), int(phm[1])]
            sTime = csvRows[yearDay+alreadyDone][keys[index][0]]
            shm = sTime.split(":")
            if (clock24hr):
                shm = [int(shm[0]) + 12 * (index != 0 and index != 1 and (index != 2 or (index == 2 and shm[0] == "1"))), int(shm[1])]
            prayerLabel = Label(timesFrame, text=str(phm[0]) + ":" + str(phm[1]).rjust(2,'0'), fg=timesForeground, bg=timesBackground, font=bigTimesFont)
            nameLabel = Label(timesFrame, text=prayer, fg=timesForeground, bg=timesBackground, font=bigTimesFont)
            startLabel = Label(timesFrame, text=str(shm[0]) + ":" + str(shm[1]).rjust(2,'0'), fg=timesForeground, bg=timesBackground, font=bigTimesFont)
            prayerLabel.place(relx=(2.25/3), rely=((index+1)/(len(prayers)+1)), relwidth=(0.75/3), relheight=(1/(len(prayers)+1)))
            nameLabel.place(relx=(0.75/3), rely=((index+1)/(len(prayers)+1)), relwidth=(1.5/3), relheight=(1/(len(prayers)+1)))
            startLabel.place(relx=0, rely=((index+1)/(len(prayers)+1)), relwidth=(0.75/3), relheight=(1/(len(prayers)+1)))
        sTime = csvRows[yearDay+alreadyDone]['FAJR start']
        sTime = sTime.split(':')
        sTime[1] = str(int(sTime[1]) - 0)
        if (int(sTime[1]) < 0):
            sTime[0] = str(int(sTime[0]) - 1)
            sTime[1] = str(int(sTime[1]) + 60)
        seherVar.set("Suhoor end: " + sTime[0] + ":" + sTime[1].rjust(2, '0'))

    def getNextPrayer():
        tm = time.localtime()
        yearDay = tm[7] - 1
        prayers = ['FAJAR', 'ZUHR', 'ASAR', 'MAGHRIB', 'ISHA']
        arabicPrayers = ["فجر","ظهر","عصر","مغرب","عشاء"]
        keys = ['FAJR prayer', 'DUHR prayer', 'ASAR prayer', 'M/RIB prayer', 'ISHA prayer']
        for index, prayer in enumerate(prayers):
            prayerTime = csvRows[yearDay][keys[index]]
            hm = prayerTime.split(":")
            hm = [int(hm[0]) + 12*(index!=0), int(hm[1])]
            pt = hm[0]*60 + hm[1]
            ct = tm[3]*60 + tm[4]
            if (ct < pt):
                return prayer, hm, arabicPrayers[index]
        prayerTime = csvRows[yearDay+1][keys[0]]
        hm = prayerTime.split(":")
        hm = [int(hm[0]), int(hm[1])]
        return 'FAJAR', hm, arabicPrayers[0]

    def updateCountdown():
        tm = time.localtime()
        yearDay = tm[7] - 1
        prayers = ['FAJAR', 'ZUHR', 'ASAR', 'MAGHRIB', 'ISHA']
        keys = ['FAJR start', 'DUHR start', 'ASAR start', 'M/RIB start', 'ISHA start']
        for index, prayer in enumerate(prayers):
            prayerTime = csvRows[yearDay][keys[index]]
            hm = prayerTime.split(":")
            hm = [int(hm[0]) + 12 * (((index == 1 and int(hm[0]) < 6) or index > 1)), int(hm[1])]
            pt = hm[0] * 60 + hm[1]
            ct = tm[3] * 60 + tm[4]
            if (ct < pt):
                countdownVar.set("{}:{}:{}".format(str(hm[0] - tm[3] - (hm[1] - tm[4] - 1 < 0)), str((hm[1] - tm[4] - 1)%60).rjust(2, '0'), str(60 - tm[5]).rjust(2, '0')))
                break
            else:
                countdownVar.set("0:00:00")

    def isRamadan():
        tm = time.localtime()
        yearDay = tm[7] - 1
        leap = (tm[0] % 4 == 0)
        return (yearDay >= 112 + leap and yearDay <= 142 + leap)

    def blinkText():
        tm = time.localtime()
        yearDay = tm[7] - 1
        prayers = ['FAJAR', 'ZUHR', 'ASAR', 'MAGHRIB', 'ISHA']
        arabicPrayers = ["فجر","ظهر","عصر","مغرب","عشاء"]
        keys = ['FAJR start', 'DUHR start', 'ASAR start', 'M/RIB start', 'ISHA start']
        for index, prayer in enumerate(prayers):
            prayerTime = csvRows[yearDay][keys[index]]
            hm = prayerTime.split(":")
            hm = [int(hm[0]) + 12*(index!=0), int(hm[1])]
            pt = hm[0]*60 + hm[1]
            ct = tm[3]*60 + tm[4]
            if (ct < pt and pt - ct <= 2):
                return True
        return False

    #logoLabelLeft.place(relx=0, rely=0, relwidth=(2/15), relheight=(2/15))
    addressLabel.place(relx=0.5, rely=(13/15), relwidth=0.5, relheight=(2/15))
    dateLabelGregorian.place(relx=0, rely=0, relwidth=(2.5/15), relheight=(1/15))
    dateLabelIslamic.place(relx=0, rely=(1/15), relwidth=(2.5/15), relheight=(1/15))
    titleFrame.place(relx=(2.5/15), rely=0, relwidth=(8.85/15), relheight=(2/15))
    timeLabel.place(relx=(11.5/15), rely=0, relwidth=(2.35/15), relheight=(2/15))

    largeTimerFrame.place(relx=0, rely=(2/15), relwidth=0.5, relheight=(11/15))
    nextLabel.place(relx=0, rely=0, relwidth=1, relheight=(0.75/5))
    nextPrayerLabel.place(relx=0, rely=(1.25/5), relwidth=1, relheight=(1.5/5))
    #nextPrayerArabicLabel.place(relx=0, rely=(3/5), relwidth=1, relheight=(0.5/5))
    nextPrayerTimeLabel.place(relx=0, rely=(2.75/5), relwidth=1, relheight=(2.25/5))
    countdownLabel.place(relx=0, rely=(0.75/5), relwidth=1,relheight=(0.5/5))

    timesFrame.place(relx=0.5, rely=(2/15), relwidth=0.5, relheight=(11/15))

    topSeparator = Label(master, bg="#693821")
    topSeparator.place(relx=0, rely=(2/15), relwidth=1, relheight=(1/15)/5)
    bottomSeparator = Label(master, bg="#693821")
    bottomSeparator.place(relx=0, rely=(13/15)-((1/15)/5), relwidth=1, relheight=(1/15)/5)
    topLeftSeparator = Label(master, bg="#693821")
    topLeftSeparator.place(relx=(2.5/15), rely=0, relwidth=(1/15)/5, relheight=(2/15))
    topRightSeparator = Label(master, bg="#693821")
    topRightSeparator.place(relx=(11.35/15), rely=0, relwidth=(1/15)/5, relheight=(2/15))

    seherLabel.place(relx=0,rely=(13/15),relwidth=0.5,relheight=(2/15))
    logoLabelRight.place(relx=(13/15), rely=0, relwidth=(2/15), relheight=(2/15))


    updatePrayerTimes()
    nextPrayerVar.set(getNextPrayer()[0])
    #nextPrayerArabicVar.set(getNextPrayer()[2])

    def updateClock():
        tm = time.localtime()
        yearDay = tm[7] - 1
        seconds = False
        if(seconds):
            if (clock24hr):
                timeVar.set("{}:{}:{}".format(tm[3], str(tm[4]).rjust(2, '0'),str(tm[5]).rjust(2, '0')))
            else:
                if (tm[3] % 12 == 0):
                    timeVar.set("{}:{}:{}".format(12, str(tm[4]).rjust(2, '0'),str(tm[5]).rjust(2, '0')))
                else:
                    timeVar.set("{}:{}:{}".format(tm[3] % 12, str(tm[4]).rjust(2, '0'),str(tm[5]).rjust(2, '0')))
        else:
            if (clock24hr):
                timeVar.set("{}:{}".format(tm[3], str(tm[4]).rjust(2, '0')))
            else:
                if (tm[3] % 12 == 0):
                    timeVar.set("{}:{}".format(12, str(tm[4]).rjust(2, '0')))
                else:
                    timeVar.set("{}:{}".format(tm[3] % 12, str(tm[4]).rjust(2, '0')))


    if (clock24hr):
        nextPrayerTimeVar.set("{}:{}".format(getNextPrayer()[1][0], str(getNextPrayer()[1][1]).rjust(2,'0')))
    else:
        if (getNextPrayer()[1][0] % 12 == 0):
            nextPrayerTimeVar.set("{}:{}".format(12, str(getNextPrayer()[1][1]).rjust(2,'0')))
        else:
            nextPrayerTimeVar.set("{}:{}".format(getNextPrayer()[1][0] % 12, str(getNextPrayer()[1][1]).rjust(2,'0')))

    def silenceMobile():
        tm = time.localtime()
        yearDay = tm[7] - 1
        prayers = ['FAJAR', 'ZUHR', 'ASAR', 'MAGHRIB', 'ISHA']
        arabicPrayers = ["فجر", "ظهر", "عصر", "مغرب", "عشاء"]
        keys = ['FAJR prayer', 'DUHR prayer', 'ASAR prayer', 'M/RIB prayer', 'ISHA prayer']

        if (tm[6]==4 and tm[3] * 60 + tm[4] < int(config.fridayPrayerEnd.split(":")[0]) * 60 + int(config.fridayPrayerEnd.split(":")[1]) and tm[3] * 60 + tm[4] > int(config.fridayPrayerStart.split(":")[0]) * 60 + int(config.fridayPrayerStart.split(":")[1])):
            return True, 'Jummah', csvRows[yearDay][keys[1]]

        for index, prayer in enumerate(prayers):
            prayerTime = csvRows[yearDay][keys[index]]
            hm = prayerTime.split(":")
            hm = [int(hm[0]) + 12 * (index != 0), int(hm[1])]
            pt = hm[0] * 60 + hm[1]
            ct = tm[3] * 60 + tm[4]
            if (ct - pt < config.noMobileTimes[index] and ct - pt >= 0):
                return True, prayer, prayerTime
        return False, None

    class TitleScroller:
        def __init__(self, master, image):
            self.master = master
            self.image = image
            loadTitle = Image.open(self.image).resize((int(master.winfo_screenwidth()*(8.85/15)),int(master.winfo_screenheight()*(2/15))))
            renderTitle = ImageTk.PhotoImage(loadTitle)
            self.labelLeft = Label(self.master, image=renderTitle)
            self.labelLeft.image = renderTitle
            self.labelRight = Label(self.master, image=renderTitle)
            self.labelRight.image = renderTitle
            self.n = 0
        def draw(self):
            self.labelLeft.place(relx=-self.n,rely=0,relwidth=1,relheight=1)
            self.labelRight.place(relx=1-self.n, rely=0, relwidth=1, relheight=1)
        def update(self):
            if (self.n < 1):
                self.n+=0.001
            else:
                self.n = 0
            self.draw()

    title = TitleScroller(titleFrame,"title.jpg")

    class Event:
        def __init__(self, master, image, x, y, w, h, length):
            self.master = master
            self.image = image
            self.x = x
            self.inc = 0
            self.y = y
            self.w = w
            self.h = h
            self.length = length
            self.started = False
            self. deltaStart = time.time()
            loadEvent = Image.open(self.image).resize(
                (int(master.winfo_screenwidth() * (1 / 2)), int(master.winfo_screenheight() * (15 / 15))))
            renderEvent = ImageTk.PhotoImage(loadEvent)
            self.l = Label(self.master, image=renderEvent)
            self.l.image = renderEvent
        def delta(self):
            return time.time() - self.deltaStart
        def draw(self):
    #        self.l.place_forget()
            self.l.place(relx=self.x,rely=self.y,relwidth=self.w,relheight=self.h)
        def show(self):
            if(self.started == False):
                self.deltaStart = time.time()
                self.started = True
            if(self.delta() < 5):
                self.x = 1 - self.delta()/5
            elif(self.delta() >= 5 and self.delta() <= 5 + self.length):
                self.x = 0
            elif(self.delta() > 5 + self.length and self.delta() < 10 + self.length):
                self.x = 0 - (self.delta()-self.length-5)/5
            elif(self.delta() > 10 + self.length):
                self.started = False
                return 1
            self.draw()
            return 0
        def sideScroll(self):
            if(self.started == False):
                self.deltaStart = time.time()
                self.started = True
                self.x = 1
                self.w = 0
            if(self.delta() < 2.5):
                self.w = self.delta()/5
                self.x = 1-self.delta()/5
            elif(self.delta() >= 2.5 and self.delta() < 5):
                self.x = 1 - self.delta()/5
            elif(self.delta() >= 5 and self.delta() <= 5 + self.length):
                self.x = 0
            elif(self.delta() > 5 + self.length and self.delta() < 10 + self.length):
                self.x = 0 - (self.delta()-self.length-5)/5
            elif(self.delta() > 10 + self.length):
                self.started = False
                return 1
            self.draw()
            return 0
        def scroll(self):
            if(self.started == False):
                self.deltaStart = time.time()
                self.started = True
            if(self.delta() < 5):
                self.h = self.delta()/5
            elif(self.delta() >= 5 and self.delta() <= 5 + self.length):
                self.h = 1
            elif(self.delta() > 5 + self.length and self.delta() < 10 + self.length):
                self.h = 1 - (self.delta()-self.length-5)/5
            elif(self.delta() > 10 + self.length):
                self.started = False
                return 1
            self.draw()
            return 0



    class EventArray:
        def __init__(self):
            self.events = []
            self.eventIndex = 0
            for index, event in enumerate(config.imageList):
                self.events.append(Event(master, event, (config.eventType=="slide"), 0, 0.5, (config.eventType=="slide"), config.imageTimes[index]))
        def showEvent(self):
            if(config.eventType=="slide"):
                i = self.events[self.eventIndex].show()
            elif(config.eventType=="scroll"):
                i = self.events[self.eventIndex].scroll()
            self.eventIndex+=i
            if(self.eventIndex==len(self.events)):
                self.eventIndex = 0

    events = EventArray()
    if (int(time.time()) % 2 == 0 and blinkText()):
        nextPrayerTimeLabel.config(fg="#FF0000")
    else:
        nextPrayerTimeLabel.config(fg="#000000")

    tm = time.localtime()
    yearDay = tm[7] - 1
    dt = datetime.date.today()
    um = HijriDate(dt.year, dt.month, dt.day, gr=True)
    gregorianDateVar.set(getDayInfo(time.localtime()[7])['GregorianDate'])
    islamicDateVar.set(getDayInfo(time.localtime()[7])['IslamicDate'])
    updateClock()
    if (int(time.time()) % 600 == 0):
        updatePrayerTimes()
    nextPrayerVar.set(getNextPrayer()[0])
    #nextPrayerArabicVar.set(getNextPrayer()[2])
    if (clock24hr):
        nextPrayerTimeVar.set("{}:{}".format(getNextPrayer()[1][0], str(getNextPrayer()[1][1]).rjust(2, '0')))
    else:
        if (getNextPrayer()[1][0] % 12 == 0):
            nextPrayerTimeVar.set("{}:{}".format(12, str(getNextPrayer()[1][1]).rjust(2, '0')))
        else:
            nextPrayerTimeVar.set("{}:{}".format(getNextPrayer()[1][0] % 12, str(getNextPrayer()[1][1]).rjust(2, '0')))


    playingSound = False
    pygame.mixer.init()
    try:
        pygame.mixer.music.load(config.audio_file)
    except:
        pass

    noPhoneDisplayed = False

    while(True):
        if(int(time.time()*10)%10 == 0):
            updateClock()
            updateCountdown()
            if (int(time.time()) % 2 == 0 and blinkText()):
                nextPrayerTimeLabel.config(fg="#FF0000")
                nextPrayerLabel.config(fg="#FF0000")
                countdownLabel.config(fg="#FF0000")
            else:
                nextPrayerTimeLabel.config(fg="#000000")
                nextPrayerLabel.config(fg="#000000")
                countdownLabel.config(fg="#000000")
        if(silenceMobile()[0]):
            try:
                if(playingSound == False):
                    pygame.mixer.music.play()
                    playingSound = True
            except:
                pass
            if(noPhoneDisplayed == False):
                imageLabel = Label(master, bg="#000000", image=renderM)
                warningLabel = Label(master, text="Turn off/silence\nyour phone", bg="#000000", fg="#ffffff", font=noPhoneFont)
                prayerLabel = Label(master, text=(str(silenceMobile()[1]) + "\n" + silenceMobile()[2]), bg="#000000", fg="#ffffff", font=noPhoneFontBigger)
                imageLabel.place(relx=0,rely=0,relwidth=0.5,relheight=1)
                warningLabel.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.5)
                prayerLabel.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.5)
                noPhoneDisplayed = True
        elif(int(time.time()*10)%600==0):
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
                gregorianDateVar.set("{}/{}/{}".format(dt.day, dt.month, dt.year))
                islamicDateVar.set("{}/{}/{}".format(um.day, um.month, um.year))
            nextPrayerVar.set(getNextPrayer()[0])
            #nextPrayerArabicVar.set(getNextPrayer()[2])
            if (clock24hr):
                nextPrayerTimeVar.set("{}:{}".format(getNextPrayer()[1][0], str(getNextPrayer()[1][1]).rjust(2,'0')))
            else:
                if (getNextPrayer()[1][0] % 12 == 0):
                    nextPrayerTimeVar.set("{}:{}".format(12, str(getNextPrayer()[1][1]).rjust(2,'0')))
                else:
                    nextPrayerTimeVar.set("{}:{}".format(getNextPrayer()[1][0] % 12, str(getNextPrayer()[1][1]).rjust(2,'0')))
        try:
            events.showEvent()
        except:
            pass
        title.update()
        master.update_idletasks()
        master.update()
        time.sleep(0.01)


































elif (config.orientation == "Vertical"):
    csvRows = []

    pygame.mixer.init()
    beginSound = pygame.mixer.Sound(config.beginSound)
    prayerSound = pygame.mixer.Sound(config.prayerSound)
    fridaySound = pygame.mixer.Sound(config.fridaySound)
    daySound = pygame.mixer.Sound(config.daySound)

    clock24hr = config.clock24hr

    with open('Full2020csv.csv') as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            csvRows.append(row)


    def minuteTime(s):
        return int(s.split(":")[0]) * 60 + int(s.split(":")[1])


    def stringTime(m):
        return str(math.floor(m / 60)) + ":" + str(math.floor(m % 60)).rjust(2, "0")


    def currentStringTime():
        return str(time.localtime()[3]) + ":" + str(time.localtime()[4]).rjust(2, "0")


    def getDayInfo(day):
        ret = {}
        day -= 1
        dt = datetime.date.fromordinal(day)
        td = datetime.date.today()
        um = HijriDate(td.year, dt.month, dt.day, gr=True)
        islamicMonths = ["Muharram", "Safar", "Rabi\' al-awwal", "Rabi\' al-thani", "Jumada al-awwal", "Jumada al-thani", "Rajab", "Sha\'ban", "Ramadan", "Shawwal", "Dhu al-Qi'dah", "Dhu al-Hijjah"]
        gregorianDate = ("{} {} {}\n{}".format(um.day_name_en[0:3].upper(), dt.day, um.month_name_gr[0:3].upper(), td.year))
        islamicDate = ("{} {}\n{}".format(um.day, islamicMonths[um.month-1], um.year))
        if (calendar.weekday(td.year, dt.month, dt.day) == 4):
            prayerNames = ['FAJAR', 'JUMMAH', 'ASAR', 'MAGHRIB', 'ISHA']
            prayerNamesArabic = ['فجر', 'جمعه', 'عصر', 'مغرب', 'عشاء']
        else:
            prayerNames = ['FAJAR', 'ZUHR', 'ASAR', 'MAGHRIB', 'ISHA']
            prayerNamesArabic = ['فجر', 'ظهر', 'عصر', 'مغرب', 'عشاء']
        prayerTimes = []
        prayerKeys = ['FAJR prayer', 'DUHR prayer', 'ASAR prayer', 'M/RIB prayer', 'ISHA prayer']
        for key in prayerKeys:
            prayerTimes.append(str(int(csvRows[day][key].split(":")[0]) + (12 * (key != "FAJR prayer"))) + ":" +
                               csvRows[day][key].split(":")[1])
        startTimes = []
        startKeys = ['FAJR start', 'DUHR start', 'ASAR start', 'M/RIB start', 'ISHA start']
        for key in startKeys:
            startTimes.append(str(int(csvRows[day][key].split(":")[0]) + (12 * (
                        key != "FAJR start" and key != "DUHR start" or (
                            key == "DUHR start" and int(csvRows[day][key].split(":")[0]) == 1)))) + ":" +
                              csvRows[day][key].split(":")[1])
        sunrise = csvRows[day]["SUN RISE"]
        seher = stringTime(minuteTime(csvRows[day]["FAJR start"])-0)
        ret["GregorianDate"] = gregorianDate
        ret["IslamicDate"] = islamicDate
        ret["PrayerNames"] = prayerNames
        ret["PrayerNamesArabic"] = prayerNamesArabic
        ret["PrayerTimes"] = prayerTimes
        ret["StartTimes"] = startTimes
        ret["Sunrise"] = sunrise
        ret["Seher"] = seher
        return ret


    master = Tk()
    master.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth(), master.winfo_screenheight()))
    master.attributes("-fullscreen", True)

    blackenImages = []
    blackenImageKeys = ['fajar', 'zuhr', 'asar', 'maghrib', 'isha', "seher", "sunrise"]
    for i in range(7):
        tmpArr = []
        tmpArr.append(Image.open(blackenImageKeys[i] + "Athan.png").resize(
            (int(master.winfo_screenwidth() * 0.4), int(master.winfo_screenheight() * 0.075))))
        tkImage = ImageTk.PhotoImage(tmpArr[0])
        tmpArr.append(tkImage)
        l = Label(master)
        l.image = tkImage
        blackenImages.append(tmpArr)
    for i in range(5):
        tmpArr = []
        tmpArr.append(Image.open(blackenImageKeys[i] + "Prayer.png").resize(
            (int(master.winfo_screenwidth() * 0.4), int(master.winfo_screenheight() * 0.075))))
        tkImage = ImageTk.PhotoImage(tmpArr[0])
        tmpArr.append(tkImage)
        l = Label(master)
        l.image = tkImage
        blackenImages.append(tmpArr)

    prayerImages = []
    prayerImageKeys = ['fajar', 'zuhr', 'asar', 'maghrib', 'isha', 'jummah']
    for i in range(6):
        tmpArr = []
        tmpArr.append(Image.open(prayerImageKeys[i] + "Arabic.png").resize(
            (int(master.winfo_screenwidth() * 0.175), int(master.winfo_screenheight() * 0.033))))
        tkImage = ImageTk.PhotoImage(tmpArr[0])
        tmpArr.append(tkImage)
        l = Label(master)
        l.image = tkImage
        prayerImages.append(tmpArr)

    def killWindow(event):
        master.destroy()


    master.bind("<Escape>", killWindow)

    loadLogo = Image.open("logoNoText.png").resize(
        (int(master.winfo_screenheight() * (0.1125)), int(master.winfo_screenheight() * (0.1125))))
    renderLogo = ImageTk.PhotoImage(loadLogo)

    loadNoPhone = Image.open("nophone.png").resize(
        (int(master.winfo_screenwidth() / 3), int(master.winfo_screenwidth() / 3)))
    renderNoPhone = ImageTk.PhotoImage(loadNoPhone)

    loadNoPhoneAthan = Image.open("nophone.png").resize(
        (int(master.winfo_screenheight() / 3), int(master.winfo_screenheight() / 3)))
    renderNoPhoneAthan = ImageTk.PhotoImage(loadNoPhoneAthan)

    loadfb = Image.open("facebook.png").resize(
        (int(master.winfo_screenheight() * 0.03), int(master.winfo_screenheight() * 0.03)))
    renderfb = ImageTk.PhotoImage(loadfb)
    loadtw = Image.open("twitter.png").resize(
        (int(master.winfo_screenheight() * 0.03), int(master.winfo_screenheight() * 0.03)))
    rendertw = ImageTk.PhotoImage(loadtw)
    loadin = Image.open("instagram.png").resize(
        (int(master.winfo_screenheight() * 0.03), int(master.winfo_screenheight() * 0.03)))
    renderin = ImageTk.PhotoImage(loadin)
    loadyt = Image.open("youtube.png").resize(
        (int(master.winfo_screenheight() * 0.03), int(master.winfo_screenheight() * 0.03)))
    renderyt = ImageTk.PhotoImage(loadyt)
    loadjummah = Image.open("jummahArabic.png").resize(
        (int(master.winfo_screenwidth() * 0.175), int(master.winfo_screenheight() * 0.033)))
    renderjummah = ImageTk.PhotoImage(loadjummah)
    loadseher = Image.open("seherArabic.png").resize(
        (int(master.winfo_screenwidth() * 0.175), int(master.winfo_screenheight() * 0.033)))
    renderseher = ImageTk.PhotoImage(loadseher)
    loadsunrise = Image.open("sunriseArabic.png").resize(
        (int(master.winfo_screenwidth() * 0.175), int(master.winfo_screenheight() * 0.033)))
    rendersunrise = ImageTk.PhotoImage(loadsunrise)
    loadzawal = Image.open("zawalArabic.png").resize(
        (int(master.winfo_screenwidth() * 0.175), int(master.winfo_screenheight() * 0.033)))
    renderzawal = ImageTk.PhotoImage(loadzawal)
    loadtitle = Image.open("titleArabic.png").resize(
        (int(master.winfo_screenwidth() * 0.4), int(master.winfo_screenheight() * 0.05)))
    rendertitle = ImageTk.PhotoImage(loadtitle)
    loadhadith = Image.open("hadithArabic.png").resize(
        (int(master.winfo_screenwidth() * 0.9), int(master.winfo_screenheight() * 0.1)))
    renderhadith = ImageTk.PhotoImage(loadhadith)
    gregorianDateVar = StringVar()
    islamicDateVar = StringVar()
    titleVar = StringVar()
    titleVar.set("MASJID ALFURQAN")
    timeVar = StringVar()
    jummahVar = StringVar()
    seherVar = StringVar()
    sunriseVar = StringVar()
    zawalVar = StringVar()
    athanVar = StringVar()
    noPhoneVar = StringVar()
    blackenVar = StringVar()

    atFont = ("Arial", int(master.winfo_screenwidth() / 54))
    dateFont = ("Arial", int(master.winfo_screenwidth() / 32), "bold")
    timeFont = ("Arial", int(master.winfo_screenwidth() / 15))
    prayerFont = ("Arial", int(master.winfo_screenwidth() / 25), "bold")
    prayerBottomFont = ("Arial", int(master.winfo_screenwidth() / 30), "bold")
    prayerBottomFontTime = ("Arial", int(master.winfo_screenwidth() / 18))
    prayerTimeFont = ("Arial", int(master.winfo_screenwidth() / 15), "bold")
    noPhoneFont = ("Arial", int(master.winfo_screenwidth() / 12), "bold")
    noPhonePrayerFont = ("Arial", int(master.winfo_screenwidth() / 16), "bold")
    countdownFont = ("Arial", int(master.winfo_screenwidth() / 5))
    athanFont = ("Arial", int(master.winfo_screenwidth() / 15))
    hadithPrayerFont = ("Arial", int(master.winfo_screenwidth() / 24), "bold")


    def isRamadan():
        tm = time.localtime()
        yearDay = tm[7] - 1
        leap = (tm[0] % 4 == 0)
        return (yearDay >= 112 + leap and yearDay <= 142 + leap)


    def silenceMobile():
        today = getDayInfo(time.localtime()[7])
        prayerTimes = today['PrayerTimes']
        currentTime = minuteTime(currentStringTime())
        if (time.localtime()[6] == 4 and minuteTime(currentStringTime()) >= minuteTime(config.fridayPrayerStart) and minuteTime(currentStringTime()) < minuteTime(config.fridayPrayerEnd)):
            return True, "{}:{}:{}".format(time.localtime()[3], str(time.localtime()[4]).rjust(2, "0"), str(time.localtime()[5]).rjust(2, "0")), "Asar\n" + str(today['StartTimes'][2]), "1st", "2nd", True
        for index, prayerTime in enumerate(prayerTimes):
            prayerTime = minuteTime(prayerTime)
            if (currentTime - prayerTime < config.noMobileTimes[index] and currentTime - prayerTime >= 0):
                return True, today['PrayerNames'][index], stringTime(prayerTime), "None", "None", False
        return False, "No Prayer", "No Time", "None", "None", False


    def blackenScreen():
        today = getDayInfo(time.localtime()[7])
        for row, start in enumerate(today["StartTimes"]):
            if (not row == 1 or not time.localtime()[6] == 4):
                currentSeconds = time.localtime()[5] + time.localtime()[4] * 60 + time.localtime()[3] * 3600
                startSeconds = minuteTime(start) * 60
                dif = startSeconds - currentSeconds
                if (dif > 0 and dif <= 2*60):
                    athanVar.set("Athan Al " + today["PrayerNames"][row])
                    athanLabelArabic.config(image=blackenImages[row][1])
                    return True, dif
        for row, prayer in enumerate(today["PrayerTimes"]):
            if (not row == 1 or not time.localtime()[6] == 4):
                currentSeconds = time.localtime()[5] + time.localtime()[4] * 60 + time.localtime()[3] * 3600
                startSeconds = minuteTime(prayer) * 60
                dif = startSeconds - currentSeconds
                if (dif > 0 and dif <= 2*60):
                    athanVar.set(today["PrayerNames"][row] + " prayer")
                    athanLabelArabic.config(image=blackenImages[row+7][1])
                    return True, dif
        currentSeconds = time.localtime()[5] + time.localtime()[4] * 60 + time.localtime()[3] * 3600
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


    def alreadyDone(prayerTime):
        return (minuteTime(prayerTime) < minuteTime(currentStringTime()))


    def create_rounded_rect(c, bounding_box, radius, color):
        c.create_arc([bounding_box[0], bounding_box[1], bounding_box[0] + radius * 2, bounding_box[1] + radius * 2],
                     start=90, fill=color, outline=color)
        c.create_arc([bounding_box[0], bounding_box[3], bounding_box[0] + radius * 2, bounding_box[3] - radius * 2],
                     start=180, fill=color, outline=color)
        c.create_arc([bounding_box[2], bounding_box[1], bounding_box[2] - radius * 2, bounding_box[1] + radius * 2],
                     start=0, fill=color, outline=color)
        c.create_arc([bounding_box[2], bounding_box[3], bounding_box[2] - radius * 2, bounding_box[3] - radius * 2],
                     start=270, fill=color, outline=color)
        c.create_rectangle([bounding_box[0], bounding_box[1] + radius, bounding_box[2], bounding_box[3] - radius],
                           fill=color, outline=color)
        c.create_rectangle(
            [bounding_box[0] + radius, bounding_box[1], bounding_box[2] - radius, bounding_box[1] + radius], fill=color,
            outline=color)
        c.create_rectangle(
            [bounding_box[0] + radius, bounding_box[3], bounding_box[2] - radius, bounding_box[3] - radius], fill=color,
            outline=color)



    today = getDayInfo(time.localtime()[7])

    backLabel = Label(master, bg="#cccccc")
    timeCanvas = Canvas(master,width=int(master.winfo_screenwidth() / 2),height=int(master.winfo_screenheight()/10),bg="#111111")
    gregorianDateLabel = Label(master, textvariable=gregorianDateVar, bg="#111111", fg="#ffffff", font=dateFont)
    create_rounded_rect(timeCanvas,[int(master.winfo_screenwidth() / 2 * 0.1),int(master.winfo_screenheight() / 10 * 0.25),int(master.winfo_screenwidth() / 2 * 0.9),int(master.winfo_screenheight() / 10 * 0.95)],16,"#ffffff")
    create_rounded_rect(timeCanvas,[int(master.winfo_screenwidth() / 2 * 0.105),int(master.winfo_screenheight() / 10 * 0.26),int(master.winfo_screenwidth() / 2 * 0.8975),int(master.winfo_screenheight() / 10 * 0.94)],16,"#080808")
    timeText = timeCanvas.create_text([int(master.winfo_screenwidth() / 4),int(master.winfo_screenheight() / 17)],text="",fill="#ffffff",font=timeFont)
    islamicDateLabel = Label(master, textvariable=islamicDateVar, bg="#111111", fg="#ffffff", font=dateFont)
    headerFrame = Frame(master)
    startHeaderLabel = Label(headerFrame,text="BEGINNING",font=prayerFont,bg="#ffffff")
    namesHeaderLabel = Label(headerFrame,text="PRAYER",font=prayerFont,bg="#ffffff")
    prayerHeaderLabel = Label(headerFrame, text="JAMAAT",font=prayerFont,bg="#ffffff")
    startHeaderLabel.place(relx=0, rely=0, relwidth=1/3, relheight=1)
    namesHeaderLabel.place(relx=1/3, rely=0, relwidth=1/3, relheight=1)
    prayerHeaderLabel.place(relx=2/3, rely=0, relwidth=1/3, relheight=1)
    prayerFrames = []
    prayerArabicLabels = []
    prayerStartPrayerTimes = []
    prayerStringvars = []
    for row in range(5):
        tempFrame = Frame(master)
        tmpArr = []
        sv = StringVar()
        nv = StringVar()
        pv = StringVar()
        startLabel = Label(tempFrame, textvariable=sv,font=timeFont,bg="#f0f0f0")
        tmpArr.append(startLabel)
        startLabel.place(relx=0,rely=0,relwidth=1/3,relheight=1)
        nameFrame = Frame(tempFrame)
        nameFrame.place(relx=1/3,rely=0,relwidth=1/3,relheight=1)
        arabicNameLabel = Label(nameFrame,bg="#f0f0f0")
        arabicNameLabel.place(relx=0,rely=0,relwidth=1,relheight=0.5)
        prayerArabicLabels.append(arabicNameLabel)
        englishNameLabel = Label(nameFrame, textvariable=nv,font=prayerFont,bg="#f0f0f0")
        englishNameLabel.place(relx=0,rely=0.5,relwidth=1,relheight=0.5)
        prayerLabel = Label(tempFrame, textvariable=pv,font=timeFont,bg="#f0f0f0")
        tmpArr.append(prayerLabel)
        prayerLabel.place(relx=2/3,rely=0,relwidth=1/3,relheight=1)
        prayerStartPrayerTimes.append(tmpArr)
        stringvars = [sv,nv,pv]
        prayerFrames.append(tempFrame)
        prayerStringvars.append(stringvars)
    jummahFrame = Frame(master)
    jummahLabelArabic = Label(jummahFrame, image=renderjummah,bg="#dedede")
    jummahLabel = Label(jummahFrame, text="Jummah",font=prayerBottomFont,bg="#dedede")
    jummahLabelTime = Label(jummahFrame, textvariable=jummahVar,font=prayerBottomFontTime,bg="#dedede")
    jummahLabelArabic.place(relx=0,rely=0,relwidth=1,relheight=1/4)
    jummahLabel.place(relx=0,rely=1/4,relwidth=1,relheight=1/4)
    jummahLabelTime.place(relx=0,rely=1/2,relwidth=1,relheight=1/2)
    seherFrame = Frame(master)
    seherLabelArabic = Label(seherFrame, image=renderseher,bg="#dedede")
    seherLabel = Label(seherFrame, text="Seher End",font=prayerBottomFont,bg="#dedede")
    seherLabelTime = Label(seherFrame, textvariable=seherVar,font=prayerBottomFontTime,bg="#dedede")
    seherLabelArabic.place(relx=0,rely=0,relwidth=1,relheight=1/4)
    seherLabel.place(relx=0,rely=1/4,relwidth=1,relheight=1/4)
    seherLabelTime.place(relx=0,rely=1/2,relwidth=1,relheight=1/2)
    sunriseFrame = Frame(master)
    sunriseLabelArabic = Label(sunriseFrame, image=rendersunrise,bg="#dedede")
    sunriseLabel = Label(sunriseFrame, text="Sunrise",font=prayerBottomFont,bg="#dedede")
    sunriseLabelTime = Label(sunriseFrame, textvariable=sunriseVar,font=prayerBottomFontTime,bg="#dedede")
    sunriseLabelArabic.place(relx=0,rely=0,relwidth=1,relheight=1/4)
    sunriseLabel.place(relx=0,rely=1/4,relwidth=1,relheight=1/4)
    sunriseLabelTime.place(relx=0,rely=1/2,relwidth=1,relheight=1/2)
    zawalFrame = Frame(master)
    zawalLabelArabic = Label(zawalFrame, image=renderzawal,bg="#dedede")
    zawalLabel = Label(zawalFrame, text="Zawal",font=prayerBottomFont,bg="#dedede")
    zawalLabelTime = Label(zawalFrame, textvariable=zawalVar,font=prayerBottomFontTime,bg="#dedede")
    zawalLabelArabic.place(relx=0,rely=0,relwidth=1,relheight=1/4)
    zawalLabel.place(relx=0,rely=1/4,relwidth=1,relheight=1/4)
    zawalLabelTime.place(relx=0,rely=1/2,relwidth=1,relheight=1/2)
    bottomLabelArabic = Label(master, bg="#111111", image=rendertitle, fg="#ffffff",anchor=S)
    bottomLabelEnglish = Label(master, bg="#111111", text="MASJID ALFURQAN", fg="#ffffff", font=prayerBottomFont,anchor=N)
    logoLabel = Label(master, bg="#111111", image=renderLogo)
    socialFrame = Frame(master,bg="#111111")
    fbLabel = Label(socialFrame,image=renderfb,bg="#111111")
    fbLabel.place(relx=0,rely=0,relwidth=0.5,relheight=0.4)
    twLabel = Label(socialFrame, image=rendertw,bg="#111111")
    twLabel.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.4)
    inLabel = Label(socialFrame, image=renderin,bg="#111111")
    inLabel.place(relx=0, rely=0.4, relwidth=0.5, relheight=0.4)
    ytLabel = Label(socialFrame, image=renderyt,bg="#111111")
    ytLabel.place(relx=0.5, rely=0.4, relwidth=0.5, relheight=0.4)
    atLabel = Label(master,text="@AlfurqanMCR",fg="#ffffff",bg="#111111",font=atFont)

    hadithArabicLabel = Label(master, image=renderhadith, bg="#111111")
    hadithLabel = Label(master,text="The messenger of Allah (peace be\n upon him) said, \"When the Imam\n is delivering the Khutba, and\n you ask your companion to\n keep quiet and listen, then no\n doubt you have done an evil act.\"", bg="#111111", fg="#ffffff", font=hadithPrayerFont)
    imageLabel = Label(master, bg="#111111", image=renderNoPhone)
    warningLabel = Label(master, text="Turn off/silence\nyour phone", bg="#111111", fg="#ffffff", font=noPhoneFont)
    prayerLabel = Label(master, textvariable=noPhoneVar, bg="#111111", fg="#ffffff", font=noPhonePrayerFont)

    athanLabel = Label(master, textvariable=athanVar, bg="#111111", fg="#ffffff",font=athanFont,anchor=S)
    athanLabelArabic = Label(master, bg="#111111", fg="#ffffff",font=athanFont, anchor=N)
    blackLabel = Label(master, textvariable=blackenVar, bg="#111111", fg="#ffffff",font=countdownFont)
    athanImageLabel = Label(master, bg="#111111", fg="#ffffff", image=renderNoPhoneAthan)


    def updateStringvars():
        today = getDayInfo(time.localtime()[7])
        islamicDateVar.set(today["IslamicDate"])
        tomorrow = getDayInfo(time.localtime()[7] + 1)
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
        jummahVar.set(stringTime(minuteTime(today["PrayerTimes"][1])-config.jummahLength))
        if (not alreadyDone(today["StartTimes"][0])):
            seherVar.set(today["Seher"])
        else:
            seherVar.set(tomorrow["Seher"])
        sunriseVar.set(today["Sunrise"])
        zawalVar.set(stringTime(minuteTime(today["StartTimes"][1])-10))

        noPhoneVar.set(str(silenceMobile()[1]) + "\n" + silenceMobile()[2])

        nextIndex = 0
        try:
            while (minuteTime(today["StartTimes"][nextIndex]) < minuteTime(currentStringTime())):
                nextIndex += 1
        except:
            nextIndex = 0

        blackenVar.set(str(int(blackenScreen()[1]/60%60)) + ":" + str(int(blackenScreen()[1]%60)).rjust(2,"0"))

    def updateColors():
        today = getDayInfo(time.localtime()[7])
        for row, start in enumerate(today["StartTimes"]):
            if (minuteTime(currentStringTime()) < minuteTime(start) and minuteTime(start) - minuteTime(
                    currentStringTime()) < 2 and int(time.time()) % 2 == 0):
                prayerStartPrayerTimes[row][0].config(fg="#ee1111")
            else:
                prayerStartPrayerTimes[row][0].config(fg="#111111")
        for row, prayer in enumerate(today["PrayerTimes"]):
            if (minuteTime(currentStringTime()) < minuteTime(prayer) and minuteTime(prayer) - minuteTime(
                    currentStringTime()) < 2 and int(time.time()) % 2 == 0):
                prayerStartPrayerTimes[row][1].config(fg="#ee1111")
            else:
                prayerStartPrayerTimes[row][1].config(fg="#111111")
        if (int(time.time()) % 2 == 0):
            blackLabel.config(fg="#ee1111")
        else:
            blackLabel.config(fg="#eeeeee")


    def placeRegularScreen():
        backLabel.place(relx=0,rely=0,relwidth=1,relheight=1)
        timeCanvas.place(relx=0.24, rely=-0.01, relwidth=0.52, relheight=0.12)
        gregorianDateLabel.place(relx=0, rely=0, relwidth=0.25, relheight=0.1)
        islamicDateLabel.place(relx=0.75, rely=0, relwidth=0.25, relheight=0.1)
        headerFrame.place(relx=0, rely=0.1, relwidth=1, relheight=0.05)
        for row in range(5):
            prayerFrames[row].place(relx=0, rely=0.15 + ((0.6 * row) / 5), relwidth=1, relheight=0.59 / 5)
        jummahFrame.place(relx=0, rely=0.75, relwidth=0.25, relheight=0.125)
        seherFrame.place(relx=0.25, rely=0.75, relwidth=0.25, relheight=0.125)
        sunriseFrame.place(relx=0.5, rely=0.75, relwidth=0.25, relheight=0.125)
        zawalFrame.place(relx=0.75, rely=0.75, relwidth=0.25, relheight=0.125)
        logoLabel.place(relx=0, rely=0.875, relwidth=0.2, relheight=0.125)
        socialFrame.place(relx=0.775, rely=0.875, relwidth=0.2, relheight=0.105)
        atLabel.place(relx=0.775, rely=0.965, relwidth=0.2, relheight=0.02)
        bottomLabelArabic.place(relx=0, rely=0.875, relwidth=1, relheight=0.125/2)
        bottomLabelEnglish.place(relx=0, rely=0.875+(0.125/2), relwidth=1, relheight=0.125/2)


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
        athanImageLabel.place(relx=0,rely=1/3, relwidth=1, relheight=1/3)
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
        timeCanvas.itemconfig(timeText,text="{}:{}:{}".format(time.localtime()[3], str(time.localtime()[4]).rjust(2, "0"), str(time.localtime()[5]).rjust(2, "0")))
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

        if (silenceMobile()[0]):
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
                if (silenceMobile()[5]):
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
