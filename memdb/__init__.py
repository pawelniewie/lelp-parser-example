class MemDb:
	def __init__(self):
		self.snapshots = []
		self.transaction = {}

	def set(self, name, value):
		self.transaction[name] = value

	def get(self, name):
		return self.transaction.get(name, "NULL")

	def unset(self, name):
		self.transaction.pop(name, None)

	def numEqualTo(self, 	value):
		"""Return number of variables equal to the given value."""
		counter = 0
		for val in self.transaction.values():
			if (val == value):
				counter += 1
		return counter

	def begin(self):
		self.snapshots.append(self.transaction.copy())

	def rollback(self):
		if len(self.snapshots) == 0:
			raise RuntimeError("INVALID ROLLBACK")
		self.transaction = self.snapshots.pop()

	def commit(self):
		if len(self.snapshots) > 0:
			self.snapshots = []
