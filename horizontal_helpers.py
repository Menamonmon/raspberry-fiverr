from helpers import *


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


def silenceMobile(csv_rows):
    tm = time.localtime()
    yearDay = tm[7] - 1
    keys = ['FAJR prayer', 'DUHR prayer',
            'ASAR prayer', 'M/RIB prayer', 'ISHA prayer']

    friday_prayer_end_hour, friday_prayer_end_minute = map(
        int, fridayPrayerEnd.split(":"))
    friday_prayer_end_time = friday_prayer_end_hour * 60 + friday_prayer_end_minute
    if tm[6] == 4 and tm[3] * 60 + tm[4] < friday_prayer_end_time and tm[3] * 60 + tm[4] > friday_prayer_end_time:
        return True, 'Jummah', csv_rows[yearDay][keys[1]]

    for index, prayer in enumerate(prayers):
        prayerTime = csv_rows[yearDay][keys[index]]
        hm = prayerTime.split(":")
        hm = [int(hm[0]) + 12 * (index != 0), int(hm[1])]
        pt = hm[0] * 60 + hm[1]
        ct = tm[3] * 60 + tm[4]
        if (ct - pt < noMobileTimes[index] and ct - pt >= 0):
            return True, prayer, prayerTime
    return False, None


def updateCountdown(csv_rows, countdownVar):
    tm = time.localtime()
    yearDay = tm[7] - 1
    keys = ['FAJR start', 'DUHR start',
            'ASAR start', 'M/RIB start', 'ISHA start']
    for index, prayer in enumerate(prayers):
        prayerTime = csv_rows[yearDay][keys[index]]
        hm = prayerTime.split(":")
        hm = [
            int(hm[0]) + 12 * (((index == 1 and int(hm[0]) < 6) or index > 1)), int(hm[1])]
        pt = hm[0] * 60 + hm[1]
        ct = tm[3] * 60 + tm[4]
        if (ct < pt):
            hours = hm[0] - tm[3] - (hm[1] - tm[4] - 1 < 0)
            minutes = (hm[1] - tm[4] - 1) % 60
            seconds = 60 - tm[5]
            countdownVar.set(f"{hours}:{minutes:02}:{seconds:02}")
            break
        else:
            countdownVar.set("00:00:00")
