import sys
import json
import os
from os.path import dirname, join, abspath

try:
	configFile = sys.argv[2]
except:
	print('Please provide a configuration file')
	sys.exit()

file = open(configFile)
config = json.load(file)
file.close()

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

task = join(dirname(commandDir), 'run', 'analyse.py')

os.system('{} run {} {} --purge'.format(pyRevitBin, task, model))
