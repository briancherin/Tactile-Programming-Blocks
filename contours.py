import cv2, numpy as np
import imutils

img = cv2.imread('notebook.jpg')
img_color = imutils.resize(img, width=600)
img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
img_gray_3c = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR) #3 channels for stacked viewing with rgb

img_edges = cv2.Canny(img_gray, 100, 200)



print img_color.shape
print img_gray.shape



cv2.imshow("notebook", np.hstack([img_gray, img_edges]))
cv2.waitKey(0)
cv2.destroyAllWindows()