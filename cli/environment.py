import os
import uuid
import tempfile


def setEnv(configFile, task):
	processId = uuid.uuid4().hex
	log = r'{}\revitron.cli.{}.log'.format(tempfile.gettempdir(), processId)
	os.environ['REVITRON_CLI_PROCESS'] = processId
	os.environ['REVITRON_CLI_CONFIG'] = configFile
	os.environ['REVITRON_CLI_LOG'] = log
	os.environ['REVITRON_CLI_TASK'] = task
	return Environment(configFile, processId, log, task)


def getEnv():
	processId = os.getenv('REVITRON_CLI_PROCESS')
	configFile = os.getenv('REVITRON_CLI_CONFIG')
	log = os.getenv('REVITRON_CLI_LOG')
	task = os.getenv('REVITRON_CLI_TASK')
	return Environment(processId, configFile, log, task)


class Environment():

	configFile = None
	processId = None
	log = None
	task = None

	def __init__(self, configFile, processId, log, task):
		self.processId = processId
		self.configFile = configFile
		self.log = log
		self.task = task
