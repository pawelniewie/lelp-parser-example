import sys
from memdb.parser import Parser
from memdb import MemDb

if __name__ == "__main__":
	db = MemDb()
	parser = Parser(db)
	parser.parseFile(sys.stdin, sys.stdout)
