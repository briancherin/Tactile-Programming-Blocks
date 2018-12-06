import block_helper

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

testBlockRowList = [] #Test input list
testBlockRowList.append([0, [IF, TRUE]])
testBlockRowList.append([10, [LED]])
testBlockRowList.append([10, [SAY]])
testBlockRowList.append([10, [IF, FALSE]])
testBlockRowList.append([20, [LED]])
testBlockRowList.append([0, [SAY]])

expectedIndentBlockList = [] #Expected output list - indent_spaces should become standardized
expectedIndentBlockList.append([0, [IF, TRUE]])
expectedIndentBlockList.append([1, [LED]])
expectedIndentBlockList.append([1, [SAY]])
expectedIndentBlockList.append([1, [IF, FALSE]])
expectedIndentBlockList.append([2, [LED]])
expectedIndentBlockList.append([0, [SAY]])



"""
IF TRUE
	LED
	SAY
	IF FALSE
		LED
SAY
"""