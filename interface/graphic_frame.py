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
	- canvas: the tkinter frame which encapsulates the graph

	- data: the data to plot
	- ticksSegments: the ticks which seperate each segment
	- rightBound: the right bound for the x axis
	
	- listChoice: a list of the number of segments we wish to plot
	- nbrSeg: the number of segment we wish to plot chosen from the list above
"""
class GraphFrame(LabelFrame):
	

	def __init__(self, parent, **kwargs):
		LabelFrame.__init__(self, parent, **kwargs)

		#Creation of the graph
		self._figure = Figure(figsize = (0.1,0.1), dpi = 60)
		self._ax = self._figure.add_subplot(111)

		self._canvas = FigureCanvasTkAgg(self._figure, self)
		self._canvas.get_tk_widget().pack(side = TOP, fill = BOTH, expand = True)

		valenceLabel = Label(self, text = "______ Valence", bg = 'white', fg = 'orange')
		arousalLabel = Label(self, text = "______ Arousal", bg = 'white', fg = 'blue')
		lastAnnotatedLabel = Label(self, text = "______ Segments bounds", bg = 'white', fg = 'red')

		valenceLabel.place(relx = 0.2, rely = 0.05)
		arousalLabel.place(relx = 0.4, rely = 0.05)
		lastAnnotatedLabel.place(relx = 0.6, rely = 0.05)

		#Memory
		self._data = []
		self._ticksSegments = [first_frame]
		self._rightBound = first_frame

		#Creation of RadioButtons to choose how many segments to show
		self._listChoice = [1,2,5,10]
		self._nbrSeg = IntVar()
		self._nbrSeg.set(1)

		for x in range(0, len(self._listChoice)):
			rb = Radiobutton(self, bg = 'white', text = str(self._listChoice[x]), variable = self._nbrSeg, value = self._listChoice[x], command = lambda : self.plotGraph(self._data, self._rightBound, self._ticksSegments))
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
		minor_tick = max(int(tickInterval / 10), 1)
		self._ax.set_xlabel(xLabel)
		self._ax.set_xbound(xLower,xUpper)
		self._ax.xaxis.set_minor_locator(tick.MultipleLocator(minor_tick))
		self._ax.xaxis.set_major_locator(tick.MultipleLocator(tickInterval))
		
		self._ax.set_ylabel(yLabel)
		self._ax.set_ybound(yLower, yUpper)
		self._ax.yaxis.set_major_locator(tick.MultipleLocator(minor_tick))

		self._ax.grid(which = 'minor', linestyle = '--', alpha = 0.2)
		self._ax.grid(which = 'major')

	"""
	Plots the graph after an annotation saved
	Arguments:
		- data: all annotations done before
		- endFrame: last frame annotated
		- ticksSegments: the ticks which seperate each annotated segment
	"""
	def plotGraph(self, data, endFrame, ticksSegments):
		self._data = data
		self._ticksSegments = ticksSegments
		self._ax.cla()
		self._rightBound = endFrame

		if endFrame in ticksSegments:
			index = ticksSegments.index(endFrame) 
		else:
			ticks = ticksSegments.copy()
			ticks.append(endFrame)
			ticks.sort()
			index = ticks.index(endFrame) - 1

		startFrame = int(ticksSegments[max(0, index - self._nbrSeg.get())])		

		subdata = data[startFrame - 1: endFrame]

		valence = []
		arousal = []
		
		for x in subdata:
			valence.append(x['Valence'])
			arousal.append(x['Arousal'])

		self._ax.plot(range(startFrame, endFrame + 1), valence, color = 'orange', linewidth = 5)
		self._ax.plot(range(startFrame, endFrame + 1), arousal, color = 'blue')

		for x in ticksSegments:
			self._ax.axvline(x = x, color = 'red', linestyle = 'dashed', linewidth = 4)

		if startFrame == first_frame:
			startFrame -= 1

		self.__setup(startFrame, endFrame, Y_LOWER_BOUND - MARGIN, Y_UPPER_BOUND + MARGIN, max(int((endFrame - startFrame) / 20), 1))

		self._canvas.draw()
		



