import cv2, numpy as np
import imutils

RED = 0
RED1 = 1
YELLOW = 2
GREEN = 3
AQUA = 4 #light blue
BLUE = 5 #dark blue
PURPLE = 6
BLACK = 7


"""

[
(RED, GREEN),	#Example block
(BLUE, YELLOW)  #Example block 2
]

"""
colors = [RED, RED1, YELLOW, GREEN, AQUA, BLUE, PURPLE]
color_names = ["RED", "RED", "YELLOW", "GREEN", "AQUA", "BLUE", "PURPLE"]

"""COLOR RANGES (HSV):"""

#TODO: lower red 1 include too much black
value = 100
lower_red1 = np.array([0,0,value])
upper_red1 = np.array([15,255,255])

lower_red2 = np.array([166,0,value])
upper_red2 = np.array([180,255,255])

lower_yellow = np.array([16,0,value])
upper_yellow = np.array([45,255,255])

lower_green = np.array([46,0,value])
upper_green = np.array([75,255,255])

lower_aqua = np.array([76,0,value])
upper_aqua = np.array([105,255,255])

lower_blue = np.array([106,0,value])
upper_blue = np.array([135,255,255])

lower_purple = np.array([136,0,value])
upper_purple = np.array([165,255,255])


color_ranges = [
	(lower_red1, upper_red1),	#INDEX 0 = RED
	(lower_red2, upper_red2), 	#INDEX 1 = RED (two different ranges for red)
	(lower_yellow, upper_yellow), #INDEX 2 = YELLOW
	(lower_green, upper_green),	#INDEX 3 = GREEN
	(lower_aqua, upper_aqua),	#INDEX 4 = AQUA
	(lower_blue, upper_blue),	#INDEX 5 = BLUE
	(lower_purple, upper_purple),#INDEX 6 = PURPLE
]

def removeExtraContours(contours):
	contours = sorted(contours, key = cv2.contourArea, reverse=True) #sort contours by greatest to least area
	max_area = cv2.contourArea(max(contours, key = cv2.contourArea))

	num_valid_contours = 0
	for contour in contours:	#for each contour (each suspected block)
	#if the are contained by the contour is of reasonable size (not an erroneous detection)
		area = cv2.contourArea(contour)
		
		if (area > max_area * 0.1):	#accept anything larger than 10% of the max block size (TODO: THIS MIGHT CAUSE ISSUES)
			num_valid_contours += 1

	return contours[0:num_valid_contours]

def printColorList(colorList):
	for color in colorList:
		print (color_names[color])

def getContoursFromImage(filename):

	img = cv2.imread(filename)	#open image
	img_color = imutils.resize(img, width=600)	#resize image
	img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY) #convert image to grayscale

	#locate any black in the image - make anything below the threshold white, and anything above black (black should turn white)
	thresh_val = 90
	#ret, thresh = cv2.threshold(img_gray, thresh_val, 255, cv2.THRESH_BINARY_INV) 
	blocksize = 101
	constant = 40
	thresh = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blocksize, constant) 

	#Find the black outline around each block
	image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	#Destroy any contours that are below a certain threshold (to get rid of false outlines)
	contours = removeExtraContours(contours)

	#check if biggest contour is just the entire image (if so, delete that extra contour)
	x,y,width,height=cv2.boundingRect(contours[0])
	if(width == img_color.shape[1]):
		contours = contours[1:]
	
	return (img_color, contours)

def getBlockListFromImage(filename):
	img_color, contours = getContoursFromImage(filename)
	
	block_list = [] #list containing lists of colors in each block
	for block_contour in contours:
		x, y, width, height = cv2.boundingRect(block_contour) #Find the closest rectangle over this block
		block_region = img_color[y:(y+height), x:(x+width)]; #crop the image to the rectangle of the block
		
		color_areas = [0] * len(colors) #initialize a list of 0s representing the area of each color
		
		block_region_hsv = cv2.cvtColor(block_region, cv2.COLOR_BGR2HSV)
		
		for color in colors: #for each color
			mask = cv2.inRange(block_region_hsv, color_ranges[color][0], color_ranges[color][1]) #mask out everything other than that color
			color_region = cv2.bitwise_and(block_region, block_region, mask=mask)
			color_region = cv2.cvtColor(color_region, cv2.COLOR_BGR2GRAY)
			ret, color_region = cv2.threshold(color_region, 10, 255, cv2.THRESH_BINARY)
			
			i, color_contours, h = cv2.findContours(color_region, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #find the contour around that color
			
			#determine the area of that color
			if len(color_contours) == 0:
				color_areas[color] = 0
			else:
				color_contour_max_area = max(color_contours, key = cv2.contourArea)
				color_areas[color] = cv2.contourArea(color_contour_max_area)
		

		colors_in_region = []
		
		total_region_area = width*height
		for color in colors:
			color_percentage = round(color_areas[color] / total_region_area * 100, 2)
			
			if color_percentage > 15:
				colors_in_region.append(color)

		block_list.append(colors_in_region) #TODO: Ordering might not be right here. (Include coordinate information?)
	return block_list

blockList = getBlockListFromImage("paper_blocks2.jpg")
for block in blockList:
	printColorList(block)
	print "\n"
print blockList
	