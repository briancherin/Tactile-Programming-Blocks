import cv2, numpy as np, imutils
import block_helper

cap = cv2.VideoCapture(4)

while True:
	ret, frame = cap.read()
	frame = imutils.resize(frame, width=600)	#resize image
	frame = imutils.resize(cv2.imread("test_images/blocks_with_words.jpg"), width=600)
	contours, blockSet = block_helper.getBlockListFromImage(frame)
	#print blockSet
	for x in range (0, len(blockSet)):
		print("Block " + str(x+1) + ":")
		block_helper.printColorSet(blockSet[x])
		
		
		
	print("")
	
	cv2.drawContours(frame, contours, -1, (0, 255, 0), 5)
	
	cv2.imshow('frame', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'): #Increase waitKey time to decrease frame rate
		break
cap.release()
cv2.destroyAllWindows()

#Fixes:
#Blocks can not be slanted - change bounding box mechanism so it is not a rectangular that must be parallel  to axes
