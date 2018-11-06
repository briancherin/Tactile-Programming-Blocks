import cv2, numpy as np, imutils
import block_helper
 
cap = cv2.VideoCapture(4)

while True:
	ret, frame = cap.read()
	
	blockSet = block_helper.getBlockListFromImage(frame)
	print blockSet
	for x in range (0, len(blockSet)):
		print("Block " + str(x+1) + ":")
		block_helper.printColorSet(blockSet[x])
	
	
	
	
	cv2.imshow('frame', frame)
	if cv2.waitKey(100) & 0xFF == ord('q'): #Increase waitKey time to decrease frame rate
		break
cap.release()
cv2.destroyAllWindows()