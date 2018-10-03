import cv2, numpy as np
import imutils

img = cv2.imread('two_colors_border.jpg')
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

while True:

	contourIndex = cv2.getTrackbarPos('index', 'controls')
	drawn = cv2.drawContours(img_color.copy(), contours, contourIndex, (0, 255, 0), 3)


	x, y, width, height = cv2.boundingRect(contours[contourIndex])
	
	print img_color.shape
	
	print([x, y, width, height])
	
	block_region = img_color[y:(y+width), x:(x+width)]; #crop the image to the rectangle of that contour

	
	
	
	

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