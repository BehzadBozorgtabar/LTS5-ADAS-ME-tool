from tkinter import *
from interface.data import *

class AnnotatorFrame(LabelFrame):
	"""
	Represent the annotation frame, we will
	annotate the data into this window

	Attributes:
		- nbrRows: number of rows in this frame
		- nbrCols: number of clos in this frame

		- emotions: a dictionnary which maps emotions to a variables linked to the scales
		- valarRelations: a dictionnary which maps a valence/arousal configuration to a list of emotions
		- nbrScalePerLine: The maximun number of scales that can be displayed on a line
		
		- quarters: a dictionnary which maps a valence/arousal configuration to a canvas ID
		- canvas: the canvas which contains the graph
		- canLabels: a dictionnary which maps an emotion to a text ID

		-scales: a dictionnary which maps emotions to a scale
	"""

	def __init__(self, parent, **kwargs):

		LabelFrame.__init__(self, parent, **kwargs)
		self._nbrRows = 6
		self._nbrCols = 9

		
		# configuration of the grid task manager
		for x in range(0, self._nbrRows):
			self.rowconfigure(x, weight=1)

		for x in range(0, self._nbrCols):
			self.columnconfigure(x, weight=1)
		
		#Data
		self._emotions = {"Joy" : IntVar(), "Sadness" : IntVar(), "Anger" : IntVar(), "Disgust" : IntVar(), "Fear" : IntVar(), "Surprise" : IntVar(), "Neutral" : IntVar(), "Valence" : IntVar(), "Arousal" : IntVar(), "Severity" : IntVar()}

		self._valarRelations = { (-1,-1): ['Sadness'],\
					 (-1,0): ['Fear', 'Disgust', 'Sadness'],\
					 (-1,1): ['Fear', 'Anger', 'Surprise', 'Disgust'],\
					 (0,-1): ['Neutral'],\
					 (0,0): [],\
					 (0,1): ['Surprise'],\
					 (1,-1): [],\
					 (1,0): ['Joy'],\
					 (1,1): ['Joy', 'Surprise']}


		self._nbrScalePerLine = 4

		
		"""
		Construct the Valence/Arousal relation Graph
		"""
		self._quarters = {}

		self._canvas = Canvas(self)
		self._canvas.grid(row = 0, rowspan = self._nbrRows, column = self._nbrScalePerLine, columnspan = self._nbrCols - self._nbrScalePerLine + 1, sticky = 'W')
		
		canWidth, canHeight = (float(self._canvas['width']), float(self._canvas['height']))

		self._canLabels = 	{'Joy' : self._canvas.create_text(self.__canH(canWidth, 8.25), self.__canH(canHeight, 3.0), text = 'Joy'),\
					'Anger' : self._canvas.create_text(self.__canH(canWidth, 1.5), self.__canH(canHeight, 1.5), text = 'Anger'),\
				 	'Sadness' : self._canvas.create_text(self.__canH(canWidth, 0.65), self.__canH(canHeight, 5.0), text = 'Sadness'),\
				 	'Surprise' : self._canvas.create_text(self.__canH(canWidth, 4.5), self.__canH(canHeight, 0.5), text = 'Surpise'),\
					'Fear' : self._canvas.create_text(self.__canH(canWidth, 0.45), self.__canH(canHeight, 4.0), text = 'Fear'),\
					'Neutral' : self._canvas.create_text(self.__canH(canWidth, 4.5), self.__canH(canHeight, 8.5), text = 'Neutral'),\
					'Disgust' : self._canvas.create_text(self.__canH(canWidth, 0.7), self.__canH(canHeight, 2.5), text = 'Disgust')}

		#Upper Left
		self._quarters[(-1,1)] = self._canvas.create_arc(self.__canH(canWidth, 1.3), self.__canH(canHeight, 1.0),\
								self.__canH(canWidth, 7.0), self.__canH(canHeight, 7.0), start = 90, extent = 90)

		#Left
		self._quarters[(-1,0)] = self._canvas.create_rectangle(self.__canH(canWidth, 1.3), self.__canH(canHeight, 4.0),\
									self.__canH(canWidth, 4.0), self.__canH(canHeight, 5.0))

		#Loer Left
		self._quarters[(-1,-1)] = self._canvas.create_arc(self.__canH(canWidth, 1.3), self.__canH(canHeight, 2.0),\
								self.__canH(canWidth, 7.0), self.__canH(canHeight, 8.0), start = 180, extent = 90)



		#Upper
		self._quarters[(0,1)] = self._canvas.create_rectangle(self.__canH(canWidth, 4.0), self.__canH(canHeight, 1.0),\
									self.__canH(canWidth, 5.0), self.__canH(canHeight, 4.0))

		#Center
		self._quarters[(0,0)] = self._canvas.create_rectangle(self.__canH(canWidth, 4.0), self.__canH(canHeight, 4.0),\
									self.__canH(canWidth, 5.0), self.__canH(canHeight, 5.0))

		#Lower
		self._quarters[(0,-1)] = self._canvas.create_rectangle(self.__canH(canWidth, 4.0), self.__canH(canHeight, 5.0),\
									self.__canH(canWidth, 5.0), self.__canH(canHeight, 8.0))



		#Upper Right
		self._quarters[(1,1)] = self._canvas.create_arc(self.__canH(canWidth, 2.15), self.__canH(canHeight, 1.0),\
								self.__canH(canWidth, 7.85), self.__canH(canHeight, 7.0), start = 0, extent = 90)

		#Right
		self._quarters[(1,0)] = self._canvas.create_rectangle(self.__canH(canWidth, 5.0), self.__canH(canHeight, 4.0),\
									self.__canH(canWidth, 7.85), self.__canH(canHeight, 5.0))

		#Loer Right
		self._quarters[(1,-1)] = self._canvas.create_arc(self.__canH(canWidth, 2.15), self.__canH(canHeight, 2.0),\
								self.__canH(canWidth, 7.85), self.__canH(canHeight, 8.0), start = 270, extent = 90)


		"""
		Construct the scales to annotate data
		"""
		self._scales = {}

		#emotions
		i = 0 #counter
		for keys in self._emotions.keys():
			islowlim = i < self._nbrScalePerLine
			modlim = i % self._nbrScalePerLine
			s = Scale(self, orient = 'vertical', resolution = 1, tickinterval = 1, variable = self._emotions[keys])
			l = Label(self, bg = self['bg'], fg = 'black', text = keys)

			if keys == 'Valence':
				s.config(bg = activeColor, orient = 'horizontal', from_ = -1, to = 1, command = self.__updateScalesState)
				s.grid(row = self._nbrRows - 1, column = self._nbrScalePerLine, columnspan = self._nbrCols - self._nbrScalePerLine, sticky = 'WE')
				l.grid(row = self._nbrRows - 1, column = self._nbrScalePerLine)
			elif keys == 'Arousal':
				s.config(bg = activeColor, from_ = 1, to = -1, command = self.__updateScalesState)
				s.grid(column = self._nbrCols, row = 1, rowspan = self._nbrRows - 2, sticky = 'NS')
				l.grid(column = self._nbrCols, row = 0)
			elif keys == 'Severity':
				s.config(bg = activeColor, from_ = 4, to = 1)
				s.grid(column = self._nbrScalePerLine - 1, row = 3, rowspan = 2, sticky = 'NS')
				l.grid(column = self._nbrScalePerLine - 1, row = 5, sticky = 'NS')
			else:
				s.grid(row = 0 if islowlim else 3, rowspan = 2, column = modlim, sticky = 'NS')
				l.grid(row = 2 if islowlim else 5, column = modlim)
			
			i += 1
			self._scales[keys] = s

		reset = Button(self, text = 'reset', command = self.reset)
		reset.grid(row =0, column = self._nbrScalePerLine, sticky = 'EW', padx = pad, pady = pad)
		self.reset()

	#helper for creation of arcs to prevent duplication of code.
	def __canH(self, widthOrHeight, ratio, dim = 9):
		return widthOrHeight * ratio / dim
		

	#Updates the scales ' state
	def updateScales(self, data):
		for keys in valAr:
			default = -1 if keys == 'Arousal' else 0
			self._emotions[keys].set(data.get(keys, default))

		self.__updateScalesState()

		for keys in self._emotions.keys():
			if keys not in valArSev:
				self._emotions[keys].set(data.get(keys, 0))

		self._emotions['Severity'].set(data.get('Severity', 1))


	#Heper function for update function
	def __updateScalesState(self, newValue = 0):
		v, a = (self._emotions['Valence'].get(), self._emotions['Arousal'].get())

		for index, ID in self._quarters.items():
			if (v,a) == index:
				self._canvas.itemconfigure(ID, fill = activeColor)
			else:
				self._canvas.itemconfigure(ID, fill = inactiveColor)	

		
		for emotion in self._emotions.keys():
			if emotion not in valArSev:
				toSetNormal = self._valarRelations[(v,a)]

				if emotion in toSetNormal:
					self.__changeState(emotion, 'normal')
				else:
					self.__changeState(emotion, 'disabled')
			
			

	#Helper function for updateScalesState
	def __changeState(self, emotion, newState):
		self._scales[emotion]['state'] = newState
		self._scales[emotion]['bg'] = mapStateColor[newState]
		if newState == 'normal':
			self._scales[emotion].config(from_ = 2, to = 0)
		else:
			self._scales[emotion].config(from_ = 0, to = 0)
	
	#It returns all annotations done with respect to the scales' state
	def getAnnotations(self):
		result = dict()
		for emotions in self._emotions:
			result[emotions] = self._emotions[emotions].get()
		return result

	#Reset the scales' state
	def reset(self):
		for keys in self._emotions.keys():
			self._emotions[keys].set(0)
		self._emotions['Arousal'].set(-1)
		self._emotions['Severity'].set(1)
		self.__updateScalesState()
