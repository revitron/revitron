import re
import sys
import json
import os
import glob
from os.path import dirname, join, abspath, isfile, exists


class Command:

	def __init__(self, command):
		from environment import setEnv
		from log import CliLog
		configFile = self.getConfigFile()
		config = self.getConfig(configFile)
		try:
			revitVersion = ' --revit={}'.format(config['revit'])
		except:
			revitVersion = ''
		self.configFile = configFile
		self.target = os.path.join(os.path.dirname(__file__), 'target.rvt')
		self.revitVersion = revitVersion
		self.pyRevitBin = self.getPyRevitBin()
		task = self.getTask(command)
		self.env = setEnv(configFile, task)
		self.log = CliLog(self.env.log)
		self.log.write('\nRunning: \n{}\n'.format(task))

	def getTask(self, command):
		task = join(dirname(__file__), 'commands', '{}.py'.format(command))
		if not exists(task):
			parent = os.path.dirname
			root = parent(parent(parent(__file__)))
			for n in range(1, 7):
				depth = n * '*/'
				path = os.path.join(root, depth, '{}.cli.py'.format(command))
				tasks = glob.glob(path)
				if tasks:
					return tasks[0]
			print('Command "{}" not found!'.format(command))
			sys.exit()
		return task

	def getConfig(self, configFile):
		try:
			file = open(configFile)
			config = json.load(file)
			file.close()
		except:
			print('Please provide a valid configuration file')
			sys.exit()
		return config

	def getConfigFile(self):
		try:
			configFile = abspath(join(os.getcwd(), sys.argv[2]))
			if not isfile(configFile):
				configFile = sys.argv[2]
			return configFile
		except:
			return None

	def getPyRevitBin(self):
		pyRevitPath = abspath(join(dirname(__file__), '../../../'))
		pyRevitBin = join(pyRevitPath, 'bin', 'pyrevit.exe')
		if not exists(pyRevitBin):
			pyRevitBin = 'pyrevit.exe'
		return pyRevitBin

	def run(self):
		bufferFile = '{}.buffer'.format(self.env.log)
		execWrapper = os.path.join(os.path.dirname(__file__), 'exec.py')
		code = os.system(
		    '{} run {} {} {} --purge > {}'.format(
		        self.pyRevitBin, execWrapper, self.target, self.revitVersion, bufferFile
		    )
		)
		buffer = getBuffer(bufferFile)
		self.log.write('\n' + buffer)
		self.log.readAndPrint()
		if self.getRuntime(buffer) != '2710' or code != 0:
			print(
			    'ERROR: Command execution has failed. Please make sure you use IronPython 2.7.10 as your pyRevit runtime.'
			)
		return code

	def getRuntime(self, buffer):
		try:
			search = re.search(r'Path:\s*"[^"]+\D(\d{3,4})\\pyRevitLoader\.dll"', buffer)
			runtime = search.group(1)
		except:
			runtime = False
		return runtime


def getBuffer(file):
	try:
		with open(file, 'r') as f:
			buffer = f.read()
	except:
		buffer = ''
	if os.path.isfile(file):
		os.unlink(file)
	return buffer
