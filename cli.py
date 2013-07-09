#!/usr/local/bin/python3
import sys
try:
	from memdb.parser import Parser
except:
	print("Please install lepl using $> pip3 install lepl")
	sys.exit(111)
from memdb import MemDb

if __name__ == "__main__":
	db = MemDb()
	parser = Parser(db)
	parser.parseFile(sys.stdin, sys.stdout)
