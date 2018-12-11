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

def removeOuterNestedContours(contours):
	innerIndex = 0
	while innerIndex < len(contours):
		innerContour = contours[innerIndex]
		potentialOuterIndex = innerIndex + 1
		while potentialOuterIndex < len(contours):
			if isNestedContour(contours[potentialOuterIndex], innerContour): #If this contour surrounds the inner one
				contours = contours[0:potentialOuterIndex] + contours[potentialOuterIndex + 1 : ]
				potentialOuterIndex -= 1
			potentialOuterIndex += 1
		innerIndex += 1
		
				
	
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

def emptyFunction(x):
	return x


	
def removeExtraContours(contours, img):

	

	contours = sorted(contours, key = cv2.contourArea, reverse=True) #sort contours by greatest to least area
	
	contours = contours[1:] #Get rid of the border contour (TODO: There might not be a border contour (around entire image) every time, so this might cause issues)
	
	if len(contours) > 0:
		max_contour_area = cv2.contourArea(contours[0])
		contours = filterSmallContours(contours, max_contour_area * 0.1) #accept anything larger than 10% of the max block size (TODO: THIS MIGHT CAUSE ISSUES)(?)
	
	
	
	#cv2.imshow("contours", cv2.drawContours(img, contours, 0, (0,  255, 0), 5))
	#cv2.waitKey(0)
	
	#check if biggest contour is just the border of the image
	#x,y,width,height = cv2.boundingRect(contours[0])
	#if(width == img.shape[1]): #If the contour width equals the image width
	#	contours = contours[1:]	#Delete that largest contour
	
	

	#TODO: BIG ISSUE: FIGURE OUT HOW TO GET RID OF TOO BID AND IRRELEVANT CONTOURS
	#img_area = img.shape[0] * img.shape[1]
	#block_contours = []
	#for contour in contours:
	#	if cv2.contourArea(contour) < img_area * 0.3: #Remove any contour larger than half the image area
	#		block_contours.append(contour)
	#contours = block_contours
	
	#Remove extra contours caused by the border of each block
	#contours = removeNestedContours(contours)
	contours = removeNestedContours(contours)
	
	#cv2.namedWindow("contours")
	#cv2.createTrackbar("ind", "contours", 0, len(contours)-1, emptyFunction)
	
	#while True:
	#	cv2.imshow("contour", cv2.drawContours(img.copy(), contours, cv2.getTrackbarPos("ind", "contours"), (0,  255, 0), 5))
	#	if cv2.waitKey(1) & 0xFF == ord('q'):
	#		break
	#cv2.destroyAllWindows()
	
	
	return contours

def printColorList(colorList):
	for color in colorList:
		print (color_names[color])

def printColorSet(colorSet):
	res = ""
	for color in colorSet:
		res += color_names[color] + " "
	print res

def getContoursFromImage(img_color):

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
	#cv2.waitKey(100)

	#check if biggest contour is just the entire image (if so, delete that extra contour)
	#if len(contours) > 0:	#Unless there are no contours,
	#	x,y,width,height=cv2.boundingRect(contours[0])
	#	if(width == img_color.shape[1]):
	#		contours = contours[1:]
		
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
	
	
#Given a source image and a single contour (of a block) in that image, return a set containing the colors of the block
def getBlockIdentityFromContour(img_color, block_contour):
	x, y, width, height = cv2.boundingRect(block_contour) #Find the closest rectangle over this block
	block_region = img_color[y:(y+height), x:(x+width)]; #crop the image to the rectangle of the block
	
	color_areas = [0] * len(colors) #initialize a list of 0s representing the area of each possible color
	
	block_region_hsv = cv2.cvtColor(block_region, cv2.COLOR_BGR2HSV) #convert to hsv for better color differentiation
			
			
	for color in colors: #for each color
		#Determine the area of that color contained by the region
		color_area = getColorArea(block_region, block_region_hsv, color_ranges[color][0], color_ranges[color][1])
		
		if color == RED: 
			red2_area = getColorArea(block_region, block_region_hsv, lower_red2, upper_red2)
			color_area += red2_area
							
		color_areas[color] = color_area

	colors_in_block = set() #unordered list of colors in this block
	
	total_region_area = width*height
	for color in colors: #For each color
		#Determine the proportion of this color in the block
		color_percentage = round(color_areas[color] / total_region_area * 100, 2)
		
		if color_percentage > 10: #If there is a significant quantity of this color in the block
			colors_in_block.add(color) #Consider it a color that makes up the block's identity
	return colors_in_block
	
#Get border of each block (stored as a contour)
#Send list of contours to orderFunction
	#This returns a list of lists, where each inner list represents a single row of blocks, and each inner list contains the contours representing those blocks. 
	#example:
	#[
		#[contour_of_block1, contour_of_block_2]
		#[contour_of_block3]
	#]
	#or:
	#[
		#[IF, TRUE]
		#[LED()]
	#]
