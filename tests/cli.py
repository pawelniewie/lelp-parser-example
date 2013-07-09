import unittest
import os
import subprocess


class CliTest(unittest.TestCase):

	def testData(self):
		data_dir = os.path.dirname(__file__) + "/data"
		for test in os.listdir(data_dir):
			if test.endswith(".in"):
				test_path = data_dir + "/" + test
				output = (subprocess.check_output("python3 cli.py < '%s'" % (test_path), shell=True))
				with open(data_dir + "/" + os.path.splitext(test)[0] + ".out", "rb") as compare:
					self.assertEqual(output, compare.read(), "comparing output for %s" % (test_path))
