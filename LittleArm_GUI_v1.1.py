#This program has a complete set of commands for most behaviors
#an improvement to the software would be for the arduino to wait until completion of the execution of the command before sending a ready signal

from Tkinter import *
import tkMessageBox
import time
import serial
import serial.tools.list_ports

#+++++++++++++Global Variables+++++++++++++++++++++

#This program has a complete set of commands for most behaviors
#an improvement to the software would be for the arduino to wait until completion of the execution of the command before sending a ready signal

from Tkinter import *
import tkFileDialog
import tkMessageBox
import time
import serial
import serial.tools.list_ports
import copy

#+++++++++++++Global Variables+++++++++++++++++++++

currentSequence = "motion_recording.txt"	#the file name of recording prei-intialized to the default
currentDirectoy = "/"						#defines the working directory of the user

loopStartStop = False

#This line of code is a manual alternative should the Arduino search function below fault
#To use Comment out the below While loop and change the COM# to the port the arduino is connected to based on the Device Mananger
#ser = serial.Serial('COM3', 9600, timeout = .1)

checker = 0  #Loop control
while checker == 0:
    #Find the serial port that the arduino is connected to
    ports = list(serial.tools.list_ports.comports())
    print ports
	
    for p in ports:
        
        print "Searching for Port ..."
        
        if "CH340"  in p[1]:
           
            print p[1]
            ser = serial.Serial(p[0], 9600, timeout = .5)
            checker = 1
            break
			
        if "Arduino" in p[1]:
            print "hello1"
            ser = serial.Serial(p[0], 9600, timeout = .5)
            checker = 1
            #print "Found the Arduino"
             		
        else:
	        print ("No Arduino Device was found connected to the computer")

#++++++++++++++++Functions+++++++++++++++++++++++

colors = {
    "spacer": "black",
    "background": "black",
    "frame": "black",
    "label": "gray",
    "speed": "#3366ff",
    "arm": "#00b300",
    "gripper": "red"
}

if sys.platform != "win32": 
    colors["spacer"] = "black"
    colors["background"] = "white"
    colors["frame"] = "white"

def move_it(aCommand):
    #this function sends the command of joint angles to the arduino to move the servos to the desired positions in real time with the GUI
    
    aCommand = 0  #unused holder to allow function to work live with scale bar

    ser.flushInput()
    ser.flushOutput()
    command = str(base.get()) + ',' + str(shoulder.get()) +   ',' + str(elbow.get())+','+ str(gripper.get())+','+ str(21 - theSpeed.get()) + '\n'
    print command
    ser.write(command)

    #wait until a repsonse if found from the arduino
    OK = 'no'
    while (OK != 'd'):
        OK = ser.read(1)
    
def recordArmPos():
    #This function records the current positions of the GUI and places them in a TXT file in the same directory as this program
    readPosCommand = str(base.get()) + ',' + str(shoulder.get()) +   ',' + str(elbow.get())+','+ str(gripper.get()) +','+ str(21 -theSpeed.get())+'\n'
    recordFile = open(currentSequence, 'a')
    print (currentSequence)
    recordFile.write(readPosCommand)
    recordFile.close()

def recordPause():
    #This function records the current positions of the GUI and places them in a TXT file in the same directory as this program
    pauseCommand = "pause" + '\n'
    recordFile = open(currentSequence, 'a')
    recordFile.write(pauseCommand)
    recordFile.close()    

def playback():
   #This function reads the record file created in recordArmPos() and send the commands to the arm so that a sequence may be repeated.
   recordFile = open(currentSequence, 'r')
   Count = 1
   for line in recordFile:
       Count = Count + 1
       recordedCommand = line

       #send the command to the arduino using another function
       sendCommand(recordedCommand)
   print ('Done')
   recordFile.close()

def sendCommand(anotherCommand):
    #this is a basic command function. It recieves the generic command in the form base,shoulder,elbow,effector\n and send it to the arduino and then waits to recieve confirmations that the arduino has processed it.
	#this function is a variation of move_it for the playback function
    ser.flushInput()
    ser.flushOutput()
    theCommand = anotherCommand 
    print theCommand

    if theCommand == "pause\n":
        time.sleep(1)
        return
    
    ser.write(theCommand)

    #wait until a repsonse if found from the arduino
    OK = 'no'
    while (OK != 'd'):
        OK = ser.read(1)
			
def goHome():
    #This function returns the robot to its initial positions and changed the GUI positions to match
    homePos = str(108) + ',' + str(154) + ',' + str(30)+ ',' + str(10) + ',' + str(4) + '\n'
    base.set(108)
    shoulder.set(154)
    elbow.set(30)
	
    sendCommand(homePos)
	
