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
			
#For each row, add correct amount of spaces for indent_level
#if see an "if", go to end of row and add a ":"

test_blocks = [{GREEN, BLUE}, {RED, GREEN}, {YELLOW, RED}]
#translate_to_code(test_blocks)
img = cv2.imread("./test_images/paper_blocks2.jpg")
img = imutils.resize(img, width=400)
img, contours = block_helper.getContoursFromImage(img)
testIndentSpaceList = [0, 10, 10, 0]
testRowList = []
testRowList.append([0, [contours[0], contours[1]]])
testRowList.append([10, [contours[2]]])

testBlockRowList = []
testBlockRowList.append([0, [IF, TRUE]])
testBlockRowList.append([10, [LED]])
testBlockRowList.append([10, [SAY]])
testBlockRowList.append([10, [IF, FALSE]])
testBlockRowList.append([20, [LED]])
testBlockRowList.append([0, [SAY]])

block_list = block_helper.getBlockListFromRowList(img, testRowList)
block_list = block_helper.standardizeIndents(block_list)
print block_list


"""
IF TRUE
	LED
	SAY
	IF FALSE
		LED
SAY
"""

#Determine which rows are nested beneat which rows.
#Given a list of rows, in the correct order top to bottom.
#Look at first row and note the indent_space1.
	#Look at the row after. If the indent_space2 > indent_space1 
	#(with some threshold: indent_space2-indent_space1 > threshold) 
		#Consider row2 a child of row1.
	#If row2 is at the same level (or close within threshold) to row1,
		#Consider them to be on the same row.
	#If indent_space2 < indent_space1, 
		#Row is one coding indentation backwards.
"""
STACK

Add first row to stack.
Look at next row. 
	If indent_space2 > indent_space1, make row2 child of row1.
	If indent_space2 == indent_space1, pop (and make this child of previous?)
	

Add first to stack.
Look at next. 
	If indented from top of stack (peek), 
		mark as child of that row. 
		Add this one to stack.
	If it is indented to the LEFT of the previous block,
		pop 
	If not indented from top of stack, 
		pop the top of the stack.
		Mark as child of top of the stack. (If there is no more top of stack, then this is a first-level row, so don't need to mark it as a child of anything. it is its own node (?))
		

IF TRUE
	LED
	SAY
	IF FALSE
		LED
SAY

RESULT: label each row with index of indentation (top level = 0, indented once = 1, twice = 2, etc)
Row 1: [0, [IF, TRUE]]
Row 2: [1, [LED]]
Row 3: [1, [SAY]]
Row 4: [1, [IF, FALSE]]
Row 5: [2, [LED]]
Row 6: [0, [SAY]]

Then, when translating to actual code to file, just add the right number of indentations at beginning of each line.

nestedRowList;

[
	[0, [IF, TRUE]],
	[1, [LED]],
	[1, [SAY]],
	[1, [IF, FALSE]],
	[2, [LED]],
	[0, [SAY]]
]		

stack: parentIndentSpaceStack #Contains indentation space for the previous row
int: indent_counter = 0 #The number of indents forward for the current row
Mark first row as indent_index 0.

for each row after the first:
	indent_diff = row.indent_space - parentIndentSpaceStack.peek() #displacement between current and previous row
	if indent_diff > forward_indent_threshold:	#At a forward indentation level from previous
		indent_counter += 1
		row.indent_index = indent_counter
	if abs(indent_diff) < equal_indentation_level_threshold: #At the same indentation level as previous
		row.indent_index = index_counter
	if indent_diff < -1 * equal_indentation_level_threshold: #At a backwards indentation level from previous
		do:
			indent_counter -= 1
			parentIndentSpaceStack.pop()
			if len(parentIndexStack) > 0:
				indent_diff = row.indent_space - parentIndentSpaceStack.peek()
			else:	#If there is no parent row
				indent_counter = 0	#Mark this as root level indentation
		while indent_counter > 0 and indent_diff < -1 * equal_indentation_level_threshold
		
	parentIndentSpaceStack.push(row.indent_space)
	
	

	
"""
	

