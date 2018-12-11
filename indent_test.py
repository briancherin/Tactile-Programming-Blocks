import block_helper, unittest

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




class TestIndentation(unittest.TestCase):
	
	#@unittest.skip("")
	def test_standardization(self):
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
		
		standardizedRowList = block_helper.standardizeIndents(testBlockRowList)
		self.assertEqual(standardizedRowList, expectedIndentBlockList)
	
	#@unittest.skip("")
	def test_simple(self):
		rowList = []
		rowList.append([1, [IF, TRUE]])
		rowList.append([9, [LED]])
		
		expected = []
		expected.append([0, [IF, TRUE]])
		expected.append([1, [LED]])
		
		standardized = block_helper.standardizeIndents(rowList)

		self.assertEqual(expected, standardized)
	
	#@unittest.skip("")
	def test_simple2(self):
		rowList = []
		rowList.append([1, [IF, TRUE]])
		rowList.append([8, [LED]])
		rowList.append([2, [IF, FALSE]])
		rowList.append([7, [SAY]])
		rowList.append([0, [LED]])
		
		expected = []
		expected.append([0, [IF, TRUE]])
		expected.append([1, [LED]])
		expected.append([0, [IF, FALSE]])
		expected.append([1, [SAY]])
		expected.append([0, [LED]])
		
		
		standardized = block_helper.standardizeIndents(rowList)
		# print("EXPECTED:")
		# print(expected)
		# print("STAND:")
		# print (standardized)
		
		#self.assertEqual(expected, standardized)
	
	def test_backwards(self):
		rowList = []
		rowList.append([1, [IF, TRUE]])
		rowList.append([10, [IF, TRUE]])
		rowList.append([18, [LED]])
		rowList.append([10, [LED]])
		rowList.append([0, [LED]])
		
		"""
		IF TRUE
			IF TRUE
				LED
		LED
		
		"""
		
		expected = []
		expected.append([0, [IF, TRUE]])
		expected.append([1, [IF, TRUE]])
		expected.append([2, [LED]])
		expected.append([1, [LED]])
		expected.append([0, [LED]])
		
		
		standardized = block_helper.standardizeIndents(rowList)
		self.assertEqual(expected, standardized)	
	
	def test_backwards1(self):
			rowList = []
			rowList.append([1, [IF, TRUE]])
			rowList.append([10, [IF, TRUE]])
			rowList.append([18, [LED]])
			rowList.append([28, [LED]])
			rowList.append([20, [LED]])
			rowList.append([30, [LED]])
			rowList.append([5, [LED]])
			
			"""
			IF TRUE
				IF TRUE
					LED
			LED
			
			"""
			
			expected = []
			expected.append([0, [IF, TRUE]])
			expected.append([1, [IF, TRUE]])
			expected.append([2, [LED]])
			expected.append([3, [LED]])
			expected.append([2, [LED]])
			expected.append([3, [LED]])
			expected.append([0, [LED]])
			
			
			standardized = block_helper.standardizeIndents(rowList)
			self.assertEqual(expected, standardized)	

if __name__ == '__main__':
	unittest.main()



"""
IF TRUE
	LED
	SAY
	IF FALSE
		LED
SAY
"""