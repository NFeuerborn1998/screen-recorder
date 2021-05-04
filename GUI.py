from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import time
import cv2
import numpy as np
import pyautogui
import threading
from PIL import Image, ImageTk, ImageGrab
from tkinter import filedialog
import pyaudio
import wave
from scipy.io import wavfile
import ffmpeg


#######################Timer Functions###################################

class Timer:

    def __init__(self):              
        #initializes the class
        self.start_time = 0
        self.timing = None
        self.sec = 0
        self.holdTime = 0
        self.time = 0

    def timeDisplay(self):           
        #Starts displaying the amount of time from the start of the recording on the time
        self.sec = time.time() - self.start_time

        mins = self.sec // 60
        self.sec = self.sec % 60
        hours = mins // 60
        mins = mins % 60
        timerLabel.config(text = "Recording Time: {0}:{1}:{2}".format(int(hours),int(mins),int(self.sec)))
        self.timing = timerLabel.after(1000, self.timeDisplay)
        #https://www.geeksforgeeks.org/python-after-method-in-tkinter/

    def continueDisplay(self):           
        #continues displaying the amount of time from the start of the recording on the timer adding the old time

        self.sec = time.time() - self.start_time + self.holdTime

        mins = self.sec // 60
        self.sec = self.sec % 60
        hours = mins // 60
        mins = mins % 60
        timerLabel.config(text = "Recording Time: {0}:{1}:{2}".format(int(hours),int(mins),int(self.sec)))
        self.timing = timerLabel.after(1000, self.continueDisplay)
        #https://www.geeksforgeeks.org/python-after-method-in-tkinter/

    def setStartTime(self):           
         #sets the start time of the recording for future use
        start_time = self.getStartTime()
        if(start_time == 0):
            self.start_time = time.time()
    
    def getStartTime(self):            
        #gets the start time of the recording
        return self.start_time

    def restartStartTime(self):        
        #restarts the start time and stops the timer when stopping recording
        self.start_time = 0
        timerLabel.after_cancel(self.timing)
        self.timing = None
        self.holdTime = 0
        timerLabel['text'] = "Recording Time: 0:0:0"

    def setOldTime(self):              
        #holds the time for future use on the timer until it is reset
        self.holdTime += time.time() - self.start_time

    def pauseTime(self):                
        #pauses the timer and sets the start time to 0
        self.start_time = 0
        timerLabel.after_cancel(self.timing)

t = Timer()          
#sets up the class for use



SCREEN_SIZE = pyautogui.size()
fourcc=cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter()
video =cv2.VideoCapture(0) 
top = Tk()
top.title("Screen Recorder")       
#sets the title of the window
top.geometry("800x325")           
#sets size of the window
photo = PhotoImage(file = "icons/icon.png")
top.iconphoto(False, photo)


##################Record Options######################

recordOptions = Frame(top, width = 130, height = 180, bg = "gray85", highlightbackground="black", highlightthickness=1)     
#creates a background frame to group the recording options together
recordOptions.place(x = 28, y = 45)

recordLabel = Label(top, text = "Record Options", font = "bold")          
#creates the label text Record Option
recordLabel.place(x = 35, y = 20)

def onRecordClick():                              
    #changes the recording button between starting and stopping, as well as starts or stops recording
    if(recordButton['text']=="Start Recording"):
        recordButton['text']="Stop Recording"
        pauseButton.config(state = "normal")
        if CheckVar1.get() == 1:
            time.sleep(5)
        t.setStartTime()
        t.timeDisplay()
        startRecording()
        saveButton.config(state = DISABLED)

    else:
        recordButton['text']="Start Recording"
        pauseButton.config(state = "disabled")
        t.restartStartTime()
        stopRecording()
        voice.stopAudioRecording()
        saveButton.config(state = NORMAL)


recordButton = Button(top, text = "Start Recording", command = onRecordClick, width = 15)  
#creates the recording button
recordButton.place(x = 35,y = 50)

def onPauseClick():                                
    #changes the pause button between pause and resume, as well as pauses or resumes recording
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

pauseButton = Button(top, text = "Pause Recording", command = onPauseClick, state = "disabled", width = 15)         
#creates the pause button
pauseButton.place(x=35, y = 80)

