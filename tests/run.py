import os
import glob
import sys
import unittest
import inspect
import json


revitronDir = os.path.dirname(os.path.dirname(__file__))
testsDir = os.path.join(revitronDir, 'tests')
tempDir = os.path.join(testsDir, 'temp')
sys.path.append(revitronDir)
sys.path.append(testsDir)

import utils

logFile = os.path.join(tempDir, 'tests.log')
try:
	os.mkdir(os.path.dirname(logFile))
except:
	pass
f = open(logFile, 'w')
sys.stdout = f

configFile = open(os.path.join(tempDir, 'config.json'))
config = json.load(configFile)

suite = unittest.TestSuite()

for file in glob.glob(r'{}\{}'.format(testsDir, config['glob'])):
	module = os.path.basename(file).replace('.py', '')
	__import__(module)
	for name, obj in inspect.getmembers(sys.modules[module]):
		if inspect.isclass(obj):
			suite.addTest(unittest.TestLoader().loadTestsFromTestCase(obj))
		
utils.runSuite(suite)
