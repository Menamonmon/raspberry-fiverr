import config


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
            (int(screen_width) * (1 / 2)), int(screen_height * (15 / 15)))
        renderEvent = ImageTk.PhotoImage(loadEvent)
        self.l = tk.Label(self.master, image=renderEvent)
        self.l.image = renderEvent

    def delta(self):
        return time.time() - self.deltaStart

    def draw(self):
        #        self.l.place_forget()
        self.l.place(relx=self.x, rely=self.y,
                     relwidth=self.w, relheight=self.h)

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
            self.events.append(Event(master, event, (config.eventType == "slide"),
                                     0, 0.5, (config.eventType == "slide"), config.imageTimes[index]))

    def showEvent(self):
        if(config.eventType == "slide"):
            i = self.events[self.eventIndex].show()
        elif(config.eventType == "scroll"):
            i = self.events[self.eventIndex].scroll()
        self.eventIndex += i
        if(self.eventIndex == len(self.events)):
            self.eventIndex = 0
