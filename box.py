#Goal: Get one contour per block. (remove the extra one created by the border / select from one of them)
#To do so: Figure out if a contour contains another contour. 
#	If it doesn't, accept that as the only contour
#	If it does, take either only the outer or inner contour
#This only works if contours are sorted by largest to smallest area (or else you would get both inside and outside)

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

#lower_black = np.array([0, 0, 0])
#upper_black = np.array([180, 255, value])



color_ranges = [
	(lower_red1, upper_red1),	#INDEX 0 = RED
	(lower_red2, upper_red2), 	#INDEX 1 = RED (two different ranges for red)
	(lower_yellow, upper_yellow), #INDEX 2 = YELLOW
	(lower_green, upper_green),	#INDEX 3 = GREEN
	(lower_aqua, upper_aqua),	#INDEX 4 = AQUA
	(lower_blue, upper_blue),	#INDEX 5 = BLUE
	(lower_purple, upper_purple),#INDEX 6 = PURPLE
	#(lower_black, upper_black)	#INDEX 7 = BLACK
]

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
	
	return contours

	
def removeExtraContours(contours):
	contours = sorted(contours, key = cv2.contourArea, reverse=True) #sort contours by greatest to least area
	max_contour_area = cv2.contourArea(contours[0])
	contours = filterSmallContours(contours, max_contour_area * 0.1) #accept anything larger than 10% of the max block size (TODO: THIS MIGHT CAUSE ISSUES)(?)
	
	#check if biggest contour is just the border of the image
	x,y,width,height = cv2.boundingRect(contours[0])
	if(width == img_color.shape[1]):
		contours = contours[1:]
	
	#Remove extra contours caused by the border of each block
	contours = removeNestedContours(contours)
	
	return contours
	
def printColorList(colorList):
	for color in colorList:
		print (color_names[color])


img = cv2.imread('paper_blocks2.jpg')	#open image
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
contours = sorted(contours, key = cv2.contourArea, reverse=True) #sort contours by greatest to least area




#display contours overlayed on image (for testing)
drawn = cv2.drawContours(img_color.copy(), contours, -1, (0, 255, 0), 3)

cv2.imshow("contours", drawn)
cv2.waitKey(0)



"""
This gets the contours. But there are two many (two per border).
Need to make it one per border. Or at least just look at the one with greater area (!)
Then, determine the coordinates of it and mask the image to just that region.

get the average color of that region
"""