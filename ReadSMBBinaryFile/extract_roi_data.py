import struct
import numpy as np
import os
import sys

from math import ceil
from interface.data import *

"""
Class to read SMB files
Attributes:
	- index: The current frame index we're reading
	- nbrFrames: number of images stored in the file
	- dataPath: the location of the smb file
	- width: the width of the images
	- height: the height of the images

	- part: the part of the whole file the user has chosen to annotate
	- partIndex: the index of the segment we're annotating
"""
class SMB:

	"""
	Constructor of the class
	Setups the smb file parameters (dimension of the images, nbr of frames)
	Argument:
		- dataPath: the location of the smb file
	"""
	def __init__(self, dataPath):
		self._index = 0
		self._nbrFrames = 0
		self._dataPath = dataPath
		self._width, self._height = 0,0

		with open(self._dataPath, 'rb') as file:
			'''
			Read SMB header:
			Jump to the position where the width and height of the image is stored in SMB header
			'''
			file.seek(12)
			image_width = bytearray(file.read(4))
			image_width.reverse()
			image_width = int.from_bytes(image_width, byteorder='big')

			image_height = bytearray(file.read(4))
			image_height.reverse()
			image_height = int.from_bytes(image_height, byteorder='big')

			self._width, self._height = image_width, image_height

			nbrFrames = ceil(os.stat(dataPath).st_size / (SMB_HEADER_SIZE + self._width*self._height))
			nbrParts = ceil(nbrFrames / 1000)
			arrayParts = np.arange(1, nbrParts + 1)
			self._part = 0

			if nbrParts > 1:
				while not self._part in arrayParts:
					print("The file is big. The annotation task is split in %d parts. So you'll have to annotate each part of the file separately." % (nbrParts))
					print("Please choose which part of the file you want to annotate now {} : ".format(arrayParts))
					self._part = int(input(""))

			self._partIndex = max(self._part - 1, 0)
			self._index = self._partIndex*MAX_SEGMENT_SIZE
			self._nbrFrames = min(MAX_SEGMENT_SIZE, nbrFrames - self._partIndex*MAX_SEGMENT_SIZE)

	"""
	Returns the part of the whole file the user has chosen to annotate
	"""
	def part(self):
		return self._part

	"""
	Returns the ROI data of the whole segment we're annotating
	"""
	def readROI(self):
		ROIData = []
		
		with open(self._dataPath, 'rb') as file:
			current_position = self._index * (self._width*self._height + SMB_HEADER_SIZE)
			file.seek(current_position)

			for i in range(1, self._nbrFrames + 1):
				sys.stdout.write("\rCharging video: %.1f%%" % (i*100 / self._nbrFrames))
				sys.stdout.flush()

				'''
				Read SMB header
				'''
				smb_header = file.read(SMB_HEADER_SIZE)
				if not smb_header:
					break

				'''
				Read ROI data
				'''
				camera_index = bytearray(file.read(4))
				camera_index.reverse()
				camera_index = int.from_bytes(camera_index, byteorder='big')

				frame_number = bytearray(file.read(8))
				frame_number.reverse()
				frame_number = int.from_bytes(frame_number, byteorder='big')

				time_stamp = bytearray(file.read(8))
				time_stamp.reverse()
				time_stamp = int.from_bytes(time_stamp, byteorder='big')

				roi_left = bytearray(file.read(4))
				roi_left.reverse()
				roi_left = int.from_bytes(roi_left, byteorder='big')

				roi_top = bytearray(file.read(4))
				roi_top.reverse()
				roi_top = int.from_bytes(roi_top, byteorder='big')

				roi_width = bytearray(file.read(4))
				roi_width.reverse()
				roi_width = int.from_bytes(roi_width, byteorder='big')

				roi_height = bytearray(file.read(4))
				roi_height.reverse()
				roi_height = int.from_bytes(roi_height, byteorder='big')

				camera_angle = bytearray(file.read(8))
				camera_angle = struct.unpack('d', camera_angle)[0]

				ROIData.append({'CameraIndex' : camera_index, 'FrameNumber' : frame_number, 'timeStamp' : time_stamp, 'panX' : roi_left, 'panY' : roi_top, 'width' : roi_width, 'height' : roi_height, 'cameraAngle' : camera_angle})


				current_position = current_position + (self._width*self._height) + SMB_HEADER_SIZE

				'''
				Jump to the next image
				'''
				file.seek(current_position)
		
			return ROIData


	"""
	Reads the file at the current image index
	Returns the image to read and if it has been read correctly
	"""
	def read(self):
		image = []

		with open(self._dataPath, 'rb') as file:
			current_position = self._index * (self._width*self._height + SMB_HEADER_SIZE)
			file.seek(current_position)

			'''
			Read SMB header
			'''
			smb_header = file.read(SMB_HEADER_SIZE)
			if not smb_header:
				return (False, image)

			'''
			Read image
			'''
			file.seek(current_position + SMB_HEADER_SIZE)

			image = bytearray(file.read(self._width * self._height))
			image = np.array(image)
			if image.size == self._width * self._height:
				image = np.reshape(image, (self._height, self._width))
				return (True, image)
			else:
				image = np.array([])
				return (False, image)

				

	"""
	Returns the nbr of frames or the current index with respect to the index given as argument following the cv2 rules
	"""
	def get(self, index):
		if index == FRAME_INDEX:
			return self._index
		elif index == NBR_FRAMES:
			return self._nbrFrames

	"""
	Set the current index to newFrame
	Arguments:
		- index: index with respect to the cv2 rules
		- newFrame: the new index
	"""
	def set(self, index, newFrame):
		if index == FRAME_INDEX:
			self._index = (newFrame - 1) + self._partIndex*MAX_SEGMENT_SIZE

	"""
	Returns the ROIdata with width and height of the images
	"""
	def imageParams(self):
		return self._width, self._height
		
