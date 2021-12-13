import re
import sys
import json
import os
from os.path import dirname, join, abspath, isfile, exists


class Command:

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
		logFile = 'log'
		code = os.system(
		    '{} run {} {} {} > {}'.format(
		        self.pyRevitBin,
		        self.task,
		        self.model,
		        self.revitVersion,
		        logFile
		    )
		)
		log = self.getLog(logFile)
		os.unlink(logFile)
		runtime = self.getRuntime(log)
		print(log)
		if runtime == '2710' and code == 0:
			print(
			    'Successfully finished "{}" command.'.format(
			        os.path.basename(self.task).replace('.py',
			                                            '')
			    )
			)
		else:
			print(
			    'ERROR: Command execution has failed. Please make sure you use IronPython 2.7.10 as your pyRevit runtime.'
			)
		return code

	def getLog(self, logFile):
		try:
			with open(logFile, 'r') as file:
				log = file.read()
		except:
			log = ''
		return log

	def getRuntime(self, log):
		try:
			search = re.search(r'Path:\s*"[^"]+\D(\d{3,4})\\pyRevitLoader\.dll"', log)
			runtime = search.group(1)
		except:
			runtime = False
		return runtime

	def setEnv(self):
		os.environ['REVITRON_CLI_CONFIG'] = self.configFile
