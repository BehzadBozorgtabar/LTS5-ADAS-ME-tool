import struct
import numpy as np
from interface.data import *

import urllib
from smb.SMBHandler import SMBHandler

SMB_HEADER_SIZE = 20

"""
Class to read SMB files
Attributes:
	- index: current image index
	- nbrFrames: number of images stored in the file
	- dataPath: the location of the smb file
	- ROIdata: the roi data
	- width: the width of the images
	- height: the height of the images
"""
class SMB:

	"""
	Constructor of the class
	Initializes the ROi data, reading all headers
	Argument:
		- dataPath: the location of the smb file
	"""
	def __init__(self, dataPath):
		self._index = 0
		self._nbrFrames = 0
		self._dataPath = dataPath
		self._ROIdata = np.array([])
		self._width, self._height = 0,0

		file = open(self._dataPath, 'rb')

		try:
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

			current_position = 0
			file.seek(current_position)

			while True:
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

				self._nbrFrames += 1
				current_position = current_position + (image_width * image_height) + SMB_HEADER_SIZE


				self._ROIdata = np.append(self._ROIdata, {'CameraIndex' : camera_index, 'FrameNumber' : frame_number, 'timeStamp' : time_stamp, 'panX' : roi_left, 'panY' : roi_top, 'width' : roi_width, 'height' : roi_height, 'cameraAngle' : camera_angle})
				'''
				Jump to the next image
				'''
				file.seek(current_position)
		finally:
			file.close()


	"""
	Reads the file at the current image index
	Returns the image read and if it has been read correctly
	"""
	def read(self):
		image = np.array([])
		with open(self._dataPath, 'rb') as file:
			file.seek((self._index - 1) * (self._width*self._height + SMB_HEADER_SIZE) + SMB_HEADER_SIZE)
			image = bytearray(file.read(self._width * self._height))
			image = np.array(image)
			self._index += 1
			if image.size == self._width * self._height:
				image = np.reshape(image, (self._height, self._width))
				return (True, image)
			else:
				return (False, np.array([])) 
		return (False, np.array([]))

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
			self._index = newFrame

	"""
	Returns the ROIdata with width and height of the images
	"""
	def ROIdata(self):
		return self._width, self._height, self._ROIdata
		
