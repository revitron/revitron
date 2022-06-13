import re
import sys
import json
import os
import uuid
import tempfile
from os.path import dirname, join, abspath, isfile, exists

processId = uuid.uuid4().hex
tmp = tempfile.gettempdir()

CLI_BUFFER_FILE = r'{}\revitron.cli.{}.buffer'.format(tmp, processId)
CLI_LOG_FILE = r'{}\revitron.cli.{}.log'.format(tmp, processId)


class Command:

	def __init__(self, command):
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
		self.task = self.getTask(command)
		self.setEnv()
		CliLog.new('\nRunning: \n{}\n'.format(self.task))

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
		code = os.system(
		    '{} run {} {} {} > {}'.format(
		        self.pyRevitBin,
		        self.task,
		        self.target,
		        self.revitVersion,
		        CLI_BUFFER_FILE
		    )
		)
		log = CliLog.get()
		print(log)
		buffer = Buffer.get()
		print(buffer)
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

	def setEnv(self):
		os.environ['REVITRON_CLI_CONFIG'] = self.configFile


class Buffer:

	@staticmethod
	def get():
		try:
			with open(CLI_BUFFER_FILE, 'r') as file:
				buffer = file.read()
		except:
			buffer = ''
		if os.path.isfile(CLI_BUFFER_FILE):
			os.unlink(CLI_BUFFER_FILE)
		return buffer


class CliLog:

	@staticmethod
	def new(text):
		with open(CLI_LOG_FILE, 'w') as f:
			f.write('{}\n'.format(text))

	@staticmethod
	def append(text):
		with open(CLI_LOG_FILE, 'a') as f:
			f.write('{}\n'.format(text))

	@staticmethod
	def get():
		with open(CLI_LOG_FILE, 'r') as f:
			log = f.read()
		return log