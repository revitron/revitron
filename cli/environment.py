import os
import uuid
import tempfile


def setEnv(configFile):
	processId = uuid.uuid4().hex
	log = r'{}\revitron.cli.{}.log'.format(tempfile.gettempdir(), processId)
	os.environ['REVITRON_CLI_PROCESS'] = processId
	os.environ['REVITRON_CLI_CONFIG'] = configFile
	os.environ['REVITRON_CLI_LOG'] = log
	return Environment(configFile, processId, log)


def getEnv():
	processId = os.getenv('REVITRON_CLI_PROCESS')
	configFile = os.getenv('REVITRON_CLI_CONFIG')
	log = os.getenv('REVITRON_CLI_LOG')
	return Environment(processId, configFile, log)


class Environment():

	configFile = None
	processId = None
	log = None

	def __init__(self, configFile, processId, log):
		self.processId = processId
		self.configFile = configFile
		self.log = log
