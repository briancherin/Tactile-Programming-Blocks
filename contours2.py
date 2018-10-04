import cv2, numpy as np
import imutils

RED = 0
YELLOW = 1
GREEN = 2
BLUE = 3

colors = [RED, YELLOW, GREEN, BLUE]
color_names = ["RED", "YELLOW", "GREEN", "BLUE"]

img = cv2.imread('two_multi_color_blocks.jpg')
img_color = imutils.resize(img, width=600)
img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

img_hsv = cv2.cvtColor(img_color, cv2.COLOR_BGR2HSV)

lower_black = np.array([0, 0, 0])
upper_black = np.array([0, 0, 70])


ret, thresh = cv2.threshold(img_gray, 10, 255, cv2.THRESH_BINARY_INV)


image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


def nothing(x):
	pass

cv2.namedWindow("controls")
cv2.createTrackbar('index', 'controls', 0, len(contours)-1, nothing)
cv2.createTrackbar('h', 'controls', 0, 180, nothing)
cv2.createTrackbar('s', 'controls', 0, 255, nothing)
cv2.createTrackbar('v', 'controls', 0, 255, nothing)



"""COLOR RANGES (HSV):"""




lower_blue = np.array([100, 50, 0])
upper_blue = np.array([140, 255, 255])

#TODO: range for red could also be h = 0 to h = 10
lower_red = np.array([160, 0, 0])
upper_red = np.array([180, 255, 255])

lower_yellow = np.array([10, 0, 0])
upper_yellow = np.array([40, 255, 255])

lower_green = np.array([40, 0, 0])
upper_green = np.array([80, 255, 255])


color_ranges = [
	(lower_red, upper_red),	#INDEX 0 = RED
	(lower_yellow, upper_yellow), #INDEX 1 = YELLOW
	(lower_green, upper_green),	#INDEX 2 = GREEN
	(lower_blue, upper_blue)	#INDEX 3 = BLUE
]




while True:

	contourIndex = cv2.getTrackbarPos('index', 'controls')
	drawn = cv2.drawContours(img_color.copy(), contours, contourIndex, (0, 255, 0), 3)


	x, y, width, height = cv2.boundingRect(contours[contourIndex])
	
	print img_color.shape
	
	print([x, y, width, height])
	
	block_region = img_color[y:(y+height), x:(x+width)]; #crop the image to the rectangle of that contour
	
	#Find block by identifying the black border. Then, crop to that block so we can look only at that block.
	#Then, identify what colors are contained by that block.
	
	#List of colors. For each color, filter (inRange) for that color and calculate the area. Large area --> contains that color.
	color_areas = [0] * len(colors) #initialize a list of 0s for each color
	
	h = cv2.getTrackbarPos('h', 'controls')
	s = cv2.getTrackbarPos('s', 'controls')
	v = cv2.getTrackbarPos('v', 'controls')
	range = 10

	block_region_hsv = cv2.cvtColor(block_region, cv2.COLOR_BGR2HSV)
	
	
	for color in colors: #for each color
		mask = cv2.inRange(block_region_hsv, color_ranges[color][0], color_ranges[color][1])
		color_region = cv2.bitwise_and(block_region, block_region, mask=mask)
		color_region = cv2.cvtColor(color_region, cv2.COLOR_BGR2GRAY)
		ret, color_region = cv2.threshold(color_region, 10, 255, cv2.THRESH_BINARY)
		
		i, color_contours, h = cv2.findContours(color_region, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		
		if len(color_contours) == 0:
			color_areas[color] = 0
		else:
			color_contour_max_area = max(color_contours, key = cv2.contourArea)
			color_areas[color] = cv2.contourArea(color_contour_max_area)
		
	print("Color areas:")
	for color in colors:
		print (color_names[color] + ": " + str(color_areas[color]))
	
	
	"""
	
	
	blue_mask = cv2.inRange(block_region_hsv, lower_blue, upper_blue)
	blue_region = cv2.bitwise_and(block_region, block_region, mask=blue_mask)
	
	
	red_mask = cv2.inRange(block_region_hsv, lower_red, upper_red)
	red_region = cv2.bitwise_and(block_region, block_region, mask=red_mask)
	red_region = cv2.cvtColor(red_region, cv2.COLOR_BGR2GRAY)
	rr, red_region = cv2.threshold(red_region, 10, 255, cv2.THRESH_BINARY)
	
	ir, red_contours, hr = cv2.findContours(red_region, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	if len(red_contours)==0:
		red_area = 0
	else:
		max_red_c = max(red_contours, key = cv2.contourArea)
		red_area = cv2.contourArea(max_red_c)
	
	print("red area = " + str(red_area))
	"""
	
	
	
	
	
	
	
	cv2.imshow("result", np.hstack([block_region]))

	if cv2.waitKey(1) & 0xFF==ord('q'):
		break
	
	
#cv2.waitKey(0)
cv2.destroyAllWindows()


"""
This gets the contours. But there are two many (two per border).
Need to make it one per border. Or at least just look at the one with greater area (!)
Then, determine the coordinates of it and mask the image to just that region.

get the average color of that region
"""