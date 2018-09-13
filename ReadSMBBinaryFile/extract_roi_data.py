import struct

def readSMB(dataPath):
	data = []
	file = open(dataPath, "rb")

	SMB_HEADER_SIZE = 20
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

			current_position = current_position + (image_width * image_height) + SMB_HEADER_SIZE

			data.append({'CameraIndex' : camera_index, 'FrameNumber' : frame_number, 'timeStamp' : time_stamp, 'panX' : roi_left, 'panY' : roi_top, 'width' : roi_width, 'height' : roi_height, 'cameraAngle' : camera_angle})
			'''
			Jump to the next image
			'''
			file.seek(current_position)
	finally:
		file.close()

	return data