CheckVar1 = IntVar()
delayCheck = Checkbutton(top, text = "5s Delay", bg = "gray85", variable = CheckVar1, onvalue = 1, offvalue = 0)   
#creates the delay check box
delayCheck.place(x = 35, y = 110)  

CheckVar2 = IntVar()
cameraCheck = Checkbutton(top, text = "Record Camera", bg = "gray85", variable = CheckVar2, onvalue = 1, offvalue = 0, state = DISABLED)   
#creates the record camera button
cameraCheck.place(x = 35, y = 135)

cameraLabel = Label(top, text = "Camera Location:", bg = "gray85")       
#Label for camera location
cameraLabel.place(x = 35, y = 165)

cameraDropMenu = ttk.Combobox(top, width = 14, values = ["Top-Left", "Top-Right", "Bottom-Left", "Bottom-Right"], state = "readonly")   
#creates the drop down menu to select camera location
cameraDropMenu.current(0)
cameraDropMenu.place(x = 37, y = 190)
cameraDropMenu.bind("<FocusIn>",lambda x: recordOptions.focus())

if video is None or not video.isOpened():     
    #if camera is not detected, this disables the record camera option
    cameraCheck.config(state = DISABLED)
else:
    cameraCheck.config(state = NORMAL)

#####################File Options####################

fileLabel = Label(top, text = "File Options", font = "bold")          
#creates the label text Record Option
fileLabel.place(x = 188, y = 20)

fileOptions = Frame(top, width = 130, height = 180, bg = "gray85", highlightbackground="black", highlightthickness=1)     
#creates a background frame to group the recording options together
fileOptions.place(x = 170, y = 45)

saveLabel = Label(top, text = "Save Location:", bg = "gray85")          
#creates the label text Record Option
saveLabel.place(x = 180, y = 85)

locationText = Text(top, width = 14, height = 3)         
#creates the textbox for showing the location where the mp4 will save
locationText.place(x = 177, y = 110)
filename = ""
locationText.insert("end", filename)
locationText.config(state = "disabled")    
#have to enable textbox, set the location text, and then disable the text box to show it without the user being able to manually change the text

def saveLocation():                         
    #this will grab the filename and display it in the location Text box
    global filename
    filename = filedialog.asksaveasfilename(title = "Select Save Location", filetypes = [("mp4 files", "*.mp4")]) 
    readLast = filename[-4:None]
    if readLast != ".mp4":     
        #this will make sure the filename doesn't end with .mp4.mp4
        filetype = ".mp4"
        filename += filetype
    locationText.config(state = "normal")
    locationText.delete("1.0", "end")
    locationText.insert("end", filename)
    locationText.config(state = "disabled")
    locationText.see(END)

locationButton = Button(top, text = "Choose Location", width = 14, command = saveLocation)  
#creates the saving location button
locationButton.place(x = 180, y = 55)

def mp4Save(): 
    #this will combine the output video and sound file into an mp4 and save it to the proper location
    try:
        #https://www.reddit.com/r/learnpython/comments/ey41dp/merging_video_and_audio_using_ffmpegpython/
        ffmpeg.overwrite_output=True
        video = ffmpeg.input("output.avi")
        audio = ffmpeg.input("output.wav")
        out = ffmpeg.output(video, audio, filename, vcodec='copy', acodec='aac', strict='experimental')
        out.overwrite_output().run()   #overwrites any mp4 with the same name
    except:
        error = messagebox.showerror(title = "Error", message = "Please select a location, and make a recording first.")

saveButton = Button(top, text = "Save MP4", font = "bold", width = 11, command = mp4Save)  
#this will save the video and convert it to MP4
saveButton.place(x = 180, y = 180)

####################Timer Display####################

timerDisplay = Frame(top, width = 272, height = 50, bg = "gray85", highlightbackground="black", highlightthickness=1)        
#creates the timer frame
timerDisplay.place(x = 28, y = 235)

timerLabel = Label(top, text = "Recording Time: 0:0:0", font = "bold", bg = "gray85")        
#sets up the timer label
timerLabel.place(x = 80, y = 247)

####################Recording Preview Display######################

recordImage = ImageTk.PhotoImage(Image.new('RGB', (426, 240), (0,0,0)))   
# sets the size of the screen recording preview

