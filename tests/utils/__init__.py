import unittest
from StringIO import StringIO
from fixture import *


def run(testClass):
	if testClass.__module__ == '__main__':
		suite = unittest.TestLoader().loadTestsFromTestCase(testClass)
		runSuite(suite)


def runSuite(suite):
	stream = StringIO()
	runner = unittest.TextTestRunner(stream=stream, verbosity=2)
	runner.run(suite)
	stream.seek(0)
	print(stream.read())


def idsToStr(ids):
	_ids = []
	for eid in ids:
		_ids.append(str(eid.IntegerValue))
	_ids.sort()
	return ','.join(_ids)


class RevitronTestCase(unittest.TestCase):

	def setUp(self):
		self.fixture = Fixture()

	def tearDown(self):
		self.fixture.closeDoc()