#For each row
	#For each block
		#Determine the identity of the block by its color combo
		#Get the equivalent code and print to file
		
		
#If considering indent space before each row, order function should return:
#[
	#[indent_space1, [block1, block2, block3, block4]], #Row 1
	#[indent_space2, [block1]], #Row 2
	#[indent_space2, [block2]]  #Row 3
#]

#Example: Row 1 has indent_space of 0 (first row), Row 2 indent_space = Row 3 indent_space (indented under same [if] block)

	
def getBlockListFromImage(img):
	img_color, contours = getContoursFromImage(img)
	
	block_list = [] #list containing lists of colors in each block
	for block_contour in contours: #for each block
		block_colors = getBlockIdentityFromContour(img_color, block_contour)

		block_list.append(block_colors)
	return (contours, block_list)

def getBlockListFromRowList(img_color, ordered_contours):
	block_list = []
	
	#TODO: Adjust for indent_space in ordered_contours? (skip the first element of each row's list (but store the indent_space in the new one too))
	"""
	for row in ordered_contours:
		row_block_list = []
		for block_contour in row:
			block_identity = getBlockIdentityFromContour(img_color, block_contour)
			row_block_list.append(block_identity)
		block_list.append(row_block_list)
	"""
	for row in ordered_contours:
		indent_space = row[0]
		row_blocks = row[1]
		row_block_list = []
		for block_contour in row_blocks:
			block_identity = getBlockIdentityFromContour(img_color, block_contour)
			row_block_list.append(block_identity)
		block_list.append([indent_space, row_block_list])
	
	return block_list
	
# testBlockRowList = [] #Test input list
# testBlockRowList.append([0, [IF, TRUE]])
# testBlockRowList.append([10, [LED]])
# testBlockRowList.append([10, [SAY]])
# testBlockRowList.append([10, [IF, FALSE]])
# testBlockRowList.append([20, [LED]])
# testBlockRowList.append([0, [SAY]])

# rowList.append([1, [IF, TRUE]])
# rowList.append([8, [LED]])

forward_indent_threshold = 7 #Must be at least this distance forward to be considered a forward indent
equal_indent_threshold = 3 #May be this distance forward or backward to be considered at the same indent level
def standardizeIndents(blockRowList):
	indentSpaceStack = [] #Contains indentation space for each potential parent row
	indent_counter = 0	#Begin at root indentation
	
	indentSpaceStack.append(blockRowList[0][0]) #Add the first row's raw indent_space to the stack
	setRowIndentLevel(blockRowList[0], 0) #Mark the first row as root indent level
	
	for row_ind in range (1, len(blockRowList)): #For each row after the first
		curr_row = blockRowList[row_ind]
		original_indent_space = curr_row[0]
		indent_diff = curr_row[0] - indentSpaceStack[-1] #Displacement between this row and the previous row (or the last potential parent)
		print("indent_diff: " + str(indent_diff))
		if indent_diff > forward_indent_threshold: #If this row is an indent forward from the previous
			indent_counter += 1 #Increment the value of the next iteration's potential indent value
			setRowIndentLevel(curr_row, indent_counter)
		elif abs(indent_diff) < equal_indent_threshold:	 #If this row is at the same indentation level as previous
			#indent_counter does not change
			setRowIndentLevel(curr_row, indent_counter)
		elif indent_diff < -1 * equal_indent_threshold:	#If this row is at a previous (more leftward) indentation than previous
			while indent_counter >= 0 or abs(indent_diff) < equal_indent_threshold: #Until root level or a row with the same indent level is reached
				
				if abs(indent_diff) < equal_indent_threshold: #if row with same indent level is reached
					break
				
				indent_counter -= 1 #This row will be at least one indent backward
				
								
				if len(indentSpaceStack) > 0: #As long as there is still something left on the stack
					indentSpaceStack.pop() #The previous row is not a potential parent for this row. Remove it from the stack
				
				if len(indentSpaceStack) > 0:  #If there are any potential parent rows still (i.e. root level has not been reached)
					indent_diff = curr_row[0] - indentSpaceStack[-1] #Recalculate the displacement from the last possible parent
					print("indent_diff (re): " + str(indent_diff))
				else: #Root level has been reached
					indent_counter = 0 
					break	#Exit the loop
			setRowIndentLevel(curr_row, indent_counter)
		indentSpaceStack.append(original_indent_space)
	return blockRowList
			
def setRowIndentLevel(row, indent_level):
	row[0] = indent_level


	

#ISSUE: If two blocks are touching, black border will get both, so they will be one block
	#FIX: Get inner contours, not outer. just change that part of the code. (but threshold might not be accurate enough for that)
#TODO: Ensure correct order of blocks in image (left to right, up to down)
#blockList = getBlockListFromImage("blocks_with_words.jpg")

	