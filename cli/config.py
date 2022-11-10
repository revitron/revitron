import os
import sys
import json
import revitron
from System import Guid


class Config:

	def __init__(self, detach=True):
		self._configFile = os.getenv('REVITRON_CLI_CONFIG')
		file = open(self._configFile)
		self._config = json.load(file)
		file.close()
		worksetConfig = revitron.DB.WorksetConfiguration(
		    revitron.DB.WorksetConfigurationOption.OpenAllWorksets
		)
		self._openOptions = revitron.DB.OpenOptions()
		self._openOptions.SetOpenWorksetsConfiguration(worksetConfig)
		try:
			model = self._config['model']
			if model['type'] == 'local':
				if detach:
					self._openOptions.DetachFromCentralOption = revitron.DB.DetachFromCentralOption.DetachAndPreserveWorksets
				else:
					self._openOptions.DetachFromCentralOption = revitron.DB.DetachFromCentralOption.DoNotDetach
				self._modelPath = revitron.DB.ModelPathUtils.ConvertUserVisiblePathToModelPath(
				    model['path']
				)
			else:
				try:
					self._modelPath = revitron.DB.ModelPathUtils.ConvertCloudGUIDsToCloudPath(
					    model['region'],
					    Guid(model['projectGUID']),
					    Guid(model['modelGUID'])
					)
				except:
					self._modelPath = revitron.DB.ModelPathUtils.ConvertCloudGUIDsToCloudPath(
					    Guid(model['projectGUID']), Guid(model['modelGUID'])
					)
		except:
			revitron.Log().error('Invalid model configuration')
			print('Invalid model configuration')
			sys.exit(1)

	def get(self):
		return self._config

	@property
	def config(self):
		return self._config

	@property
	def file(self):
		return self._configFile

	@property
	def modelPath(self):
		return self._modelPath

	@property
	def openOptions(self):
		return self._openOptions
