#Hight level API imports
from tkinter import *
import PIL.Image, PIL.ImageTk
import cv2
import csv

#Imports from the project's folders
from interface.data import *


"""
Represent the frame which will show us the video frames 
and permit us to handle the data

Attributes:
	- parent: the parent widget of the video frame
	- dataPath: the path we need to fetch the data
	- savePath: The path where we save the annotation
	- part: The part of the whole video we're annotating
	- onePart: Does the video contain only one part ?
	- annotator: the frame which annotates the data
	- graph: the graph which shows us the annotations done

	- data: the data to annotate
	- video: the video data
	- vidWidth: the width of the video window
	- vidHeight: the height of the video window

	- play: is the video playing ?
	- end: does the task finish ?
	- frame: the index frame which is displaying
	- lastFrame: the index of the frame we've just displaying before
	- nbrFrames: the number of frame of the video
	- startFrame: The lower bound of the segmnent displayed
	- endDrame: the upper bound of the segment displayed
	- lastAnnotations: A list of all the frame for which we've saved an annotation

	- canvas: the support of the video data
	- prevFrame: a button to go to the previous frame
	- scale: a scale to choose which frame to display within the current segment
	- nextFrame: a button to go to the next frame
	- replay: a button to plays the video during a segment of 5 frames
	- info: a label to inform the user his current position in the video
	- prevSegment: a button to go to the previous segment
	- nextSegment: a button to go to the next segment
	- saveFrame: a button to save the annotations done from startFrame to lastAnnotation
	- resetSegment: a buton to reset the annotations to the default ones in the segment
"""
class VideoFrame(LabelFrame):
	
	"""
	Constructor of the class.
	It constructs the architecture of the frame and loads the data
	Arguments:
		- parent: the parent widget
		- dataPath: The path we need to fetch the data
		- savePath: The path where we save the annotation
		- annotator: the annotator frame binded to this frame
		- graph: the graph frame binded to this frame
		- video: the video which will be displayed on this panel
		- videoWidth: the width of the frames
		- videoHeight: the height of the frames
		- part: the part of the whole files we're annotating
		- nbrFrames: the number of frames in this part
	"""
	def __init__(self, parent, dataPath, savePath, annotator, graph, video, videoWidth, videoHeight, part, nbrFrames, **kwargs):
		LabelFrame.__init__(self, parent, **kwargs)

		self._parent = parent
		self._dataPath = dataPath
		self._savePath = savePath
		self._part = part
		self._onePart = part == 0

		#annotator/Graph
		self._annotator = annotator
		self._graph = graph

		# configuration of the grid task manager
		nbr_rows = 5
		nbr_cols = 6
		
		for x in range(0, nbr_rows):
			self.rowconfigure(x, weight=1)

		for x in range(0, nbr_cols):
			self.columnconfigure(x, weight=1)

		#opens the video file
		self._video = video
		self._vidWidth = videoWidth
		self._vidHeight = videoHeight
		
		#stores the metadata
		self._data = self._video.readROI()

		#Setup
		self._play = False
		self._end = False
		self._frame = IntVar()
		self._lastFrame = first_frame
		self._nbrFrames = nbrFrames
		self._startFrame = first_frame
		self._endFrame = min(self._nbrFrames, self._startFrame + SEGMENT_SIZE - 1)
		self._lastAnnotations = [first_frame - 1]
		
		self._frame.set(self._startFrame)
		self._video.set(FRAME_INDEX, self._startFrame)

		#Create a canvas that can fit the above video source size
		self._canvas = Canvas(self, width = window_width, height = window_height)
		self._canvas.grid(row = 0, column = 0, columnspan = 6)
		self._canvas.grid_propagate(0)

		#Widgets to handle the data
		self._prevFrame = Button(self, text = 'Previous frame', state = 'disabled', command = self.__prevFrame)
		self._prevFrame.grid(row = 1, column = 0, sticky = stick, padx = pad, pady = pad)

		self._scale = Scale(self, orient = 'horizontal', from_ = self._startFrame, to = self._endFrame, tickinterval = SEGMENT_SIZE - 1, variable = self._frame)
		self._scale.grid(row = 1, column = 1, columnspan = 4, sticky = 'ew', padx = pad, pady = pad)

		self._nextFrame = Button(self, text = 'Next frame', state = 'disabled', command = self.__nextFrame)
		self._nextFrame.grid(row = 1, column = 5, sticky = stick, padx = pad, pady = pad)

		self._replay = Button(self, text = 'Play/Replay', fg = 'green', state = 'normal', command = self.__replay)
		self._replay.grid(row = 2, column = 0, columnspan = 3, sticky = stick, padx = pad, pady = pad)

		self._info = Label(self, text = "Frame %d/%d" % (self._frame.get(), self._nbrFrames))
		self._info.grid(row = 2, column = 3, columnspan = 3, sticky = stick, padx = pad, pady = pad)

		self._prevSegment = Button(self, text = 'Previous segment (x5 frames)', state = 'disabled', command = self.__prevSegment)
		self._prevSegment.grid(row = 3, column = 0, columnspan = 3, sticky = stick, padx = pad, pady = pad)

		self._nextSegment = Button(self, text = 'Next segment (x5 frames)', state = 'disabled', command = self.__nextSegment)
		self._nextSegment.grid(row = 3, column = 3, columnspan = 3, sticky = stick, padx = pad, pady = pad)

		self._saveFrame = Button(self, state = 'disabled', command = self.__saveFrame)
		self._saveFrame.grid(row = 4, column = 0, columnspan = 5, sticky = stick, padx = pad, pady = pad)

		self._resetSegment = Button(self, text = 'Reset Segment', state = 'disabled', command = self.__resetSegment)
		self._resetSegment.grid(row = 4, column = 5, sticky = stick, padx = pad, pady = pad)

		#self.__setData()
		self.__update()


	"""
	Writes a csv file
	Argument:
		- The path where we want to save the file
	"""
	def __writeCSV(self, path):
		path = path[:-4] + '_annotated'
		path = path + str(self._part) if not self._onePart else path 
		with open(path + '.csv', 'w') as dataFile:
			fieldnames = self._data[first_frame - 1].keys()
			
			writer = csv.DictWriter(dataFile, fieldnames = fieldnames)
			
			writer.writeheader()
			for row in self._data:
				writer.writerow(row)

	"""
	Goes to the next frame
	"""
	def __nextFrame(self):
		self._frame.set(self._frame.get() + 1)

	
	"""
	Goes to the previous frame
	"""
	def __prevFrame(self):
		self._frame.set(self._frame.get() - 1)
		

	"""
	Plays the video for the current segment
	"""
	def __replay(self):
		self._frame.set(self._startFrame)
		self._play = True
		self._replay['state'] = 'disabled'

	
	"""
	Goes to the next segment
	"""
	def __nextSegment(self):
		self._nextSegment['state'] = 'disabled'
		self._resetSegment['state'] = 'disabled'
		self._startFrame = min(self._startFrame + SEGMENT_SIZE, self._nbrFrames)

		self._endFrame = min(self._endFrame + SEGMENT_SIZE, self._nbrFrames)
		self._scale['from_'] = self._startFrame
		self._scale['to'] = self._endFrame
	
	"""
	Goes to the previous segment
	"""
	def __prevSegment(self):
		self._end = False
		self._nextSegment.config(text = 'Next segment (x5 frames)', fg = 'black', state = 'disabled', command = self.__nextSegment)
		self._prevSegment['state'] = 'disabled'
		self._resetSegment['state'] = 'disabled'
		self._startFrame = max(self._startFrame - SEGMENT_SIZE, 1)
		self._endFrame = min(self._startFrame + SEGMENT_SIZE - 1, self._nbrFrames)
		self._scale.config(from_ = self._startFrame, to = self._endFrame)


	"""
	Save an entire segment in the data array, permits to go to the next segment
	"""
	def __saveSegment(self):
		if self._endFrame < self._nbrFrames:
			self._nextSegment['state'] = 'normal'
		else:
			self._end = True
			self._nextSegment.config(text = 'Save All and Exit', fg = 'green', state = 'normal', command = self.__saveAll)
			self._info.config(text = 'You have finished, clic on Save All and Exit below', fg= 'green')


	"""
	Resets all annotations done on the current segment to the initial state
	"""
	def __resetSegment(self):
		self._frame.set(min(self._lastAnnotations[-1] + 1, self._endFrame))
		self._annotator.setDefaults()

		first_index = self._lastAnnotations.index(self._startFrame - 1) + 1
		last_index = self._lastAnnotations.index(self._endFrame) if self._endFrame in self._lastAnnotations else len(self._lastAnnotations) - 1

		
		for n in range(first_index, last_index + 1):
			del self._lastAnnotations[first_index]
		self.__saveFrame()
		self._frame.set(self._startFrame)
		

	"""
	Save a group of frame in data array, from the last annotated frame to the actual frame
	"""
	def __saveFrame(self):
		frame = self._frame.get()
		index = 0
		prevAnnotated = self._lastAnnotations[-1]
		
		if frame not in self._lastAnnotations:
			self._lastAnnotations.append(frame)
			self._lastAnnotations.sort()
		
		if frame <= prevAnnotated:
			index = self._lastAnnotations.index(frame)-1
			prevAnnotated = self._lastAnnotations[index]

		
		for x in range(prevAnnotated, frame):
			for keys, value in self._annotator.getAnnotations().items(): 
				self._data[x][keys] = value

		self._graph.plotGraph(self._data, self._lastAnnotations[0], self._lastAnnotations[-1], frame)

		if frame >= self._endFrame:
			self.__saveSegment()
			self._resetSegment['state'] = 'normal'
		else:
			self._nextSegment['state'] = 'disabled'
			self.__nextFrame()

	"""
	Save all data and exit the application
	"""
	def __saveAll(self):
		default = defaultSavePath + self._savePath.split('/')[-1]
		if self._savePath == default:
			self.__writeCSV(self._savePath)
		else:
			self.__writeCSV(default)
			self.__writeCSV(self._savePath)
			
		self._parent.destroy()

	"""
	loop method of the app, to display a video and have an interactive app
	"""
	def __update(self):
		self._video.set(FRAME_INDEX, self._frame.get())
		setup = self._frame.get() if not self._play else self._frame.get() + 1
		self._frame.set(setup)

		if not self._frame.get() == self._lastFrame:
			self._annotator.updateScales(self._data[self._frame.get() -1])
			self._lastFrame = self._frame.get()
		
		self.__handle_widgets_states()


		ret, frame = self._video.read()

		if ret:
			photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame).resize((window_width, window_height), PIL.Image.ANTIALIAS))
			self._canvas.create_image(0, 0, image = photo, anchor = NW)
			self._canvas.photo = photo

		currData = self._data[self._frame.get() - 1]
		scale_w = window_width / self._vidWidth
		scale_h = window_height / self._vidHeight
		panx, pany, width, height = float(currData['panX']) * scale_w, float(currData['panY']) * scale_h, float(currData['width']) * scale_w, float(currData['height']) * scale_h
		canvas_id = self._canvas.create_line(panx, pany, panx + width, pany, panx + width, pany + height, panx, pany + height, panx, pany, fill = 'red')


		self._canvas.after(delay, self._canvas.delete, canvas_id)
		self.after(delay, self.__update)

	"""
	Control center of all buttons' state
	"""
	def __handle_widgets_states(self):
		nearestPrevAnnotated = self.__nearestPrevAnnotated()
		self._saveFrame['text'] = "Save this annotation from frame %d to %d" % (nearestPrevAnnotated, self._frame.get()) if not nearestPrevAnnotated == self._frame.get() else "Save this annotation for the frame %d" % (self._frame.get()) 

		#We reach the end of the segment
		if self._frame.get() >= self._endFrame:
			self._play = False
			self._replay['state'] = 'normal'
			self._nextFrame['state'] = 'disabled'
		else:			
			self._saveFrame['text'] += " and Next"

			if not self._play:
				self._nextFrame['state'] = 'normal'

			else:
				self._nextFrame['state'] = 'disabled'

		#We are not playing the video (frame by frame)
		if not self._play:
			self._saveFrame['state'] = 'normal'
			self._prevSegment['state'] = 'normal'
			self._prevFrame['state'] = 'normal'
		#We are playing the video
		else:
			self._saveFrame['state'] = 'disabled'
			self._prevSegment['state'] = 'disabled'
			self._prevFrame['state'] = 'disabled'

		#It's the the first frame of the segment
		if self._frame.get() <= self._startFrame:
			self._prevFrame['state'] = 'disabled'

		#It's the first segment
		if self._startFrame <= 1:
			self._prevSegment['state'] = 'disabled'

		#It's not the last frame
		if not self._end or self._frame.get() < self._nbrFrames:
			self._info.config(text = "Frame %d/%d" % (self._frame.get(), self._nbrFrames), fg = 'black')

	"""
	Helpers method
	return the nearest previous annotated frame from the current frame
	"""
	def __nearestPrevAnnotated(self):
		annotation_list = self._lastAnnotations.copy()
		annotation_list.append(self._frame.get())
		annotation_list.sort()
		return self._lastAnnotations[annotation_list.index(self._frame.get()) - 1] + 1
		
		
