from memdb import Parser
import unittest


class ParserTest(unittest.TestCase):

	data = [('''
		SET a 10
		GET a
		UNSET a
		GET a
		END
		''', '''
		10
		NULL
		''')]

	def testData(self):
		parser = new Parser()
		for test in data:
			parser.parseString()