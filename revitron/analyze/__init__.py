"""
The ``revitron.analyze`` module helps you to automate analysing the health and status of a model and to extract 
several types of data and statistics in order to simplifiy BIM quality control. Extracted data is stored 
as snapshots in a SQLite database to be consumed by other applications or dashboards.
"""
import json
import sys
import os
import glob
import pyrevit
from revitron import String
from revitron.analyze.providers import *
from revitron.analyze.storage import *
from revitron.analyze.history import *


class ModelAnalyzer:
	"""
	The ``ModelAnalyzer`` class applies a configured set of data providers on a model 
	and creates snapshots with the extracted statistics in a given SQLite database.
	"""

	def __init__(self, configJson, cliLog):
		"""
		Init a ``ModelAnalyzer`` instance.

		Args:
			configJson (string): The configuration JSON file
			cliLog (CliLog): The CLI log instance
		"""
		self.log = cliLog.write
		file = open(configJson)
		config = json.load(file)
		file.close()
		try:
			self.storageDriver = config['storage']['driver']
			self.storageConfig = config['storage']['config']
			self.providers = config['providers']
			self.model = self._getLocalPath(config['model'])
		except:
			from revitron import Log
			self.log('Invalid analyzer configuration JSON file')
			sys.exit(1)
		self.history = DirectusHistorySynchronizer(config)

	def snapshot(self):
		"""
		Create a snapshot and store the given ``DataProviderResult`` list along with a 
		timestamp using a given storage driver.
		"""
		results = []
		try:
			storageDriverModule = __import__(__name__)
			storageDriverClass = getattr(
			    storageDriverModule, '{}StorageDriver'.format(self.storageDriver)
			)
			storageDriverInstance = storageDriverClass(self.storageConfig)
		except:
			self.log('Error instanciating the storage driver')
			sys.exit(1)
		for provider in self.providers:
			providerClass = provider.get('class')
			providerName = provider.get('name')
			providerConfig = provider.get('config')
			results.append(
			    DataProviderResult(providerClass, providerName, providerConfig)
			)
		try:
			modelSize = os.path.getsize(self.model)
		except:
			modelSize = 0
		storageDriverInstance.add(results, modelSize)
		self.history.sync()
		self.log('Finished snapshot')

	def _getLocalPath(self, model):
		if model['type'] == 'local':
			return model['path']
		else:
			modelGUID = model['modelGUID']
			projectGUID = model['projectGUID']
			fileName = os.path.join(projectGUID, '{}.rvt'.format(modelGUID))
			cliRuntimeCache = os.path.join(os.getcwd(), '_CC', fileName)
			if os.path.isfile(cliRuntimeCache):
				return cliRuntimeCache
			else:
				cache = r'C:\Users\{}\AppData\Local\Autodesk\Revit\Autodesk Revit {}\CollaborationCache'.format(
				    os.getenv('username'),
				    pyrevit.HOST_APP.uiapp.Application.VersionNumber
				)
				pattern = os.path.join(cache, '*', fileName)
				files = glob.glob(pattern)
				try:
					return files[0]
				except:
					return ''
			return ''


class DataProviderResult:
	"""
	The ``DataProviderResult`` object handles the execution of a data provider by creating a unified results object
	containing the provider name, the resulting value and its data type.
	"""

	def __init__(self, providerClass, providerName, providerConfig):
		"""
		Inits a new provider class instances and runs the provider's ``run()`` method
		in order to populate the value property.

		Args:
			providerClass (string): The class name for the data provider that has to be used
			providerName (string): A descriptive name to generate the storage field
			providerConfig (dict): The configuration that is passed to the data provider
		"""
		module = __import__(__name__)
		cls = getattr(module, providerClass)
		providerInstance = cls(providerConfig)
		self._value = providerInstance.run()
		self._name = providerName
		self._valueType = providerInstance.valueType
		self._dataType = providerInstance.dataType

	@property
	def name(self):
		"""
		The name that is used to create a storage field.

		Returns:
			string: The field name
		"""
		return '{}__{}'.format(self._valueType, String.sanitize(self._name).lower())

	@property
	def value(self):
		"""
		The resulting value.

		Returns:
			mixed: The value that is returned by the provider's ``run()`` method
		"""
		return self._value

	@property
	def dataType(self):
		"""
		The data type that is used to store the value.

		Returns:
			string: The data type
		"""
		return self._dataType
