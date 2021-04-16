from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import time
import cv2
import numpy as np
import pyautogui
import threading
from PIL import Image, ImageTk, ImageGrab

#######################Timer Functions###################################

class Timer:

    def __init__(self):              #initializes the class
        self.start_time = 0
        self.timing = None
        self.sec = 0
        self.holdTime = 0
        self.time = 0

    def timeDisplay(self):           #Starts displaying the amount of time from the start of the recording on the timer

        self.sec = time.time() - self.start_time


        mins = self.sec // 60
        self.sec = self.sec % 60
        hours = mins // 60
        mins = mins % 60
        timerLabel.config(text = "Recording Time: {0}:{1}:{2}".format(int(hours),int(mins),int(self.sec)))
        self.timing = timerLabel.after(1000, self.timeDisplay)

    def continueDisplay(self):           #continues displaying the amount of time from the start of the recording on the timer adding the old time

        self.sec = time.time() - self.start_time + self.holdTime

        mins = self.sec // 60
        self.sec = self.sec % 60
        hours = mins // 60
        mins = mins % 60
        timerLabel.config(text = "Recording Time: {0}:{1}:{2}".format(int(hours),int(mins),int(self.sec)))
        self.timing = timerLabel.after(1000, self.continueDisplay)

    def setStartTime(self):            #sets the start time of the recording for future use
        start_time = self.getStartTime()
        if(start_time == 0):
            self.start_time = time.time()
    
    def getStartTime(self):            #gets the start time of the recording
        return self.start_time

    def restartStartTime(self):        #restarts the start time and stops the timer when stopping recording
        self.start_time = 0
        timerLabel.after_cancel(self.timing)
        self.timing = None
        self.holdTime = 0
        timerLabel['text'] = "Recording Time: 0:0:0"

    def setOldTime(self):              #holds the time for future use on the timer until it is reset
        self.holdTime += time.time() - self.start_time

    def pauseTime(self):                #pauses the timer and sets the start time to 0
        self.start_time = 0
        timerLabel.after_cancel(self.timing)

t = Timer()          #sets up the class for use



SCREEN_SIZE = pyautogui.size()
fourcc=cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter()
video =cv2.VideoCapture(0) 
top = Tk()
top.title("Screen Recorder")       #sets the title of the window
top.geometry("800x325")           #sets size of the window
photo = PhotoImage(file = "icons/icon.png")
top.iconphoto(False, photo)


##################Record Options######################

recordOptions = Frame(top, width = 130, height = 180, bg = "gray85", highlightbackground="black", highlightthickness=1)     #creates a background frame to group the recording options together
recordOptions.place(x = 28, y = 45)

recordLabel = Label(top, text = "Record Options", font = "bold")          #creates the label text Record Option
recordLabel.place(x = 35, y = 20)

def onRecordClick():                              #changes the recording button between starting and stopping
    if(recordButton['text']=="Start Recording"):
        recordButton['text']="Stop Recording"
        pauseButton.config(state = "normal")
        t.setStartTime()
        t.timeDisplay()
        startRecording()

    else:
        recordButton['text']="Start Recording"
        pauseButton.config(state = "disabled")
        t.restartStartTime()
        stopRecording()


recordButton = Button(top, text = "Start Recording", command = onRecordClick, width = 15)  #creates the recording button
recordButton.place(x = 35,y = 50)

def onPauseClick():                                #changes the pause button between pause and resume
    if(pauseButton['text']=="Pause Recording"):
        pauseButton['text']="Resume Recording"
        t.setOldTime()
        t.pauseTime()
        pauseRecord()

    else:
        pauseButton['text']="Pause Recording"
        t.setStartTime()
        t.continueDisplay()
        resumeRecord()

pauseButton = Button(top, text = "Pause Recording", command = onPauseClick, state = "disabled", width = 15)         #creates the pause button
pauseButton.place(x=35, y = 80)

CheckVar1 = IntVar()
delayCheck = Checkbutton(top, text = "5s Delay", bg = "gray85", variable = CheckVar1, onvalue = 1, offvalue = 0)   #creates the delay check box
delayCheck.place(x = 35, y = 110)  

CheckVar2 = IntVar()
cameraCheck = Checkbutton(top, text = "Record Camera", bg = "gray85", variable = CheckVar2, onvalue = 1, offvalue = 0, state = DISABLED)   #creates the record camera button
cameraCheck.place(x = 35, y = 135)

