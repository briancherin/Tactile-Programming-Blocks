import block_helper, cv2, imutils

RED = block_helper.RED
YELLOW = block_helper.YELLOW
GREEN = block_helper.GREEN
BLUE = block_helper.BLUE
PURPLE = block_helper.PURPLE

#function chart
IF = {BLUE, GREEN} #if - red-yellow
TRUE = {RED, GREEN} #true - red-green
#FALSE = {RED, AQUA} #false - red-aqua
WHILE = {RED, BLUE} #while - red-blue
SAY = {RED, PURPLE} #say - red-purple
LED = {YELLOW, RED} #LED - yellow-green

ZERO = {BLUE}
ONE = {RED}
THREE = {YELLOW}
LESS_THAN = {GREEN}


block_identities = {
	tuple(IF): "if",
	tuple(TRUE): "true",
	#tuple(FALSE): "false",
	tuple(WHILE): "while",
	tuple(SAY): "say",
	tuple(LED): "LED()",
	tuple(ZERO): "0",
	tuple(ONE): "1",
	tuple(THREE): "3",
	tuple(LESS_THAN): "<",
}

#[
	#[0, [IF, TRUE]] #Row 1
	#[1, [LED]] 					#Row 2
#]
#becomes (printed to file):
#if true:\n
#[tab]led()
def translate_to_code_file(output_file_name, block_rows): #list of block identities in rows, with indent level
	final_code = ""
	
	for row in block_rows:
		indent_level = row[0]
		final_code += "    " * indent_level #Add correct number of indent spaces to this line
			
		blocks = row[1]
		semicolon_at_end = False
		for block in blocks:
			if block == IF: #TODO: Add or WHILE
				semicolon_at_end = True
			final_code += block_identities[tuple(block)] + " "
		#End of the row:
		if semicolon_at_end: #Add a semicolon if needed
			final_code = final_code[0:-1] #Get rid of the extra space at the end
			final_code += ":"
		final_code += "\n" #Move to the next line


	f = open(output_file_name, "w")
	f.write(final_code)
	f.close()
	
			
#TODO: For each row, add correct amount of spaces for indent_level
#TODO: if see an "if", go to end of row and add a ":"
#Write string first, and then write to file?

img = cv2.imread("./test_images/real_blocks_numbers_code.jpg") #open image
img = imutils.resize(img, width=400)	#resize image [to reduce resolution???]
img, contours = block_helper.getContoursFromImage(img)	#find contours of blocks in the image
sortedContours = block_helper.sortIntoRows(contours) #Split the contours into correctly-ordered rows
sortedContours = block_helper.markIndentSpace(sortedContours) #Add the raw horizontal displacement of each row to the list of rows
sortedContours = block_helper.standardizeIndents(sortedContours)
blockIdentitiesInRows = block_helper.getBlockListFromRowList(img, sortedContours)
translate_to_code_file("block_code.py", blockIdentitiesInRows)
print blockIdentitiesInRows

"""
for row in blockIdentitiesInRows:
	for block in row[1]:
		
		for color in block:
			#print(color)
			print(block_helper.color_names[color])
		print()
	print()
"""


	

