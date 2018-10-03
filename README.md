![](screenshot/screenshot.png)

README to know how to use well this Emotion Recognition Annotation Tool


1. Load data:
	
	Put your data files in the data/to_annotate folder.

	Requirements:
			- the video files have to be .avi ones
			- the data files have to be .csv files or .smb ones
			- for a csv file, you must import the associated video file beside

2. Libraries requirements:

	You need to have the following python libraries installed:
		- matplotlib
		- tkinter
		- cv2
		- csv
		- struct
		- numpy

3. Start the application:
	
	On linux, type in the terminal in lts5-ada-me folder: python3 main.py
	A little window with a list of file will be displayed

4. Choose a file:

	Choose a .smb or a .cvs file to annotate the corresponding video and clic on validate.
	Your can exit this window at any moment

5. Annotate:
	
	First, annotate the valence and arousal with help of the graph that shows you the previous segments annotated.
	Then, you can annotate the corresponding emotions to have more precision
	Don't forget to annotate the severity
	The annotation done, save it and go to the next frame/segment

	You always have to save an entire segment before go to the next one
	
	In this version you can't quit the application and continue your current annotation later. You have to annotate all before Save All and Quit


6. Fetch annotated data:

	All annotated data is in the data/annotated folder.
	They are .csv files with the same name as file input followed by annotated
		
