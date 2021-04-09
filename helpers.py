import math
import datetime
import time
import calendar
import csv
import pprint
from ummalqura.hijri_date import HijriDate
from consts import *


def minuteTime(s):
    return int(s.split(":")[0]) * 60 + int(s.split(":")[1])


def stringTime(m):
    return str(math.floor(m / 60)) + ":" + str(math.floor(m % 60)).rjust(2, "0")


def currentStringTime():
    return str(time.localtime()[3]) + ":" + str(time.localtime()[4]).rjust(2, "0")


def getDayInfo(day, csvRows):
    ret = {}
    day -= 1
    dt = datetime.date.fromordinal(day)
    td = datetime.date.today()
    um = HijriDate(td.year, dt.month, dt.day, gr=True)
    islamicMonths = ["Muharram", "Safar", "Rabi\' al-awwal", "Rabi\' al-thani", "Jumada al-awwal",
                     "Jumada al-thani", "Rajab", "Sha\'ban", "Ramadan", "Shawwal", "Dhu al-Qi'dah", "Dhu al-Hijjah"]
    gregorianDate = ("{} {} {} {}".format(
        um.day_name_en[0:3].upper(), dt.day, um.month_name_gr[0:3].upper(), td.year))
    islamicDate = ("{} {} {}".format(
        um.day, islamicMonths[um.month-1], um.year))
    if (calendar.weekday(td.year, dt.month, dt.day) == 4):
        prayerNames = ['FAJAR', 'JUMMAH', 'ASAR', 'MAGHRIB', 'ISHA']
        prayerNamesArabic = ['فجر', 'جمعه', 'عصر', 'مغرب', 'عشاء']
    else:
        prayerNames = ['FAJAR', 'ZUHR', 'ASAR', 'MAGHRIB', 'ISHA']
        prayerNamesArabic = ['فجر', 'ظهر', 'عصر', 'مغرب', 'عشاء']
    prayerTimes = []
    prayerKeys = ['FAJR prayer', 'DUHR prayer',
                  'ASAR prayer', 'M/RIB prayer', 'ISHA prayer']
    for key in prayerKeys:
        prayerTimes.append(str(int(csvRows[day][key].split(":")[0]) + (12 * (key != "FAJR prayer"))) + ":" +
                           csvRows[day][key].split(":")[1])
    startTimes = []
    startKeys = ['FAJR start', 'DUHR start',
                 'ASAR start', 'M/RIB start', 'ISHA start']
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


def read_csv_rows(filename):
    with open(filename) as f:
        dictreader = csv.DictReader(f)
        return [row for row in dictreader]


def isRamadan():
    tm = time.localtime()
    yearDay = tm[7] - 1
    leap = (tm[0] % 4 == 0)
    return (yearDay >= 112 + leap and yearDay <= 142 + leap)


def blinkText(csv_rows):
    tm = time.localtime()
    yearDay = tm[7] - 1
    keys = ['FAJR start', 'DUHR start',
            'ASAR start', 'M/RIB start', 'ISHA start']
    for index in range(len(prayers)):
        prayerTime = csv_rows[yearDay][keys[index]]
        hm = prayerTime.split(":")
        hm = [int(hm[0]) + 12*(index != 0), int(hm[1])]
        pt = hm[0]*60 + hm[1]
        ct = tm[3]*60 + tm[4]
        if (ct < pt and pt - ct <= 2):
            return True
    return False


def getNextPrayer(csv_rows):
    tm = time.localtime()
    yearDay = tm[7] - 1
    keys = ['FAJR prayer', 'DUHR prayer',
            'ASAR prayer', 'M/RIB prayer', 'ISHA prayer']
    for index, prayer in enumerate(prayers):
        prayerTime = csv_rows[yearDay][keys[index]]
        hm = prayerTime.split(":")
        hm = [int(hm[0]) + 12*(index != 0), int(hm[1])]
        pt = hm[0]*60 + hm[1]
        ct = tm[3]*60 + tm[4]
        if (ct < pt):
            return prayer, hm, arabic_prayers[index]
    prayerTime = csv_rows[yearDay+1][keys[0]]
    hm = prayerTime.split(":")
    hm = [int(hm[0]), int(hm[1])]
    return prayers[0], hm, arabic_prayers[0]


def get_now():
    return datetime.datetime.fromtimestamp(time.mktime(time.localtime()))


def updateClock(timeVar, seconds=False):
    dt = get_now()
    seconds = False
    time_str = dt.strftime(
        f"{'%H' if clock24hr else '%I'}:%M{':%S' if seconds else ''}")
    timeVar.set(time_str)


def silenceMobile():
    tm = time.localtime()
    yearDay = tm[7] - 1
    keys = ['FAJR prayer', 'DUHR prayer',
            'ASAR prayer', 'M/RIB prayer', 'ISHA prayer']

    if (tm[6] == 4 and tm[3] * 60 + tm[4] < int(config.fridayPrayerEnd.split(":")[0]) * 60 + int(config.fridayPrayerEnd.split(":")[1]) and tm[3] * 60 + tm[4] > int(config.fridayPrayerStart.split(":")[0]) * 60 + int(config.fridayPrayerStart.split(":")[1])):
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


def kill_window(master):
    master.destroy()
