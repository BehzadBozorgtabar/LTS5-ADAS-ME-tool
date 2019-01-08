#Imports from the local program
from tkinter import *
from interface.video_frame import VideoFrame
from interface.annotations import AnnotatorFrame
from interface.graphic_frame import GraphFrame
from ReadSMBBinaryFile.extract_roi_data import SMB
from interface.data import *

#Python modules
import os
import numpy as np


"""
Draws annotation interface.
Argument:
	- file_to_annotate: the location of the data
	- savePath: The path where we save the annotation
"""
def draw_annotation_interface(file_to_annotate, savePath):

	#opens the video file
	video = 0
	vidWidth = 0
	vidHeight = 0
	
	video = SMB(file_to_annotate)
	vidWidth, vidHeight = video.imageParams()

	nbrFrames = video.get(NBR_FRAMES)
	part = video.part()

	# Setup interface
	main_nbr_rows = 10
	main_nbr_cols = 10
	
	# interface initialisation
	interface = Tk()
	ws = interface.winfo_screenwidth()
	hs = interface.winfo_screenheight()
	L,H,X,Y = ws*0.75, hs*0.75, ws/8, hs/8 

	#interface.geometry("%dx%d%+d%+d" % (L,H,X,Y))
	interface.geometry("1400x700+200+200")
	interface.title('Emotion facial recognition annotation tool')
	interface['bg'] = 'black'
	interface.resizable(width = False, height = False)
	

	# configuration of the grid task manager
	for x in range(0, main_nbr_rows):
		interface.rowconfigure(x, weight=1)

	for x in range(0, main_nbr_cols):
		interface.columnconfigure(x, weight=1)

	# Panels
	annotator_frame = AnnotatorFrame(interface, fg = 'black', text = "2. Annotation")
	annotator_frame.grid(row = 0, rowspan = 6, column = 5, columnspan = 5, padx = pad, pady = pad, sticky = stick)
	annotator_frame.grid_propagate(0)
	
	graph_frame = GraphFrame(interface, bg = 'white', text = "3. Graph")
	graph_frame.grid(row = 6, rowspan = 4, column = 5, columnspan = 5, padx = pad, pady = pad, sticky = stick)
	graph_frame.grid_propagate(0)

	video_frame = VideoFrame(interface, file_to_annotate, savePath, annotator_frame, graph_frame, video, vidWidth, vidHeight, part, nbrFrames, bg = "green", fg = 'white', text = "1. Data")
	video_frame.grid(row = 0, rowspan = 10, column = 0, columnspan = 5, padx = 5, pady = 5, sticky = stick)
	video_frame.grid_propagate(0)

	try:
		interface.mainloop()
	except KeyboardInterrupt:
		interface.destroy()
		exit()


