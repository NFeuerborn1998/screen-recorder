from tkinter import *
from tkinter import messagebox

top = Tk()
top.geometry("1000x500")           #sets size of the window

def onRecordClick():                              #changes the recording button between starting and stopping
    if(recordButton['text']=="Start Recording"):
        recordButton['text']="Stop Recording"
    else:
        recordButton['text']="Start Recording"

recordButton = Button(top, text = "Start Recording", command = onRecordClick)  #creates the recording button
recordButton.place(x = 35,y = 50)

saveButton = Button(top, text = "Browse Save Location")  #creates the saving location button
saveButton.place(x = 170,y = 50)

CheckVar1 = IntVar()
delayCheck = Checkbutton(top, text = "5s Delay", variable = CheckVar1, onvalue = 1, offvalue = 0)   #creates the delay check box
delayCheck.place(x = 35, y = 80)  

CheckVar2 = IntVar()
cameraCheck = Checkbutton(top, text = "Record Camera", variable = CheckVar2, onvalue = 1, offvalue = 0)   #creates the record camera button
cameraCheck.place(x = 35, y = 110)

variable = StringVar(top)
variable.set("Top-Left")
cameraDropMenu = OptionMenu(top, variable, "Top-Left", "Top-Right", "Bottom-Left", "Bottom-Right")   #creates the drop down menu to select camera location
cameraDropMenu.place(x = 33, y = 150)
cameraDropMenu.config(width = 12)                                                                    #sets length of drop menu to remain the same

top.mainloop()

