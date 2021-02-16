from tkinter import *
from tkinter import messagebox

top = Tk()
top.geometry("1000x500")

def onclick():
    if(recordButton['text']=="Start Recording"):
        recordButton['text']="Stop Recording"
    else:
        recordButton['text']="Start Recording"

recordButton = Button(top, text = "Start Recording", command = onclick)
recordButton.place(x = 35,y = 50)

CheckVar1 = IntVar()
delayCheck = Checkbutton(top, text = "5s delay", variable = CheckVar1, onvalue = 1, offvalue = 0)
delayCheck.place(x = 35, y = 80)


top.mainloop()