"""
Draws the start interface, shows directories or files.
The user has to select an element listed.
Attributes:
	- filename: the file or directory the user is selecting
	- toAnnotatePath: the actual location of the user in the server or local repository
	- dirList: file or directories shown on the listbox
	- depth: the actual depth in the repository from the initial actual:location(see constructor)
	- depth_to_remove: the depth from / directory to the initial path the user wanted to be in
	- savePath: The path where we save the annotation
	
	- exit: exit Button to exit application
	- back: back Button to go back in the repository
	- validate: validate Button to open a file or a directory
	- listBox: the listBox displaying all files and directories in the actual location
"""
class AnnotationStarter(Frame):

	"""
	Constructor of the class.
	Arguments:
		- parent: the parent widget of the class
		- listToAnnotate: the first files or directories to show on the list box
		- actual_location: the actual location of the user in the server or local repository
		
		- depth_to_remove: the depth from / directory to the initial path the user wanted to be in
	"""
	def __init__(self, parent, listToAnnotate, actual_location, savePath, depth_to_remove, **kwargs):
		Frame.__init__(self, parent, **kwargs)

		self._parent = parent
		
		# Window initialization
		start_nbr_rows = 5
		start_nbr_cols = 3
		start_minsize = 60

		self._filename = ''
		self._toAnnotatePath = actual_location
		self._dirList = listToAnnotate
		self._depth = 0
		self._depth_to_remove = depth_to_remove
		self._savePath = savePath
		
		#configuration of the grid task manager
		for x in range(0, start_nbr_rows):
			parent.rowconfigure(x, weight=1, minsize = start_minsize)

		for x in range(0, start_nbr_cols):
			parent.columnconfigure(x, weight=1)

		#Exit button
		self._exit = Button(start, text = "Exit", fg = 'red', command = sys.exit)
		self._exit.grid(row = 4, column = 2, padx = pad, pady = pad, sticky = stick)
		self._exit.grid_propagate(False)

		#Back button
		self._back = Button(start, text = "Back", fg = 'red', state = 'disabled', command = self.__back)
		self._back.grid(row = 4, column = 1, padx = pad, pady = pad, sticky = stick)
		self._back.grid_propagate(False)

		#Validate button
		self._validate = Button(start, text = "Validate _/", fg = 'green', state = 'disabled', command = self.__validate_command)
		self._validate.grid(row = 4, column = 0, padx = pad, pady = pad, sticky = stick)
		self._validate.grid_propagate(False)

		#List box and scrollbar
		defil = Scrollbar(start, orient = 'vertical')
		defil.grid(row = 0, rowspan = 4, column = 2, sticky = 'ns')
		self._listBox = Listbox(start, height = 0, yscrollcommand = defil.set, selectforeground = 'green', selectmode = 'single')
		for elem in listToAnnotate:
			self._listBox.insert('end', elem)
		self._listBox.grid(row = 0, rowspan = 4, column = 0, columnspan = 2, sticky = stick)
		
		#Binds the listBox with the onselect method
		self._listBox.bind('<<ListboxSelect>>', lambda evt: self.__onselect(evt))
		defil['command'] = self._listBox.yview


	"""
	The validate command, opens the directory or the file selected.
	Arguments: 
		to_annotate: the name of the element selected in the listBox
		toAnnotatePath: the actual location of the user in the server or local repository
	"""
	def __validate_command(self):
		smb = self._filename[-4:]
		if not (smb == '.smb'):
			self._validate['state'] = 'disabled'
			self._depth += 1
			self._back['state'] = 'normal'
			self._toAnnotatePath = self._toAnnotatePath + self._filename + '/'
			self._listBox.delete(0, END)
			self._dirList = listDirectories(self._toAnnotatePath)
			for elem in self._dirList:
				self._listBox.insert('end', elem)
		else:
			self._back['state'] = 'disabled'
			self._parent.destroy()
			draw_annotation_interface(self._toAnnotatePath + self._filename, self._savePath + self._filename)

	"""
	Select method, sets filename[0] to the selected element
	"""
	def __onselect(self, evt):
		w = evt.widget
		index = int(w.curselection()[0])
		self._filename = w.get(index)
		self._validate['state'] = 'normal'

	"""
	back method, permits to go back in the repository
	"""
	def __back(self):
		self._validate['state'] = 'disabled'
		if self._depth == 1:
			self._back['state'] = 'disabled'
		self._depth -= 1
		lastDirectory = self._toAnnotatePath.split('/')[self._depth + self._depth_to_remove]
		to_remove = len(lastDirectory) + 1
		self._toAnnotatePath = self._toAnnotatePath[:-to_remove]
		self._listBox.delete(0, END)
		self._dirList = listDirectories(self._toAnnotatePath)
		for elem in self._dirList:
			self._listBox.insert('end', elem)

"""
Lists the directories in the current directory
Argument:
	- path: the actual location od the user in the repository
Returns the list of all files and directories at path
Throws an error if the path is not valid
"""
def listDirectories(path):
	list = []
	try:
		list = os.listdir(path)
		list = [x for x in list if (os.path.isdir(path + x) or x.endswith(".smb"))]
	except FileNotFoundError:
		print("The path", path, "doesn't exist! The application will shut down!")
		exit()
	return list
	

"""
The main program
"""
if __name__ == '__main__':

	toAnnotateList = [] #List all data to annotate in the directory
	toAnnotatePath = "data/files/" #The path we have to follow to fetch the data
	savePath = defaultSavePath #The path to save the annotation
	depth_to_remove = 0 #we remove the depth od the initial toAnnotatePath

	depth_to_remove = len(toAnnotatePath.split('/')) - 1
	toAnnotateList = listDirectories(toAnnotatePath)

	start = Tk()
	ws = start.winfo_screenwidth()
	hs = start.winfo_screenheight()
	X,Y = ws/3, hs/3 
	start.geometry("400x300%+d%+d" % (X,Y))
	start.title('Choose a data set to annotate')
	start['bg'] = 'black'
	start.resizable(width = False, height = False)
	
	interface = AnnotationStarter(start, toAnnotateList, toAnnotatePath, savePath, depth_to_remove)

	try:
		interface.mainloop()
	except KeyboardInterrupt:
		interface.destroy()
		exit()
	
		
