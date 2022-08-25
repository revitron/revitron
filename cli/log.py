from environment import getEnv


def getLogFromEnv():
	env = getEnv()
	return CliLog(env.log)


class CliLog():

	def __init__(self, file):
		self.file = file

	def write(self, text):
		with open(self.file, 'a') as log:
			log.write('{}\n'.format(text))

	def readAndPrint(self):
		with open(self.file, 'r') as f:
			log = f.read()
		print(log)
