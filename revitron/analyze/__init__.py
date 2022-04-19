"""
The ``analyze`` module helps you to automate analysing the health and status of a model and to extract 
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


class ModelAnalyzer:
	"""
	The ``ModelAnalyzer`` class applies a configured set of data providers on a model 
	and creates snapshots with the extracted statistics in a given SQLite database.
	"""

	def __init__(self, configJson):
		"""
		Init a ``ModelAnalyzer`` instance.

		Args:
			configJson (string): The configuration JSON file
		"""
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
			Log().error('Invalid analyzer configuration JSON file')
			sys.exit(1)

	def snapshot(self):
		"""
		Create a snapshot and store the given ``DataProviderResult`` list along with a 
		timestamp using a given storage driver.
		"""
		logger = Log()
		results = []
		try:
			storageDriverModule = __import__(__name__)
			storageDriverClass = getattr(
			    storageDriverModule,
			    '{}StorageDriver'.format(self.storageDriver)
			)
			storageDriverInstance = storageDriverClass(self.storageConfig)
		except:
			logger.error('Error instanciating the storage driver')
			sys.exit(1)
		for provider in self.providers:
			providerClass = provider.get('class')
			providerName = provider.get('name')
			providerConfig = provider.get('config')
			try:
				results.append(
				    DataProviderResult(providerClass,
				                       providerName,
				                       providerConfig)
				)
			except:
				logger.error(
				    'Error instanciating {} for provider "{}"'.format(
				        providerClass,
				        providerName
				    )
				)
		try:
			modelSize = os.path.getsize(self.model)
		except:
			modelSize = 0
		storageDriverInstance.add(results, modelSize)

	def _getLocalPath(self, model):
		if model['type'] == 'local':
			return model['path']
		else:
			modelGUID = model['modelGUID']
			projectGUID = model['projectGUID']
			directory = 'C:\\Users\\{}\\AppData\\Local\\Autodesk\\Revit\\Autodesk Revit {}\\CollaborationCache'.format(
			    os.getenv('username'),
			    pyrevit.HOST_APP.uiapp.Application.VersionNumber
			)
			pattern = os.path.join(
			    directory,
			    '*',
			    projectGUID,
			    '{}.rvt'.format(modelGUID)
			)
			files = glob.glob(pattern)
			try:
				return files[0]
			except:
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