cameraLabel = Label(top, text = "Camera Location:", bg = "gray85")       #Label for camera location
cameraLabel.place(x = 35, y = 165)

cameraDropMenu = ttk.Combobox(top, width = 14, values = ["Top-Left", "Top-Right", "Bottom-Left", "Bottom-Right"], state = "readonly")   #creates the drop down menu to select camera location
cameraDropMenu.current(0)
cameraDropMenu.place(x = 37, y = 190)     
cameraDropMenu.bind("<FocusIn>",lambda x: recordOptions.focus())

if video is None or not video.isOpened():
    cameraCheck.config(state = DISABLED)
else:
    cameraCheck.config(state = NORMAL)

#####################File Options####################

fileLabel = Label(top, text = "File Options", font = "bold")          #creates the label text Record Option
fileLabel.place(x = 188, y = 20)

fileOptions = Frame(top, width = 130, height = 180, bg = "gray85", highlightbackground="black", highlightthickness=1)     #creates a background frame to group the recording options together
fileOptions.place(x = 170, y = 45)

saveLabel = Label(top, text = "Save Location:", bg = "gray85")          #creates the label text Record Option
saveLabel.place(x = 180, y = 50)

locationText = Text(top, width = 14, height = 1)         #creates the extbox for showing the location where the mp4 will save
locationText.place(x = 177, y = 78)
test = "test"
locationText.insert("end", test)
locationText.config(state = "disabled")    #have to enable textbox, set the location text, and then disable the text box to show it without the user being able to manually change the text

locationButton = Button(top, text = "Choose Location", width = 14)  #creates the saving location button
locationButton.place(x = 180, y = 105)

####################Timer Display####################

#timerDisplayLabel = Label(top, text = "Timer Display", font = "bold")       #creates the label for the timer frame
#timerDisplayLabel.place(x = 40, y = 230)

timerDisplay = Frame(top, width = 272, height = 50, bg = "gray85", highlightbackground="black", highlightthickness=1)        #creates the timer frame
timerDisplay.place(x = 28, y = 235)

timerLabel = Label(top, text = "Recording Time: 0:0:0", font = "bold", bg = "gray85")        #sets up the timer label
timerLabel.place(x = 80, y = 247)

####################Recording Preview Display######################

recordImage = ImageTk.PhotoImage(Image.new('RGB', (426, 240), (0,0,0)))

def previewScreen():
    preview = True
    while preview:
        tempImg = pyautogui.screenshot()
        tempFrame = np.array(tempImg)
        tempFrame = cv2.cvtColor(tempFrame, cv2.COLOR_RGB2BGR)
        tempFrame = cv2.resize(tempFrame, (426, 240))
        recordImage.paste(Image.fromarray(tempFrame))
        time.sleep(1/30)

threading.Thread(target=previewScreen, daemon=True).start()

recordingPreview = Frame(top, width = 432, height = 246, highlightbackground = "black", highlightthickness = 1)
recordingPreview.place(x = 339, y = 44)
recordingScreens = Label(top, width = 426, height = 240, image = recordImage)
recordingScreens.place(x = 340, y = 45)


####################Recording Screen Modules######################


def startRecording():
    if not out.isOpened():
        out.open("output.avi", fourcc, 10, (SCREEN_SIZE))  
    threading.Thread(target=screenRecord, daemon=True).start()

def screenRecord():
    global recording
    recording = True
    while recording:
        if CheckVar2.get() == 1:
            img = pyautogui.screenshot()
            videoImg = video.read()
            frame = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            rows,cols,channels = videoImg.shape
            frame[0:rows, 0:cols] = dst
            frame = np.array(frame)
        else:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        #img = pyautogui.screenshot()
        #videoImg = video.read()
        #combinedFrame = cv2.addWeighted(np.float32(img),1,videoImg,1,0)
        #frame = np.array(combinedFrame)
        #frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        #if CheckVar2 == 1:

        #gray = cv2.cvtColor(videoFrame, cv2.COLOR_BGR2GRAY)

        out.write(frame)

def pauseRecord():
    global recording
    recording = False

def resumeRecord():
    global recording
    recording = True
    if not out.isOpened():
        out.open("output.avi", fourcc, 10, (SCREEN_SIZE))
    threading.Thread(target=screenRecord, daemon=True).start()

def stopRecording():
    global recording
    recording = False
    out.release()
    video.release()

top.mainloop()
