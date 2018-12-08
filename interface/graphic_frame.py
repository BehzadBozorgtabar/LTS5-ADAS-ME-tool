#Imports from the project's modules
from tkinter import *
from interface.data import *

#Hight level API imports
import matplotlib
import matplotlib.ticker as tick
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

"""
It represents the graph which will show us the previous valence and arousal
annotations done with respect of the last frame annotated

Attributes: 
	- figure: the matplotlib figure which contains the graph
	- ax: the graph
	- memory: a tuple which contains informations about the last save (data, first annotated, last annotated, current frame)
	- canvas: the tkinter frame which encapsulates the graph

	- listChoice: list of number of segment the user could choose to analyse the graph
	- nbrSeg: variable linked to the choice of the user
"""
class GraphFrame(LabelFrame):
	

	def __init__(self, parent, **kwargs):
		LabelFrame.__init__(self, parent, **kwargs)

		#Creation of the graph
		self._figure = Figure(figsize = (0.1,0.1), dpi = 60)
		self._ax = self._figure.add_subplot(111)
		
		self._memory = ([], first_index, first_index, first_index)
		self.__setup(first_frame, first_frame + SEGMENT_SIZE, Y_LOWER_BOUND, Y_UPPER_BOUND, 1.0)

		self._canvas = FigureCanvasTkAgg(self._figure, self)
		self._canvas.get_tk_widget().pack(side = TOP, fill = BOTH, expand = True)

		valenceLabel = Label(self, text = "______ Valence", bg = 'white', fg = 'orange')
		arousalLabel = Label(self, text = "______ Arousal", bg = 'white', fg = 'blue')
		lastAnnotatedLabel = Label(self, text = "______ Last frame annotated", bg = 'white', fg = 'red')

		valenceLabel.place(relx = 0.2, rely = 0.05)
		arousalLabel.place(relx = 0.4, rely = 0.05)
		lastAnnotatedLabel.place(relx = 0.6, rely = 0.05)


		#Creation of RadioButtons to choose how many segments to show
		self._listChoice = [1,2,5,10]
		self._nbrSeg = IntVar()
		self._nbrSeg.set(1)

		for x in range(0, len(self._listChoice)):
			rb = Radiobutton(self, bg = 'white', text = str(self._listChoice[x]), variable = self._nbrSeg, value = self._listChoice[x], command = lambda : self.plotGraph(self._memory[0], max(self._memory[1] - SEGMENT_SIZE * self._nbrSeg.get(), first_index), self._memory[2], self._memory[3]))
			rb.place(relx = 0.025, rely = 0.3 + 0.1*x)
		 

	"""
	It setups the graph
	Arguments:
		- xLower: the min x
		- xUpper: the max x
		- yLower: the min y
		- yUpper: the max y
		- tickInterval: the interval between each major tick
	"""
	def __setup(self, xLower, xUpper, yLower, yUpper, tickInterval):
		self._ax.set_xlabel(xLabel)
		self._ax.set_xbound(xLower,xUpper)
		self._ax.xaxis.set_minor_locator(tick.MultipleLocator(DEFAULT_TICK))
		self._ax.xaxis.set_major_locator(tick.MultipleLocator(tickInterval))
		
		self._ax.set_ylabel(yLabel)
		self._ax.set_ybound(yLower, yUpper)
		self._ax.yaxis.set_major_locator(tick.MultipleLocator(DEFAULT_TICK))

		self._ax.grid(which = 'minor', linestyle = '--', alpha = 0.2)
		self._ax.grid(which = 'major')


	"""
	Plots the graph after an annotation saved
	Arguments:
		- data: all annotations done before
		- firstAnnotated: the frame annotated
		- lastAnnotated: last frame annotated
		- currAnnotation: the current frame annotated
	Be careful:
		- firstAnnotated and lastAnnotated are the programming indexes of frames
		- right_bound and left_bound are the real indexes of frames
	"""
	def plotGraph(self, data, firstAnnotated, lastAnnotated, currAnnotation):
		self._memory = (data, firstAnnotated, lastAnnotated, currAnnotation)
		self._ax.cla()
		repair = min(lastAnnotated, currAnnotation)
		right_bound = max(repair + 1,  first_index + SEGMENT_SIZE)
		left_bound = max(firstAnnotated + 1, right_bound - SEGMENT_SIZE * self._nbrSeg.get()) 
		
		
		subdata = data[left_bound - 1: lastAnnotated]

		valence = []
		arousal = []
		
		for x in subdata:
			valence.append(x['Valence'])
			arousal.append(x['Arousal'])

		self._ax.plot(range(left_bound, lastAnnotated + 1), valence, color = 'orange', linewidth = 5)
		self._ax.plot(range(left_bound, lastAnnotated + 1), arousal, color = 'blue')
		self._ax.axvline(x = currAnnotation, color = 'red', linestyle = 'dashed')

		if left_bound == first_frame:
			left_bound -= 1

		self.__setup(left_bound, right_bound, Y_LOWER_BOUND - MARGIN, Y_UPPER_BOUND + MARGIN, self._nbrSeg.get())

		self._canvas.draw()
		



