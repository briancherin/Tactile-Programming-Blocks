import block_helper, cv2, imutils

RED = block_helper.RED
YELLOW = block_helper.YELLOW
GREEN = block_helper.GREEN
AQUA = block_helper.AQUA
BLUE = block_helper.BLUE
PURPLE = block_helper.PURPLE

#function chart
IF = {BLUE, GREEN} #if - red-yellow
TRUE = {RED, GREEN} #true - red-green
FALSE = {RED, AQUA} #false - red-aqua
WHILE = {RED, BLUE} #while - red-blue
SAY = {RED, PURPLE} #say - red-purple
LED = {YELLOW, RED} #LED - yellow-green

#At the beginning of each row, determine the horizontal difference from the previous row (length of indent relative to previous)

"""

[
[indent_space1, [block1, block2, block3, block4]], #Row 1
[indent_space2, [block1]], #Row 2
[indent_space2, [block2]]  #Row 3
]

Example: Row 1 has indent_space of 0 (first row), Row 2 indent_space = Row 3 indent_space (indented under same [if] block)



If see 'if', add ':' to end of the row.


if true
LED

if 3 < 5
LED








"""

def translate_to_code(tuple_name):
	f = open("myfile.py", "w")
	for list_name in tuple_name:
		if list_name == IF:
			f.write("if ")
		elif list_name == TRUE:
			f.write("true:\n")
		elif list_name == FALSE:
			f.write("false:\n")
		elif list_name == WHILE:
			f.write("while ")
		elif list_name == SAY:
			f.write("say ")
		elif list_name == LED:
			f.write("LED ")

test_blocks = [{GREEN, BLUE}, {RED, GREEN}, {YELLOW, RED}]
#translate_to_code(test_blocks)
img = cv2.imread("./test_images/paper_blocks2.jpg")
img = imutils.resize(img, width=400)
img, contours = block_helper.getContoursFromImage(img)
testIndentSpaceList = [0, 10, 10, 0]
testRowList = []
testRowList.append([0, [contours[0], contours[1]]])
testRowList.append([10, [contours[2]]])
	
block_list = block_helper.getBlockListFromRowList(img, testRowList)
print block_list