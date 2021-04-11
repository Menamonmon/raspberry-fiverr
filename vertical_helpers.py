from helpers import *


def silenceMobile(csv_rows):
    today = getDayInfo(time.localtime()[7], csv_rows)
    prayerTimes = today['PrayerTimes']
    currentTime = minuteTime(currentStringTime())
    dt = datetime.datetime.fromtimestamp(time.mktime(time.localtime()))
    if (dt.weekday() == 4 and minuteTime(currentStringTime()) >= minuteTime(fridayPrayerStart) and minuteTime(currentStringTime()) < minuteTime(fridayPrayerEnd)):
        return True, f"{dt.hour:02}:{dt.mintue:02}:{dt.second:02}", "Asar\n" + str(today['StartTimes'][2]), "1st", "2nd", True
    for index, prayerTime in enumerate(prayerTimes):
        prayerTime = minuteTime(prayerTime)
        if (currentTime - prayerTime < noMobileTimes[index] and currentTime - prayerTime >= 0):
            return True, today['PrayerNames'][index], stringTime(prayerTime), "None", "None", False
    return False, "No Prayer", "No Time", "None", "None", False



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

