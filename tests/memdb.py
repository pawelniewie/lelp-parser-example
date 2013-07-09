from memdb import MemDb
import unittest


class OperationsTest(unittest.TestCase):
	def setUp(self):
		self.memdb = MemDb()

	def testSetGet(self):
		self.assertEqual(self.memdb.get("a"), "NULL")
		self.memdb.set("a", 123)
		self.assertEqual(self.memdb.get("a"), 123)

	def testNumEqualTo(self):
		self.memdb.set("a", 10)
		self.memdb.set("b", 10)
		self.assertEqual(self.memdb.numEqualTo(10), 2)
		self.assertEqual(self.memdb.numEqualTo(20), 0)
		self.memdb.unset("a")
		self.assertEqual(self.memdb.numEqualTo(10), 1)
		self.memdb.set("b", 30)
		self.assertEqual(self.memdb.numEqualTo(10), 0)

	def testRollbackThrowsAnExceptionWhenNoTransactionIsInProgress(self):
		with self.assertRaises(RuntimeError):
			self.memdb.rollback()

	def testCommitIsNopWhenNoTransactionInProgress(self):
		self.memdb.commit()

	def testMultiLevelTransactions(self):
		db = self.memdb
		self.assertEqual(db.get("a"), "NULL")
		db.begin()
		self.assertEqual(len(db.snapshots), 1)
		db.set("a", 10)
		self.assertEqual(db.get("a"), 10)
		db.begin()
		self.assertEqual(len(db.snapshots), 2)
		db.set("a", 20)
		self.assertEqual(db.get("a"), 20)
		db.rollback()
		self.assertEqual(len(db.snapshots), 1)
		self.assertEqual(db.get("a"), 10)
		db.rollback()
		self.assertEqual(db.get("a"), "NULL")
		with self.assertRaises(RuntimeError):
			db.rollback()

	def testMultiLevelWithCommit(self):
		db = self.memdb
		db.set("a", 50)
		db.begin()
		self.assertEqual(db.get("a"), 50)
		db.set("a", 60)
		db.begin()
		db.unset("a")
		self.assertEqual(db.get("a"), "NULL")
		db.rollback()
		self.assertEqual(db.get("a"), 60)
		db.commit()
		self.assertEqual(db.get("a"), 60)

	def	testNumEqualToInTransaction(self):
		db = self.memdb
		db.set("a", 10)
		db.begin()
		self.assertEqual(db.numEqualTo(10), 1)
		db.begin()
		db.unset("a")
		self.assertEqual(db.numEqualTo(10), 0)
		db.rollback()
		self.assertEqual(db.numEqualTo(10), 1)
