from tkinter import *
from tkinter import ttk
from tkinter import messagebox

top = Tk()
top.title("Screen Recorder")       #sets the title of the window
top.geometry("1000x500")           #sets size of the window
photo = PhotoImage(file = "icons/icon.png")
top.iconphoto(False, photo)

##################Record Options######################

recordOptions = Frame(top, width = 130, height = 140, bg = "gray85", highlightbackground="black", highlightthickness=1)     #creates a background frame to group the recording options together
recordOptions.place(x = 28, y = 45)

recordLabel = Label(top, text = "Record Options", font = "bold")          #creates the label text Record Option
recordLabel.place(x = 35, y = 20)

def onRecordClick():                              #changes the recording button between starting and stopping
    if(recordButton['text']=="Start Recording"):
        recordButton['text']="Stop Recording"
    else:
        recordButton['text']="Start Recording"

recordButton = Button(top, text = "Start Recording", command = onRecordClick)  #creates the recording button
recordButton.place(x = 35,y = 50)

CheckVar1 = IntVar()
delayCheck = Checkbutton(top, text = "5s Delay", bg = "gray85", variable = CheckVar1, onvalue = 1, offvalue = 0)   #creates the delay check box
delayCheck.place(x = 35, y = 80)  

CheckVar2 = IntVar()
cameraCheck = Checkbutton(top, text = "Record Camera", bg = "gray85", variable = CheckVar2, onvalue = 1, offvalue = 0)   #creates the record camera button
cameraCheck.place(x = 35, y = 110)

cameraDropMenu = ttk.Combobox(top, width = 14, values = ["Top-Left", "Top-Right", "Bottom-Left", "Bottom-Right"], state = "readonly")   #creates the drop down menu to select camera location
cameraDropMenu.current(0)
cameraDropMenu.place(x = 33, y = 150)     
cameraDropMenu.bind("<FocusIn>",lambda x: recordOptions.focus())

#####################File Options####################

fileLabel = Label(top, text = "File Options", font = "bold")          #creates the label text Record Option
fileLabel.place(x = 188, y = 20)

fileOptions = Frame(top, width = 130, height = 140, bg = "gray85", highlightbackground="black", highlightthickness=1)     #creates a background frame to group the recording options together
fileOptions.place(x = 170, y = 45)

browseButton = Button(top, text = "Browse")  #creates the saving location button
browseButton.place(x = 180, y = 110)

locationText = Text(top, width = 14, height = 1)
locationText.place(x = 177, y = 78)
test = "test"
locationText.insert("end", test)
locationText.config(state = "disabled")

saveLabel = Label(top, text = "Save Location:", bg = "gray85")          #creates the label text Record Option
saveLabel.place(x = 180, y = 50)

####################Timer Display####################

timerLabel = Label(top, text = "Timer Display", font = "bold")
timerLabel.place(x = 40, y = 190)

timerDisplay = Frame(top, width = 180, height = 100, bg = "gray85", highlightbackground="black", highlightthickness=1)
timerDisplay.place(x = 28, y = 220)



top.mainloop()

