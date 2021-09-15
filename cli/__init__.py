import sys
import json
import os
from os.path import dirname, join, abspath, isfile, exists


class Command():

	def __init__(self, command):
		configFile = self.getConfigFile()
		config = self.getConfig(configFile)
		try:
			model = config['model']
		except:
			print('No model has been defined in the config')
			sys.exit()
		try:
			revitVersion = ' --revit={}'.format(config['revit'])
		except:
			revitVersion = ''
		self.configFile = configFile
		self.model = model
		self.revitVersion = revitVersion
		self.pyRevitBin = self.getPyRevitBin()
		self.task = self.getTask(command)
		self.setEnv()
		CliLog.new(self.task)

	def getTask(self, command):
		task = join(dirname(__file__), 'run', '{}.py'.format(command))
		if not exists(task):
			print('Command not found!')
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
		configFile = abspath(join(os.getcwd(), sys.argv[2]))
		if not isfile(configFile):
			configFile = sys.argv[2]
		return configFile

	def getPyRevitBin(self):
		pyRevitPath = abspath(join(dirname(__file__), '../../../'))
		pyRevitBin = join(pyRevitPath, 'bin', 'pyrevit.exe')
		if not exists(pyRevitBin):
			pyRevitBin = 'pyrevit.exe'
		return pyRevitBin

	def run(self):
		os.system(
		    '{} run {} {} {}'.format(
		        self.pyRevitBin,
		        self.task,
		        self.model,
		        self.revitVersion
		    )
		)
		CliLog.show()

	def setEnv(self):
		os.environ['REVITRON_ANALYSE_CFG_FILE'] = self.configFile


class CliLog:

	file = 'C:\\temp\\revitron.cli.log'

	@staticmethod
	def new(text):
		f = open(CliLog.file, 'w')
		f.write('{}\n'.format(text))
		f.close()

	@staticmethod
	def stdout():
		f = open(CliLog.file, 'a')
		sys.stdout = f

	@staticmethod
	def show():
		sys.stdout = sys.__stdout__
		with open(CliLog.file, 'r') as f:
			print(f.read())
