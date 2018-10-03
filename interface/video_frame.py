from tkinter import *
from interface.data import *
from ReadSMBBinaryFile.extract_roi_data import SMB
import PIL.Image, PIL.ImageTk
import cv2
import csv

class VideoFrame(LabelFrame):
	"""
	Represent the frame which will show us the video frames 
	and permit us to handle the data

	This class has got these attributes:
		-data: the data to annotate
		-annotator: the frame which annotates the data
		-graph: the graph which shows us the annotations done
		-video: the video data
		-vidWidth: the width of the video window
		-vidHeight: the height of the video window
		-canvas: the video support
		-play: does the video is playing ?
		-end: does the task finish ?

		-frame: the index frame which is displaying
		-lastFrame: the index of the frame we've just displaying before
		-nbrFrames: the number of frame of the video
		-startFrame: The lower bound of the segmnent displayed
		-endDrame: the upper bound of the segment displayed
		-lastAnnotations: A list of all the frame for which we've saved an annotation

		-all the different widgets to handle the data
	"""

	def __init__(self, parent, file_to_annotate, annotator, graph, **kwargs):
		LabelFrame.__init__(self, parent, **kwargs)

		self._parent = parent
		self._file_to_annotate = file_to_annotate
		self._dataPath = toAnnotatePath + '/' + self._file_to_annotate

		# configuration of the grid task manager
		self._nbr_rows = 5
		self._nbr_cols = 6
		
		for x in range(0, self._nbr_rows):
			self.rowconfigure(x, weight=1)

		for x in range(0, self._nbr_cols):
			self.columnconfigure(x, weight=1)

		#stores the csv file data into an array
		self._smb = file_to_annotate.endswith('.smb')
		self._data = 0
	
		#annotator/Graph
		self._annotator = annotator
		self._graph = graph

		#opens the video file
		self._video = 0
		self._vidWidth = 0
		self._vidHeight = 0
		
		if self._smb:
			self._video = SMB(self._dataPath)
			self._vidWidth, self._vidHeight, self._data = self._video.ROIdata()
		else:
			self._data = self.readCSV()
			self._video = cv2.VideoCapture(self._dataPath[:-4] + ".avi")
			self._vidWidth = self._video.get(cv2.CAP_PROP_FRAME_WIDTH)
			self._vidHeight = self._video.get(cv2.CAP_PROP_FRAME_HEIGHT)

		#Setup
		self._play = False
		self._end = False
		self._frame = IntVar()
		self._lastFrame = first_frame
		self._nbrFrames = self._video.get(NBR_FRAMES)
		self._startFrame = first_frame
		self._frame.set(self._startFrame)
		self._endFrame = min(self._nbrFrames, self._startFrame + SEGMENT_SIZE - 1)
		self._video.set(FRAME_INDEX, self._startFrame)
		self._lastAnnotations = [first_frame - 1]

		#Create a canvas that can fit the above video source size
		self._canvas = Canvas(self, width = window_width, height = window_height)
		self._canvas.grid(row = 0, column = 0, columnspan = 6)
		self._canvas.grid_propagate(0)

		#Widgets to handle the data
		self._prevFrame = Button(self, text = 'Previous frame', state = 'disabled', command = self.prevFrame)
		self._prevFrame.grid(row = 1, column = 0, sticky = stick, padx = pad, pady = pad)

		self._scale = Scale(self, orient = 'horizontal', from_ = self._startFrame, to = self._endFrame, tickinterval = SEGMENT_SIZE - 1, variable = self._frame)
		self._scale.grid(row = 1, column = 1, columnspan = 4, sticky = 'ew', padx = pad, pady = pad)

		self._nextFrame = Button(self, text = 'Next frame', state = 'disabled', command = self.nextFrame)
		self._nextFrame.grid(row = 1, column = 5, sticky = stick, padx = pad, pady = pad)

		self._replay = Button(self, text = 'Play/Replay', fg = 'green', state = 'normal', command = self.replay)
		self._replay.grid(row = 2, column = 0, columnspan = 3, sticky = stick, padx = pad, pady = pad)

		self._info = Label(self, text = "Frame %d/%d" % (self._frame.get(), self._nbrFrames))
		self._info.grid(row = 2, column = 3, columnspan = 3, sticky = stick, padx = pad, pady = pad)

		self._prevSegment = Button(self, text = 'Previous segment (x20 frames)', state = 'disabled', command = self.prevSegment)
		self._prevSegment.grid(row = 3, column = 0, columnspan = 3, sticky = stick, padx = pad, pady = pad)

		self._nextSegment = Button(self, text = 'Next segment (x20 frames)', state = 'disabled', command = self.nextSegment)
		self._nextSegment.grid(row = 3, column = 3, columnspan = 3, sticky = stick, padx = pad, pady = pad)

		self._saveFrame = Button(self, state = 'disabled', command = self.saveFrame)
		self._saveFrame.grid(row = 4, column = 0, columnspan = 5, sticky = stick, padx = pad, pady = pad)

		self._resetSegment = Button(self, text = 'Reset Segment', state = 'disabled', command = self.resetSegment)
		self._resetSegment.grid(row = 4, column = 5, sticky = stick, padx = pad, pady = pad)

		self.update()

	#Read a CSV file
	def readCSV(self):
		data = []
		with open(self._dataPath, 'r') as csvFile:
			spamReader = csv.DictReader(csvFile, delimiter = '\t')

			for row in spamReader:
				data.append(row)
		return data

	#Goes to the next frame in the segment
	def nextFrame(self):
		self._frame.set(self._frame.get() + 1)

	#Goes to the previous frame in the segment
	def prevFrame(self):
		self._frame.set(self._frame.get() - 1)
		

	# Replays the segment video
	def replay(self):
		self._video.set(FRAME_INDEX,self._startFrame)
		self._play = True
		self._replay['state'] = 'disabled'

	# Go the next segment
	def nextSegment(self):
		self._nextSegment['state'] = 'disabled'
		self._resetSegment['state'] = 'disabled'
		self._startFrame = min(self._startFrame + SEGMENT_SIZE, self._nbrFrames)
		self._endFrame = min(self._endFrame + SEGMENT_SIZE, self._nbrFrames)
		self._scale['from_'] = self._startFrame
		self._scale['to'] = self._endFrame

	# Go to the previous segment
	def prevSegment(self):
		self._end = False
		self._nextSegment.config(text = 'Next segment (x20 frames)', fg = 'black', state = 'disabled', command = self.nextSegment)
		self._prevSegment['state'] = 'disabled'
		self._resetSegment['state'] = 'disabled'
		self._startFrame = max(self._startFrame - SEGMENT_SIZE, 1)
		self._endFrame = min(self._startFrame + SEGMENT_SIZE - 1, self._nbrFrames)
		self._scale.config(from_ = self._startFrame, to = self._endFrame)

	# Save an entire segment in the data array, permits to go to the next segment
	def saveSegment(self):
		if self._endFrame < self._nbrFrames:
			self._nextSegment['state'] = 'normal'
		else:
			self._end = True
			self._nextSegment.config(text = 'Save All and Exit', fg = 'green', state = 'normal', command = self.saveAll)
			self._info.config(text = 'You have finished, clic on Save All and Exit below', fg= 'green')

	# Resets all annotations done on the current segment to the initial state
	def resetSegment(self):
		self._frame.set(min(self._lastAnnotations[-1] + 1, self._endFrame))
		self._annotator.reset()

		first_index = self._lastAnnotations.index(self._startFrame - 1) + 1
		last_index = self._lastAnnotations.index(self._endFrame) if self._endFrame in self._lastAnnotations else len(self._lastAnnotations) - 1

		
		for n in range(first_index, last_index + 1):
			del self._lastAnnotations[first_index]
		self.saveFrame()
		self._frame.set(self._startFrame)
		

	# Save a group of frame in data array, from the last annotated frame to the actual frame
	def saveFrame(self):
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
			self.saveSegment()
			self._resetSegment['state'] = 'normal'
		else:
			self._nextSegment['state'] = 'disabled'
			self.nextFrame()

	# Save all data and exit the application
	def saveAll(self):
		data = self._data
		path = annotatedPath + '/' + self._file_to_annotate[:-4]
		
		with open(path + '_annotated.csv', 'w') as dataFile:
			fieldnames = data[first_frame - 1].keys()
			
			writer = csv.DictWriter(dataFile, fieldnames = fieldnames)
			
			writer.writeheader()
			for row in data:
				writer.writerow(row)

		self._parent.destroy()

	# loop method of the app, to display a video and have an interactive app
	def update(self):

		if not self._play:
			self._video.set(FRAME_INDEX, self._frame.get())
		# Get a frame from the video source
		self._frame.set(self._video.get(FRAME_INDEX))

		if not self._frame.get() == self._lastFrame:
			self._annotator.updateScales(self._data[self._frame.get() -1])
			self._lastFrame = self._frame.get()
		
		self.handle_widgets_states()


		ret, frame = self.get_frame() if not self._smb else self._video.read()

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
		self.after(delay, self.update)


	# Release the video source when the object is destroyed
	def __del__(self):
		if not self._smb and self._video.isOpened():
			self._video.release()


	# Get the next video frame
	def get_frame(self):
		if self._video.isOpened():
			ret, frame = self._video.read()
			if ret:
			# Return a boolean success flag and the current frame converted to BGR
				return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
			else:
				return (ret, None)
		else:
			return (ret, None)

	# shares the data
	def data(self):
		return (self._data, self._lastAnnotations)

	# Is it the end ?
	def end(self):
		return self._end
	
	#Permits to display only 20 frames
	def handle_widgets_states(self):
		nearestPrevAnnotated = self.nearestPrevAnnotated()
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

	#return the nearest previous annotated frame from the current frame
	def nearestPrevAnnotated(self):
		annotation_list = self._lastAnnotations.copy()
		annotation_list.append(self._frame.get())
		annotation_list.sort()
		return self._lastAnnotations[annotation_list.index(self._frame.get()) - 1] + 1
		
		