def clearFile():
    #this clears the file for a new sequence
    open(currentSequence, 'w').close()
	
def saveFileAs():
    #This function is called by the menubar
    #this function opens the current set of commands in the file motion_recording.txt and saves the contents to a new
    print "Saving a File I see"
    global currentSequence			#aacess the gloabl value of the current sequence
	
	#open the current file and copy its contents
    file = open(currentSequence, 'r')   
    textoutput = file.readlines()
    file.close()
	
	#open the new files and insert the contents
    theNewFile = tkFileDialog.asksaveasfilename(initialfile='Untitled.txt',defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])

    file = open(theNewFile, 'w')
    file.writelines(textoutput)		#not the writelines. write does not enter the data correctly from readlines
    file.close()
	
	#update the working file
    currentSequence = theNewFile	#update the file that is being used universally

def openFile():
    #this function sets the file that is being edited and recorded into
    global currentSequence
    currentSequence = tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("txt files","*.txt"),("all files","*.*")))
    print (currentSequence)
	
def newFile():
    #this function created a new .txt file to hold imput commands
    global currentSequence
	
	#open a new fle 
    theNewFile = tkFileDialog.asksaveasfilename(initialfile='Untitled.txt',defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])	#names the file and sets the location
    file = open(theNewFile, 'a')   #creates the file
    file.close()
    
    currentSequence = theNewFile	#update the file that is being used universally

def looper( ):
    #this function loops through a the current sequence repeatedly.
    #startStop is the boolean bit that stats looping
    if loopStartStop == 1:
        playback()
    root.after(1000, looper)	

def startLooper():
    global loopStartStop
    loopStartStop = 1

def stopLooper():
    global loopStartStop	
    loopStartStop = 0
	
#++++++++++++++++++++The GUI++++++++++++++++++++++
root = Tk()
root.wm_title("LittleArm")
root.configure(background = colors["background"])

#++++++++++++++++++Menu+++++++++++++++++++++++++
menubar = Menu(root)

filemenu = Menu(menubar, tearoff = 0)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=openFile)
filemenu.add_command(label= "New Sequence", command=newFile)

filemenu.add_command(label="Save Sequence As", command=saveFileAs)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

# display the menu
root.config(menu=menubar)

#+++++++++++++++++++++++spacer frame++++++++++++++++++++++++++++++++++
spacerFrameLeft = Frame(root, bg = colors["frame"])
spacerFrameLeft.grid(row = 0, column = 0 )


spacerLabel6 = Label(spacerFrameLeft,  bg = colors["spacer"], padx = 10)
spacerLabel6.grid(row = 0, column = 0 )

#+++++++++++++++++ARM+++++++++++++++++++++++++

# The scroll bars
armControl = Frame(root, background = colors["frame"])
armControl.grid(row = 0, column = 1 )

#armLabel = Label(armControl, text = "Arm Components", font = ("ARIAL", 24),relief = GROOVE, padx = 100)
#armLabel.pack()

spacerLabel = Label(armControl,  bg = colors["spacer"], padx = 100)
spacerLabel.grid(row = 1, column = 1 )

#++++++++++++++++++++++++BASE+++++++++++++++++++++++++++

baseLabel = Label(armControl, text = "Base", font = ("ARIAL", 16), relief = GROOVE, padx = 100, width = 9, bg = colors["arm"])
baseLabel.grid(row = 2, column = 1 )

base = Scale(armControl, from_= 5, to = 175, length = 306, orient = HORIZONTAL, troughcolor = colors["arm"], showvalue = 0, command = move_it)
base.set(108)
base.grid(row = 3, column = 1 )

#++++++++++++++++++++++++Shoulder+++++++++++++++++++++++++

shoulderLabel = Label(armControl, text = "Shoulder", font = ("ARIAL", 16),relief = GROOVE, padx = 100, width = 9, bg = colors["arm"])
shoulderLabel.grid(row = 4, column = 1 )

shoulder = Scale(armControl, from_= 5, to = 175, length = 306, orient = HORIZONTAL, troughcolor = colors["arm"], showvalue = 0,command = move_it)
shoulder.set(100)
shoulder.grid(row = 5, column = 1 )

#++++++++++++++++++++++ELBOW++++++++++++++++++++++++++++

elbowLabel = Label(armControl, text = "Elbow",font = ("ARIAL", 16), relief = GROOVE, padx = 100, width = 9, bg = colors["arm"])
elbowLabel.grid(row = 6, column = 1 )

