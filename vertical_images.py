from PIL import Image, ImageTk
from consts import screen_height, screen_width

loadLogo = Image.open("images/logoNoText.png").resize(
    (int(screen_height * (0.1125)), int(screen_height * (0.1125))))
renderLogo = ImageTk.PhotoImage(loadLogo)

loadNoPhone = Image.open("images/nophone.png").resize(
    (int(screen_width / 3), int(screen_width / 3)))
renderNoPhone = ImageTk.PhotoImage(loadNoPhone)

loadNoPhoneAthan = Image.open("images/nophone.png").resize(
    (int(screen_height / 3), int(screen_height / 3)))
renderNoPhoneAthan = ImageTk.PhotoImage(loadNoPhoneAthan)

loadfb = Image.open("images/facebook.png").resize(
    (int(screen_height * 0.03), int(screen_height * 0.03)))
renderfb = ImageTk.PhotoImage(loadfb)
loadtw = Image.open("images/twitter.png").resize(
    (int(screen_height * 0.03), int(screen_height * 0.03)))
rendertw = ImageTk.PhotoImage(loadtw)
loadin = Image.open("images/instagram.png").resize(
    (int(screen_height * 0.03), int(screen_height * 0.03)))
renderin = ImageTk.PhotoImage(loadin)
loadyt = Image.open("images/youtube.png").resize(
    (int(screen_height * 0.03), int(screen_height * 0.03)))
renderyt = ImageTk.PhotoImage(loadyt)
loadjummah = Image.open("images/jummahArabic.png").resize(
    (int(screen_width * 0.175), int(screen_height * 0.033)))
renderjummah = ImageTk.PhotoImage(loadjummah)
loadseher = Image.open("images/seherArabic.png").resize(
    (int(screen_width * 0.175), int(screen_height * 0.033)))
renderseher = ImageTk.PhotoImage(loadseher)
loadsunrise = Image.open("images/sunriseArabic.png").resize(
    (int(screen_width * 0.175), int(screen_height * 0.033)))
rendersunrise = ImageTk.PhotoImage(loadsunrise)
loadzawal = Image.open("images/zawalArabic.png").resize(
    (int(screen_width * 0.175), int(screen_height * 0.033)))
renderzawal = ImageTk.PhotoImage(loadzawal)
loadtitle = Image.open("images/titleArabic.png").resize(
    (int(screen_width * 0.4), int(screen_height * 0.05)))
rendertitle = ImageTk.PhotoImage(loadtitle)
loadhadith = Image.open("images/hadithArabic.png").resize(
    (int(screen_width * 0.9), int(screen_height * 0.1)))
renderhadith = ImageTk.PhotoImage(loadhadith)


blackenImages = []
blackenImageKeys = ['fajar', 'zuhr', 'asar',
                    'maghrib', 'isha', "seher", "sunrise"]
for i in range(len(blackenImageKeys)):
    tmpArr = []
    tmpArr.append(Image.open(f"images/{blackenImageKeys[0]}Athan.png").resize(
        (int(screen_width * 0.4), int(screen_height * 0.075))))
    tkImage = ImageTk.PhotoImage(tmpArr[0])
    tmpArr.append(tkImage)
    blackenImages.append(tmpArr)
for i in range(5):
    tmpArr = []
    tmpArr.append(Image.open(f"images/{blackenImageKeys[i]}Prayer.png").resize(
        (int(screen_width * 0.4), int(screen_height * 0.075))))
    tkImage = ImageTk.PhotoImage(tmpArr[0])
    tmpArr.append(tkImage)
    blackenImages.append(tmpArr)

prayerImages = []
prayerImageKeys = ['fajar', 'zuhr', 'asar', 'maghrib', 'isha', 'jummah']
for i in range(6):
    tmpArr = []
    tmpArr.append(Image.open(f"images/{prayerImageKeys[i]}Arabic.png").resize(
        (int(screen_width * 0.175), int(screen_height * 0.033))))
    tkImage = ImageTk.PhotoImage(tmpArr[0])
    tmpArr.append(tkImage)
    prayerImages.append(tmpArr)
