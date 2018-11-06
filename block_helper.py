import cv2, numpy as np
import imutils

RED = 0
YELLOW = 1
GREEN = 2
AQUA = 3 #light blue
BLUE = 4 #dark blue
PURPLE = 5
BLACK = 6


"""

[
(RED, GREEN),	#Example block
(BLUE, YELLOW)  #Example block 2
]

"""
colors = [RED, YELLOW, GREEN, AQUA, BLUE, PURPLE]
color_names = ["RED", "YELLOW", "GREEN", "AQUA", "BLUE", "PURPLE"]

"""COLOR RANGES (HSV):"""

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
	(lower_yellow, upper_yellow), #INDEX 2 = YELLOW
	(lower_green, upper_green),	#INDEX 3 = GREEN
	(lower_aqua, upper_aqua),	#INDEX 4 = AQUA
	(lower_blue, upper_blue),	#INDEX 5 = BLUE
	(lower_purple, upper_purple),#INDEX 6 = PURPLE
]

def isNestedContour(outerContour, potentialInnerContour):
	outer_x, outer_y, outer_width, outer_height = cv2.boundingRect(outerContour)
	inner_x, inner_y, inner_width, inner_height = cv2.boundingRect(potentialInnerContour)


	return outer_x < inner_x and outer_y < inner_y and (outer_x + outer_width > inner_x + inner_width) and (outer_y + outer_height > inner_y + inner_height)
	

def filterSmallContours(sorted_contours, thresholdArea):
	max_area = cv2.contourArea(max(sorted_contours, key = cv2.contourArea))
	num_valid_contours = 0
	
	for contour in sorted_contours:	#for each contour (each suspected block)
		area = cv2.contourArea(contour)
		#if the are contained by the contour is of reasonable size (not an erroneous detection)
		if area > thresholdArea:
			num_valid_contours += 1
	return sorted_contours[0:num_valid_contours]

	
def removeNestedContours(contours):
#Precondition: contours is sorted from greatest contour area to least

	#For each contour
		#for each other contour
			#if the other contour is contained by the original contour
				#delete that contour
				#decrement counter
				#0 1 2 3
	outerIndex = 0
	while outerIndex < len(contours):
		outerContour = contours[outerIndex]
		potentialInnerIndex = outerIndex + 1
		while potentialInnerIndex < len(contours):
			if isNestedContour(outerContour, contours[potentialInnerIndex]):
				contours = contours[0:potentialInnerIndex] + contours[potentialInnerIndex + 1 :]
				potentialInnerIndex -= 1 #correct for the shift of deletion to look at the next item
			potentialInnerIndex += 1
		outerIndex += 1
		

	return contours

	
def removeExtraContours(contours, img):
	contours = sorted(contours, key = cv2.contourArea, reverse=True) #sort contours by greatest to least area
	max_contour_area = cv2.contourArea(contours[0])
	contours = filterSmallContours(contours, max_contour_area * 0.1) #accept anything larger than 10% of the max block size (TODO: THIS MIGHT CAUSE ISSUES)(?)
	
	#check if biggest contour is just the border of the image
	x,y,width,height = cv2.boundingRect(contours[0])
	if(width == img.shape[1]): #If the contour width equals the image width
		contours = contours[1:]	#Delete that largest contour
	
	#Remove extra contours caused by the border of each block
	contours = removeNestedContours(contours)
	
	return contours

def printColorList(colorList):
	for color in colorList:
		print (color_names[color])

def printColorSet(colorSet):
	for color in colorSet:
		print color_names[color]

def getContoursFromImage(img):

	img_color = imutils.resize(img, width=600)	#resize image
	img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY) #convert image to grayscale

	#locate any black in the image - make anything below the threshold white, and anything above black (black should turn white)
	thresh_val = 90
	blocksize = 101
	constant = 40
	thresh = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blocksize, constant) 
	
	

	#Find the black outline around each block
	image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	#Destroy any contours that are below a certain threshold (to get rid of false outlines)
	contours = removeExtraContours(contours, img_color)
	
	#cv2.imshow("contours", cv2.drawContours(cv2.cvtColor(thresh.copy(), cv2.COLOR_GRAY2BGR), contours, -1, (0,  255, 0), 5))
	#cv2.waitKey(0)

	#check if biggest contour is just the entire image (if so, delete that extra contour)
	if len(contours) > 0:	#Unless there are no contours,
		x,y,width,height=cv2.boundingRect(contours[0])
		if(width == img_color.shape[1]):
			contours = contours[1:]
		
	return (img_color, contours)

#Determine the area of a color that a given region contains
def getColorArea(region_bgr, region_hsv, lower_hsv, upper_hsv):
	mask = cv2.inRange(region_hsv, lower_hsv, upper_hsv)	#Find mask excluding everything except the given color
	color_region = cv2.bitwise_and(region_bgr, region_bgr, mask = mask) #Blacken everything except this color
	
	#Convert to grayscale and apply threshold to binarize the image (totally white for target color area, totally black elsewhere)
	color_region = cv2.cvtColor(color_region, cv2.COLOR_BGR2GRAY) 
	ret, color_region = cv2.threshold(color_region, 10, 255, cv2.THRESH_BINARY) #TODO: better threshold value? (currently arbitrary)
	
	#Find the contour surrounding the color region
	i, color_contours, h = cv2.findContours(color_region, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	if len(color_contours) == 0: #If no area of this color was found
		return 0
	else:
		#Find the area of the largest contour (TODO: Find the sum of all contour areas?)
		color_contour_max_area = max(color_contours, key = cv2.contourArea)
		return cv2.contourArea(color_contour_max_area)

		
#def orderContoursByLocation(contours):
	
		
def getBlockListFromImage(img):
	img_color, contours = getContoursFromImage(img)
	
	block_list = [] #list containing lists of colors in each block
	for block_contour in contours: #for each block
		x, y, width, height = cv2.boundingRect(block_contour) #Find the closest rectangle over this block
		block_region = img_color[y:(y+height), x:(x+width)]; #crop the image to the rectangle of the block
		
		color_areas = [0] * len(colors) #initialize a list of 0s representing the area of each possible color
		
		block_region_hsv = cv2.cvtColor(block_region, cv2.COLOR_BGR2HSV) #convert to hsv for better color differentiation
				
		print("\nColor areas:")
				
		for color in colors: #for each color
			#Determine the area of that color contained by the region
			color_area = getColorArea(block_region, block_region_hsv, color_ranges[color][0], color_ranges[color][1])
			
			if color == RED: 
				red2_area = getColorArea(block_region, block_region_hsv, lower_red2, upper_red2)
				color_area += red2_area
						
			#print(color_names[color] + ": " + str(color_area))
			
			color_areas[color] = color_area

		colors_in_region = set() #unordered list of colors in this block
		
		total_region_area = width*height
		for color in colors:
			color_percentage = round(color_areas[color] / total_region_area * 100, 2)
			#print(color_names[color] + ": " +  str(color_percentage) + "%")
			
			if color_percentage > 10:
				colors_in_region.add(color)

		block_list.append(colors_in_region)
	return block_list

#ISSUE: If two blocks are touching, black border will get both, so they will be one block
	#FIX: Get inner contours, not outer. just change that part of the code.
#TODO: Ensure correct order of blocks in image (left to right, up to down)
#blockList = getBlockListFromImage("blocks_with_words.jpg")

	