elbow = Scale(armControl, from_= 5, to = 175, length = 306, orient = HORIZONTAL,troughcolor = colors["arm"], showvalue = 0, command = move_it)
elbow.set(30)
elbow.grid(row = 7, column = 1 )

#++++++++++++++++++++++++++++Gripper+++++++++++++++++++

gripperLabel = Label(armControl, text = "Gripper",font = ("ARIAL", 16), relief = GROOVE, padx = 100, width = 9, bg = colors["gripper"])
gripperLabel.grid(row = 8, column = 1 )

gripper = Scale(armControl, from_= 5, to = 75, length = 306, orient = HORIZONTAL, troughcolor = colors["gripper"], showvalue = 0,  command = move_it)
gripper.grid(row = 9, column = 1 )

#++++++++++++++++++++++++++Speed++++++++++++++++++++++++

spacerLabel2 = Label(armControl,  bg = colors["spacer"], padx = 100)
spacerLabel2.grid(row = 10, column = 1 )

speedLabel = Label(armControl, bg = colors["speed"], font = ("Arial", 16), text = "Speed", relief = GROOVE, padx = 100, width = 9)
speedLabel.grid(row = 11, column = 1 )

theSpeed = Scale(armControl, from_= 3, to = 20, length = 306, orient = HORIZONTAL, troughcolor = colors["speed"] ,command = move_it)
theSpeed.grid(row = 12, column = 1 )


spacerLabel3 = Label(armControl,  bg = colors["spacer"], padx = 100)
spacerLabel3.grid(row = 13, column = 1 )

pauseButton = Button(armControl, font = ("ARIAL", 16), text= "Pause for 1 Sec", width = 20, command = recordPause)
pauseButton.grid(row = 14, column = 1 )

homeButton = Button(armControl, font = ("ARIAL", 16), text= "Go Home", width = 20, command = goHome)
homeButton.grid(row = 15, column = 1 )

spacerLabel8 = Label(armControl,  bg = colors["spacer"], padx = 100)
spacerLabel8.grid(row = 16, column = 1 )

#+++++++++++++++++++++++space frame++++++++++++++++++++++++++++++++++

spacerFrame = Frame(root, bg = colors["frame"])
spacerFrame.grid(row = 0, column = 2 )

spacerLabel6 = Label(spacerFrame,  bg = colors["spacer"], padx = 20)
spacerLabel6.grid(row = 0, column = 0 )

#+++++++++++++++++++++++RECORD++++++++++++++++++++++++++++
recordButtons = Frame(root, bg = colors["frame"])
recordButtons.grid(row = 0, column = 3 )

spacerLabel4 = Label(recordButtons,  bg = colors["spacer"], padx = 100)
spacerLabel4.grid(row = 1, column = 2 )

recordButton = Button(recordButtons, font = ("ARIAL", 16),text = "Record Position", width = 20, command = recordArmPos)
recordButton.grid(row = 2, column = 2 )

spacerLabel9 = Label(recordButtons,  bg = colors["spacer"], padx = 100)
spacerLabel9.grid(row = 3, column = 2 )

playButton = Button(recordButtons, font = ("ARIAL", 16), text = "Play Sequence", width = 20, command = playback)
playButton.grid(row = 4, column = 2 )

clearButton = Button(recordButtons, font = ("ARIAL", 16), text = "Clear Sequence", width = 20, command = clearFile)
clearButton.grid(row = 5, column = 2 )

spacerLabel5 = Label(recordButtons,  bg = colors["spacer"], padx = 100)
spacerLabel5.grid(row = 6, column = 2 )

#++++++++Looping+++++++++++++++++++

loopStartButton = Button(recordButtons, font = ("ARIAL", 16), text = "Start Loop", width = 20, command = startLooper)
loopStartButton.grid(row = 7, column = 2 )
loopStopButton = Button(recordButtons, font = ("ARIAL", 16), text = "Stop Loop", width = 20, command = stopLooper)
loopStopButton.grid(row = 8, column = 2 )

#+++++++++++++++++++++++space frame++++++++++++++++++++++++++++++++++

spacerFrameRight = Frame(root, bg = colors["frame"])
spacerFrameRight.grid(row = 0, column = 4 )

spacerLabel7 = Label(spacerFrameRight,  bg = colors["spacer"], padx = 10)
spacerLabel7.grid(row = 0, column = 0 )

#+++++++++++++++++++++++++++Primary Loop+++++++++++++++++

root.after(1000, looper)
root.mainloop()

