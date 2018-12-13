# NEW ALGORITHM
# 1. Sort everything by x (unsorted list)
# 2. Put first thing in unsorted list into new list of lists (the list of rows)
# 3. append anything that overlaps
# 4. remove overlaps from original list
# 5. repeat steps 2, 3, and 4 until unsorted list is empty

import block_helper
import cv2
import imutils

def takeFirst(elem):
    return elem[0]
    

img = cv2.imread("three_blocks.jpg")
img = imutils.resize(img, width = 400)
img_color, contourList = block_helper.getContoursFromImage(img) #contours are given in order of decreasing area

coordinate_list = []
height_list = []


def sortIntoRows(contourList):
	# add the contours to a list
	for contour in contourList:
		x, y, width, height = cv2.boundingRect(contour)
		coordinate_list.append((x,y,width,height))

	# begin step 1
	# sort contour list first by x-coordinate
	coordinate_list.sort(key=takeFirst)
	# end step 1

	row_list = list()
	row = 0
	# begin step 5
	while len(coordinate_list) > 0: # loops until there is nothing in the list anymore
		count = 0
		first_in_row = coordinate_list.pop(0) # first block in the row
		row_list.append([first_in_row])
		while count < len(coordinate_list): # finds everything in row
			# begin step 2
			# end step 2
			# begin steps 3 & 4
			check_row = coordinate_list[count] # the block that we are checking if is in the same row as first_in_row
			if check_row[1] < first_in_row[1] + first_in_row[3]/2 and check_row[1] + check_row[3] > first_in_row[1] + first_in_row[3]/2: # they overlap
				row_list[len(row_list) - 1].append(coordinate_list.pop(count))
			else: # they don't overlap
				count += 1
			# end steps 3 & 4
	# end step 5

