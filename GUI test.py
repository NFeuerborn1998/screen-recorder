from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import time

class Timer:

    def __init__(self):
        self.start_time = 0
        self.timing = None

    def timeDisplay(self):

        sec = time.time() - self.start_time

        mins = sec // 60
        sec = sec % 60
        hours = mins // 60
        mins = mins % 60
        timerLabel.config(text = "Recording Time: {0}:{1}:{2}".format(int(hours),int(mins),int(sec)))
        self.timing = timerLabel.after(1000, self.timeDisplay)

    def setStartTime(self):
        start_time = self.getStartTime()
        if(start_time == 0):
            self.start_time = time.time()
    
    def getStartTime(self):
        return self.start_time

    def restartStartTime(self):
        self.start_time = 0
        timerLabel.after_cancel(self.timing)
        self.timing = None
        timerLabel['text'] = "Recording Time: 0:0:0"

t = Timer()

top = Tk()
top.title("Screen Recorder")       #sets the title of the window
top.geometry("1000x500")           #sets size of the window
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

    else:
        recordButton['text']="Start Recording"
        pauseButton.config(state = "disabled")
        t.restartStartTime()


recordButton = Button(top, text = "Start Recording", command = onRecordClick, width = 15)  #creates the recording button
recordButton.place(x = 35,y = 50)

pauseButton = Button(top, text = "Pause Recording", state = "disabled", width = 15)         #creates the pause button
pauseButton.place(x=35, y = 80)

CheckVar1 = IntVar()
delayCheck = Checkbutton(top, text = "5s Delay", bg = "gray85", variable = CheckVar1, onvalue = 1, offvalue = 0)   #creates the delay check box
delayCheck.place(x = 35, y = 110)  

CheckVar2 = IntVar()
cameraCheck = Checkbutton(top, text = "Record Camera", bg = "gray85", variable = CheckVar2, onvalue = 1, offvalue = 0)   #creates the record camera button
cameraCheck.place(x = 35, y = 135)

cameraLabel = Label(top, text = "Camera Location:", bg = "gray85")       #Label for camera location
cameraLabel.place(x = 35, y = 165)

cameraDropMenu = ttk.Combobox(top, width = 14, values = ["Top-Left", "Top-Right", "Bottom-Left", "Bottom-Right"], state = "readonly")   #creates the drop down menu to select camera location
cameraDropMenu.current(0)
cameraDropMenu.place(x = 37, y = 190)     
cameraDropMenu.bind("<FocusIn>",lambda x: recordOptions.focus())

#####################File Options####################

fileLabel = Label(top, text = "File Options", font = "bold")          #creates the label text Record Option
fileLabel.place(x = 188, y = 20)

fileOptions = Frame(top, width = 130, height = 140, bg = "gray85", highlightbackground="black", highlightthickness=1)     #creates a background frame to group the recording options together
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

saveButton = Button(top, text = "Save MP4", font = "bold", width = 11)
saveButton.place(x = 180, y = 140)

####################Timer Display####################

timerDisplayLabel = Label(top, text = "Timer Display", font = "bold")       #creates the label for the timer frame
timerDisplayLabel.place(x = 40, y = 230)

timerDisplay = Frame(top, width = 180, height = 100, bg = "gray85", highlightbackground="black", highlightthickness=1)        #creates the timer frame
timerDisplay.place(x = 28, y = 260)

timerLabel = Label(top, text = "Recording Time: 0:0:0", bg = "gray85")
timerLabel.place(x = 35, y = 275)



top.mainloop()

