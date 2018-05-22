import tkinter #used for GUI
import json #save game/settings
import os #list directories
import pygame #render and move objects
import threading
from functools import partial #used to pass text to LoadSim
from tkinter import *

running = 0 #indicates if the sim is active
size = [300,300]  #size of display apon start up
save = {} #holds sim data of current sim

class GUILoader(threading.Thread):
	def __init__(self,id):
		threading.Thread.__init__(self)
		guiraw = open("gui.json") #loads GUI data
		gui = json.load(guiraw)
		if id == 0:
			gui[0][1][1]["Object"] = [x[:-5] for x in os.listdir("Saves")] #list of files from save folder without extension
			gui[0][1][1]["Command"] = ["partial(LoadSim, settings['Object'][z])"]*len(os.listdir("Saves")) #copies command to load save for each one
			self.root = Tk() #creates new instance of tk
		self.gui = gui[id]
	def pygame(self):#creates window for pygame
		window = tkinter.Frame(self.root,width=size[0],height=size[1])
		window.grid(columnspan=size[0],rowspan=size[1])
		window.pack(side = LEFT)
		os.environ["SDL_WINDOWID"] = str(window.winfo_id())
		os.environ["SDL_VIDEODRIVER"] = "windib"
		self.screen = pygame.display.set_mode(size)#sets up pygame
		self.screen.fill(pygame.Color(255,255,255))
		pygame.display.init()
	def menu(self): #creates menubar
		self.menubar = Menu(self.root) # creates new menu on root
		for x in range(len(self.gui)):
			object = self.gui[x]
			window = object[0]
			for y in range(len(object)-1): #loops through Options on menubar
				settings = object[y+1]
				#if not settings["Name"] in locals():
				globals()[settings["Name"]] = Menu(eval(window),tearoff=settings["Tear"]) #create object
				for z in range(len(settings["Object"])):
					globals()[settings["Name"]].add_command(label=settings["Object"][z],command=eval(settings["Command"][z])) #add button on object
				if settings["New"] == 1:
					eval(window).add_cascade(label=settings["Name"],menu=eval(settings["Name"])) # add object to menubar
	def start(self):
		self.root.title("2D Physics Simulator")
		self.root.config(menu=mainwindow.menubar)
		self.root.mainloop()

def LoadSim(localsave): #Loads save after button is clicked
	saveraw = open("Saves/"+localsave+".json")
	save =  json.load(saveraw)
	sim.load(save)
def NewSim(): #Creates new box to name new sim
	new = Toplevel(width="10c",height="2.5c")
	new.title("New Simulator")
	namelabel = Label(new,padx="0.5c",pady="1c",text="Name")
	namelabel.pack(side=LEFT)
	nameenter = Entry(new)
	nameenter.pack(side=RIGHT)
def Pass(): #temp
    pass
def ToggleRun(): #Toggles if the sim is acive
    global running
    if running == 0:
        Control.entryconfig(1,label="Pause")
        running = 1
    else:
        Control.entryconfig(1,label="Play")
        running = 0
def MainGui():
	mainmenu = GUILoader(0)
	mainmenu.menu()

class pygamemager(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def load(self,save):
		for x in range(len(save["Objects"])):
			object = save["Objects"][x]
			#if object["type"] == "rect":
			pygame.draw.rect(mainwindow.screen,(0,0,0),[10,10,20,20])
	def loop(self):
		pass
		
class objectmanager(pygamemager):
	def __init__(self,size):
		self.size = size
	def new_object(self,xy):
		pass
		#self.	
#bar.entryconfig(3,state="disabled")

mainwindow = GUILoader(0)
mainwindow.pygame()
mainwindow.menu()

sim = pygamemager()
#sim.loop()

pygame.draw.rect(mainwindow.screen,(0,0,0),[10,10,20,20])

mainwindow.start()
