#This program has a complete set of commands for most behaviors
#an improvement to the software would be for the arduino to wait until completion of the execution of the command before sending a ready signal

from Tkinter import *
import tkMessageBox
import time
import serial
import serial.tools.list_ports

#+++++++++++++Global Variables+++++++++++++++++++++

#This line of code is a manual alternative should the Arduino search function below fault
#To use Comment out the below While loop and change the COM# to the port the arduino is connected to based on the Device Mananger
#ser = serial.Serial('COM3', 9600, timeout = .1)

checker = 0  #Loop control
while checker == 0:
    #Find the serial port that the arduino is connected to
    ports = list(serial.tools.list_ports.comports())
    #print ports
    for p in ports:
        print p
        if "Arduino" or ("CH340") in p[1]:
            ser = serial.Serial(p[0], 9600, timeout = .25)
            checker = 1
        else:
	        print ("No Arduino Device was found connected to the computer")

#++++++++++++++++Functions+++++++++++++++++++++++

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
    recordFile = open('motion_recording.txt', 'a')
    recordFile.write(readPosCommand)
    recordFile.close()

def recordPause():
    #This function records the current positions of the GUI and places them in a TXT file in the same directory as this program
    pauseCommand = "pause" + '\n'
    recordFile = open('motion_recording.txt', 'a')
    recordFile.write(pauseCommand)
    recordFile.close()    


def playback():
   #This function reads the record file created in recordArmPos() and send the commands to the arm so that a sequence may be repeated.
   recordFile = open('motion_recording.txt', 'r')
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
    open('motion_recording.txt', 'w').close()

#++++++++++++++++++++The GUI++++++++++++++++++++++
root = Tk()
root.wm_title("LittleArm Interface")
root.configure(background = 'black')

#++++++++++++++++++++Drive Motors++++++++++++++++++

motorControl = Frame(root)
motorControl.pack()

forwardFrame = Frame(motorControl)
forwardFrame.pack()

backFrame = Frame(motorControl)
backFrame.pack (side = BOTTOM)

speedControl = Frame(root)
speedControl.pack()

#+++++++++++++++++ARM+++++++++++++++++++++++++
# The scroll bars
armControl = Frame(root, background = 'black')
armControl.pack( )

armLabel = Label(armControl, text = "Arm Components", font = ("ARIAL", 24),relief = GROOVE, padx = 100)
armLabel.pack()

spacerLabel = Label(armControl,  bg = 'SystemBackground', padx = 100)
spacerLabel.pack()

#++++++++++++++++++++++++BASE+++++++++++++++++++++++++++

baseLabel = Label(armControl, text = "Base", font = ("ARIAL", 16), relief = GROOVE, padx = 100, width = 9, bg = 'green')
baseLabel.pack()

base = Scale(armControl, from_= 5, to = 175, length = 306, orient = HORIZONTAL, troughcolor = 'green', showvalue = 0, highlightbackground = 'black', command = move_it)
base.set(108)
base.pack()

#++++++++++++++++++++++++Shoulder+++++++++++++++++++++++++

shoulderLabel = Label(armControl, text = "Shoulder", font = ("ARIAL", 16),relief = GROOVE, padx = 100, width = 9, bg = 'green')
shoulderLabel.pack()

shoulder = Scale(armControl, from_= 5, to = 175, length = 306, orient = HORIZONTAL, troughcolor = 'green', showvalue = 0,command = move_it)
shoulder.set(154)
shoulder.pack()

#++++++++++++++++++++++ELBOW++++++++++++++++++++++++++++

elbowLabel = Label(armControl, text = "Elbow",font = ("ARIAL", 16), relief = GROOVE, padx = 100, width = 9, bg = 'green')
elbowLabel.pack()

elbow = Scale(armControl, from_= 5, to = 175, length = 306, orient = HORIZONTAL,troughcolor = 'green', showvalue = 0, command = move_it)
elbow.set(30)
elbow.pack()

#++++++++++++++++++++++++++++Gripper+++++++++++++++++++

gripperLabel = Label(armControl, text = "Gripper",font = ("ARIAL", 16), relief = GROOVE, padx = 100, width = 9, bg = 'red')
gripperLabel.pack()

gripper = Scale(armControl, from_= 5, to = 75, length = 306, orient = HORIZONTAL, troughcolor = 'red', showvalue = 0,  command = move_it)
gripper.pack()

#++++++++++++++++++++++++++Speed++++++++++++++++++++++++

spacerLabel2 = Label(armControl,  bg = 'SystemBackground', padx = 100)
spacerLabel2.pack()

speedLabel = Label(armControl, font = ("Arial", 16), text = "Speed", relief = GROOVE, padx = 100, width = 9)
speedLabel.pack()

theSpeed = Scale(armControl, from_= 3, to = 20, length = 306, orient = HORIZONTAL, troughcolor = 'blue' ,command = move_it)
theSpeed.pack()

#+++++++++++++++++++++++RECORD++++++++++++++++++++++++++++
spacerLabel3 = Label(armControl,  bg = 'SystemBackground', padx = 100)
spacerLabel3.pack()

recordButtons = Frame(root, bg = 'black')
recordButtons.pack( )

pauseButton = Button(recordButtons,font = ("ARIAL", 16), text= "Pause for 1 Sec", width = 20, command = recordPause)
pauseButton.pack()

homeButton = Button(recordButtons,font = ("ARIAL", 16), text= "Go Home", width = 20, command = goHome)
homeButton.pack()

spacerLabel4 = Label(recordButtons,  bg = 'SystemBackground', padx = 100)
spacerLabel4.pack()

recordButton = Button(recordButtons, font = ("ARIAL", 16),text = "Record Position", width = 20, command = recordArmPos)
recordButton.pack()

playButton = Button(recordButtons, font = ("ARIAL", 16), text = "Play Sequence", width = 20, command = playback)
playButton.pack()

clearButton = Button(recordButtons, font = ("ARIAL", 16), text = "New Sequence", width = 20, command = clearFile)
clearButton.pack()

spacerLabel5 = Label(recordButtons,  bg = 'SystemBackground', padx = 100)
spacerLabel5.pack()
#+++++++++++++++++++++++++++Primaryu Loop+++++++++++++++++

root.mainloop()


