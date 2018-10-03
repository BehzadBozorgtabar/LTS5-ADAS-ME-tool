from tkinter import *
from interface.video_frame import VideoFrame
from interface.annotations import AnnotatorFrame
from interface.graphic_frame import GraphFrame
from interface.data import *

import os
import csv

def draw_annotation_interface(file_to_annotate):
	
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

	# Frames
	annotator_frame = AnnotatorFrame(interface, fg = 'black', text = "2. Annotation")
	annotator_frame.grid(row = 0, rowspan = 6, column = 5, columnspan = 5, padx = pad, pady = pad, sticky = stick)
	annotator_frame.grid_propagate(0)

	graph_frame = GraphFrame(interface, bg = 'white', text = "3. Graph")
	graph_frame.grid(row = 6, rowspan = 4, column = 5, columnspan = 5, padx = pad, pady = pad, sticky = stick)
	graph_frame.grid_propagate(0)

	video_frame = VideoFrame(interface, file_to_annotate, annotator_frame, graph_frame, bg = "green", fg = 'white', text = "1. Data")
	video_frame.grid(row = 0, rowspan = 10, column = 0, columnspan = 5, padx = 5, pady = 5, sticky = stick)
	video_frame.grid_propagate(0)

	"""
	These comments are code for a possibe update which consist to add a Menu Bar

	#Menu creation
		
	#menuBar = Menu(interface)
	#interface['menu'] = menuBar
	
	#saveMenu = Menu(menuBar)
	#menuBar.add_cascade(label='Save', menu = saveMenu)
	#saveMenu.add_command(label='Save all')
	#menuBar.add_command(label='Save all and exit', command = lambda : saveAll(video_frame))
	
	#resetMenu = Menu(menuBar)
	#menuBar.add_cascade(label='Reset', menu = resetMenu)
	#resetMenu.add_command(label='Reset all data')
	"""
	
	interface.mainloop()


def draw_start_interface(listToAnnotate):

	start_nbr_rows = 5
	start_nbr_cols = 3
	start_minsize = 60
	
	start = Tk()
	ws = start.winfo_screenwidth()
	hs = start.winfo_screenheight()
	X,Y = ws/3, hs/3 
	start.geometry("400x300%+d%+d" % (X,Y))
	start.title('Choose a data set to annotate')
	start['bg'] = 'black'
	start.resizable(width = False, height = False)

	#data that we want to annotate
	filename = ['']
	
	#configuration of the grid task manager
	for x in range(0, start_nbr_rows):
		start.rowconfigure(x, weight=1, minsize = start_minsize)

	for x in range(0, start_nbr_cols):
		start.columnconfigure(x, weight=1)

	#Exit
	exit = Button(start, text = "Exit", fg = 'red', command = sys.exit)
	exit.grid(row = 4, column = 2, padx = pad, pady = pad, sticky = stick)
	exit.grid_propagate(False)


	#validation
	def validate_command(to_annotate):
		start.destroy()
		draw_annotation_interface(to_annotate)

	validate = Button(start, text = "Validate _/", fg = 'green', state = 'disabled', command = lambda: validate_command(filename[0]))
	validate.grid(row = 4, column = 0, columnspan = 2, padx = pad, pady = pad, sticky = stick)
	validate.grid_propagate(False)
		

	#ListBox
	def onselect(evt, to_annotate):
		w = evt.widget
		index = int(w.curselection()[0])
		to_annotate[0] = w.get(index)
		validate['state'] = 'normal'


	defil = Scrollbar(start, orient = 'vertical')
	defil.grid(row = 0, rowspan = 4, column = 2, sticky = 'ns')
	listBox = Listbox(start, height = 0, yscrollcommand = defil.set, selectforeground = 'green', selectmode = 'single')
	for elem in listToAnnotate:
		listBox.insert('end', elem)
	listBox.grid(row = 0, rowspan = 4, column = 0, columnspan = 2, sticky = stick)
	listBox.bind('<<ListboxSelect>>', lambda evt: onselect(evt, filename))
	defil['command'] = listBox.yview


	start.mainloop()
	
import ReadSMBBinaryFile.extract_roi_data as smb

if __name__ == '__main__':

	#load data
	toAnnotateList = []

	"""
	An idea for a possible update to modify/finish previously annotated data

	annotatedList = []

	for filename in os.listdir(annotatedPath):
		if filename.endswith(".smb"):
			annotatedList.append(filename[:-4])
	"""

	for filename in os.listdir(toAnnotatePath):
		if filename.endswith(".smb") or (filename.endswith(".csv") and os.path.exists(toAnnotatePath + '/' + filename[:-4] + '.avi')):
			toAnnotateList.append(filename)

	draw_start_interface(toAnnotateList)
	
		
