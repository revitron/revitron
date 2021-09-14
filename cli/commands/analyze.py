from genericpath import isfile
import sys
import json
import os
from os.path import dirname, join, abspath, isfile

try:
	configFile = abspath(join(os.getcwd(), sys.argv[2]))
	if not isfile(configFile):
		configFile = sys.argv[2]
	file = open(configFile)
	config = json.load(file)
	file.close()
except:
	print('Please provide a valid configuration file')
	sys.exit()

os.environ['REVITRON_ANALYSE_CFG_FILE'] = configFile

try:
	model = config['model']
except:
	print('No model has been defined in the config')
	sys.exit()

commandDir = dirname(__file__)
pyRevitPath = abspath(join(commandDir, '../../../../'))
pyRevitBin = join(pyRevitPath, 'bin', 'pyrevit.exe')

if not os.path.exists(pyRevitBin):
	pyRevitBin = 'pyrevit'

task = join(dirname(commandDir), 'run', 'analyze.py')

os.system('{} run {} {} --purge'.format(pyRevitBin, task, model))
