# constant for all
stick = "nesw"
pad = 5
defaultSavePath = "data/files/"
MAX_SEGMENT_SIZE = 1000
SMB_HEADER_SIZE = 20

#constants for video
first_frame = 1
first_index = first_frame - 1
FRAME_INDEX = 1
NBR_FRAMES = 7
MIN_SEGMENT_SIZE = 20
window_width = 640
window_height = 480
SEGMENT_SIZE = 5
delay = 15

#constant for graph
xLabel = "Frame Number"
yLabel = "Value"
MARGIN = 0.2
Y_UPPER_BOUND = 1
Y_LOWER_BOUND = -1
DEFAULT_TICK = 1.0

#Constants for annotation frame
inactiveColor = 'grey'
activeColor = 'green'
mapStateColor = {'normal' : activeColor, 'disabled' : inactiveColor}
Valence = 0
Arousal = 1
CanvasID = 2
valAr = ['Valence', 'Arousal']
valArSev = ['Valence', 'Arousal', 'Severity']
