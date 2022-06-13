import os
import sys
import json
from os.path import dirname
from pyrevit import HOST_APP
from System import Guid

sys.path.append(dirname(dirname(dirname(__file__))))

import revitron

worksetConfig = revitron.DB.WorksetConfiguration(
    revitron.DB.WorksetConfigurationOption.OpenAllWorksets
)

openOptions = revitron.DB.OpenOptions()
openOptions.SetOpenWorksetsConfiguration(worksetConfig)

configFile = os.getenv('REVITRON_CLI_CONFIG')

file = open(configFile)
config = json.load(file)
file.close()

try:
	model = config['model']
	if model['type'] == 'local':
		openOptions.DetachFromCentralOption = revitron.DB.DetachFromCentralOption.DetachAndPreserveWorksets
		modelPath = revitron.DB.ModelPathUtils.ConvertUserVisiblePathToModelPath(
		    model['path']
		)
	else:
		try:
			modelPath = revitron.DB.ModelPathUtils.ConvertCloudGUIDsToCloudPath(
			    model['region'], Guid(model['projectGUID']), Guid(model['modelGUID'])
			)
		except:
			modelPath = revitron.DB.ModelPathUtils.ConvertCloudGUIDsToCloudPath(
			    Guid(model['projectGUID']), Guid(model['modelGUID'])
			)
except:
	print('Invalid model configuration')
	sys.exit(1)

revitron.DOC = HOST_APP.uiapp.Application.OpenDocumentFile(modelPath, openOptions)

analyzer = revitron.ModelAnalyzer(configFile)
analyzer.snapshot()

revitron.DOC.Close(False)