def previewScreen():        
    #inputs each recorded frame of the screen for the screen preview
    preview = True
    while preview:
        tempImg = pyautogui.screenshot()
        tempFrame = np.array(tempImg)
        tempFrame = cv2.resize(tempFrame, (426, 240))
        recordImage.paste(Image.fromarray(tempFrame))

threading.Thread(target=previewScreen, daemon=True).start()   
#threads the screen recording to run in the background

recordingPreview = Frame(top, width = 432, height = 246, highlightbackground = "black", highlightthickness = 1)    
#creates the frame around the screen preview
recordingPreview.place(x = 339, y = 44)
recordingScreens = Label(top, width = 426, height = 240, image = recordImage)        
#this is the label for where the screen preview goes
recordingScreens.place(x = 340, y = 45)

####################Recording Audio Modules#######################
class VoiceRecorder:
    def __init__(self): 
        #Inintializes the VoiceRecorder
        self.audio_format = pyaudio.paInt16 
        self.channels = 1
        self.sample_rate = 44100 #44100 bits/second
        self.chunk = int(0.03*self.sample_rate)

    def audioRecord(self): 
        #https://realpython.com/playing-and-recording-sound-python/
        #records the audio
        self.recUser_data = [] 
        self.p = pyaudio.PyAudio() 
        #initializes pyaudio
        self.stream = self.p.open(format=self.audio_format, channels=self.channels, rate=self.sample_rate, input=True, frames_per_buffer=self.chunk)

        while recording:
            data = self.stream.read(self.chunk)
            self.recUser_data.append(data)

    def stopAudioRecording(self):
            self.stream.stop_stream()
            #stops/closes stream
            self.stream.close()
            self.p.terminate()
            self.recUser_data = [np.frombuffer(frame, dtype=np.int16) for frame in self.recUser_data]
            wav = np.concatenate(self.recUser_data, axis=0)  #conversion of data taking place
            wavfile.write("output.wav", self.sample_rate, wav)

voice = VoiceRecorder()

####################Recording Screen Modules######################

def startRecording():                  
    #opens the screen recordings and starts threading the screenRecord method
    if not out.isOpened():
        out.open("output.avi", fourcc, 10, (SCREEN_SIZE))  
    global recording
    recording = True
    threading.Thread(target=screenRecord, daemon=True).start()
    threading.Thread(target=voice.audioRecord, daemon=True).start()

def screenRecord():                    
    #Starts recording the screen
    while recording:
        if CheckVar2.get() == 1:        
            #records the camera and screen
            #https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_core/py_image_arithmetics/py_image_arithmetics.html#:~:text=You%20can%20add%20two%20images,just%20be%20a%20scalar%20value.
            img = pyautogui.screenshot()
            ret, videoImg = video.read()
            frame = np.array(img)
            if ret is True:  
                videoImg = cv2.resize(videoImg, (426, 240))
                rows,cols,channels = videoImg.shape
                rows2,cols2,channels2 = frame.shape
                cols3 = cols2 - cols
                rows3 = rows2 - rows
            if ret is True:             
                #decides where to put the camera recording on the screen recording
                if cameraDropMenu.get() == "Top-Left":
                    frame[0:rows, 0:cols] = videoImg
                elif cameraDropMenu.get() == "Bottom-Left":
                    frame[rows3:rows2, 0:cols] = videoImg
                elif cameraDropMenu.get() == "Top-Right":
                    frame[0:rows, cols3:cols2] = videoImg
                else:
                    frame[rows3:rows2, cols3:cols2] = videoImg
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            time.sleep(1/90)
        else:                            
            #records only the screen without the camera
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        out.write(frame)

def pauseRecord():    
    #pauses the recording
    global recording
    recording = False

def resumeRecord():    
    #resumes the recording after screen
    global recording
    recording = True
    if not out.isOpened():
        out.open("output.avi", fourcc, 10, (SCREEN_SIZE))
    threading.Thread(target=screenRecord, daemon=True).start()
    threading.Thread(target=voice.audioRecord, daemon=True).start()

def stopRecording():    
    #stops the recording entirely and releases the video and camera recordings
    global recording
    recording = False
    out.release()
    video.release()

top.mainloop()
