from lepl import *


class Parser:
	def __init__(self, memdb):
		name = Word()
		value = Real()
		spaces = Space()[0:]
		setOperator = (Literal("SET") & ~spaces & name & ~spaces & value) > self.set
		getOperator = (Literal("GET") & ~spaces & name) > self.get
		unsetOperator = (Literal("UNSET") & ~spaces & name) > self.unset
		numEqualToOperator = (Literal("NUMEQUALTO") & ~spaces & value) > self.numEqualTo
		commitOperator = Literal("COMMIT") > self.commit
		rollbackOperator = Literal("ROLLBACK") > self.rollback
		beginOpertor = Literal("BEGIN") > self.begin
		endOperator = Literal("END")
		newline = spaces & Newline() & spaces
		line = setOperator | getOperator | unsetOperator | numEqualToOperator | commitOperator | rollbackOperator | beginOpertor | endOperator | newline
		self.expression = line[0:, ~newline]

		self.db = memdb

	def set(self, results):
		self.db.set(results[1], results[2])

	def get(self, results):
		return self.db.get(results[1])

	def unset(self, results):
		self.db.unset(results[1])

	def numEqualTo(self, results):
		return self.db.numEqualTo(results[1])

	def commit(self, results):
		self.db.commit()

	def rollback(self, results):
		try:
			self.db.rollback()
		except RuntimeError as e:
			return str(e)

	def begin(self, results):
		self.db.begin()

	def parseFile(self, input, output):
		self.expression.config.clear() # faster compilation time, http://www.acooke.org/lepl/examples.html
		for p in self.expression.parse(input):
			if p == "END":
				break
			if p is not None:
				output.write(str(p) + "\n")