#        Aayush Chauhan
#		   MNNIT,Allahabad
#        Audio & Video player in python

import Tkinter as tk
import Tkconstants,tkFileDialog
import events                              # all required modules
import threading
import thread
import pygame
from tkFileDialog import askdirectory 
from subprocess import call
import vlc

top = tk.Tk()                                   # take window
w = 800
h = 600
wscreen = top.winfo_screenwidth()
hscreen = top.winfo_screenheight()
x =(wscreen/2) -(w/2)                      #set location of window to middle of screen
y =(hscreen/2) - (h/2)
top.geometry('%dx%d+%d+%d' % (w,h,x,y))
player = vlc.MediaPlayer("")

pygame.init()
pygame.mixer.init()
set= 0  
playTill = 0                                  	 # just a flag 
filename=""
file = ''   										#example


def music(file):
	print file
	pygame.mixer.music.load(file)         	 				   # you can refer to https://www.pygame.org/docs/ref/music.html
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy() and playTill == 0:
		pygame.time.Clock().tick(0)


def pause():
	pygame.mixer.music.pause()
	global set
	set=1

def browse():     # to change value of a global variable inside a function apply global  
	global file                                 				# method to browse music files in system
	top.filename = tkFileDialog.askopenfilename(initialdir="/home/${USER}/",title = "Choose Music file")
	file = top.filename
	

def playsong():
	global set
	print file
	if file != "" and set==0:
		t1 = threading.Thread(target = music ,args=(file,))      # separate thread to play music
		t1.setName("audio bajao")
		t1.start()
	elif set==1:
		pygame.mixer.music.unpause()


def playUtility(event):                                 
	playsong()


def pauseUtility(event):
	pause()


def stop():
	pygame.mixer.music.pause();
	global set 
	set = 0    												# set =0 ,means song is  not playing currently


def Restart():                                             #restart currently loaded mp3 file
	pygame.mixer.music.rewind()


def stopUtility(event):                                      #stop mp3 
	stop()


def restartUtility(event):                                             
	Restart()


def playvideo(file):                                    #play video designated by file variable
	# comm =  "/home/aayushshivam7/python\ projects/pygam_vlc.py "
	# call(["python","pygam_vlc.py","abc.mp4"])
	global player
	player = vlc.MediaPlayer(file)
	player.play()


def video():
	if file != "":
		t2 = threading.Thread(target = playvideo,args=(file,))
		t2.start()


def pauseVideo():
	player.pause()


def stopVideo():
	global file 
	player.stop() 
	# player = vlc.MediaPlayer("")
	file = ""


def pauseVideoUtility(event):
	pauseVideo()


#mp3 portion
B = tk.Button(top,text = "Play audio",command = playsong)              # putting buttons on tkinter window
P = tk.Button(top,text = "pause audio",command = pause)
S = tk.Button(top,text = "Stop audio",command = stop)
R = tk.Button(top,text = "Restart current song",command = Restart )

#video portion
V = tk.Button(top,text = "Play video",command = video)
PV = tk.Button(top,text = "Pause video",command = pauseVideo)
SV = tk.Button(top,text = "Stop video",command = stopVideo)

select = tk.Button(top,text="Browse files",command = browse)
top.bind("<p>",playUtility)                                     # binding keyboard shortcuts to buttons on window
top.bind("<s>",pauseUtility)
top.bind("<x>",stopUtility)
top.bind("<r>",restartUtility)
top.bind("<space>",pauseVideoUtility)
top.focus_set()


B.pack(pady=10)
P.pack(pady=10)
S.pack(pady=30)                                          # pack all items to the window
R.pack(pady=10)

V.pack(pady=10)
PV.pack(pady=10)
SV.pack(pady=10)


select.pack(pady=10)


top.mainloop()
pygame.quit()
t1.join()
t2.join()                                          #  wait for music thread to join main thread
