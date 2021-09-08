import sys
import json
import os
from os.path import dirname, join

try:
	configFile = sys.argv[1]
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

pyRevitBin = join(dirname(dirname(dirname(dirname(__file__)))), 'bin', 'pyrevit.exe')
task = join(dirname(__file__), 'run', 'analyse.py')

os.system('{} run {} {}'.format(pyRevitBin, task, model))
