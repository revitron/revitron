"""
The ``analyse`` module helps you to automate analysing the health and status of a model and to extract 
several types of data and statistics in order to simplifiy BIM quality control. Extracted data is stored 
as snapshots in a SQLite database to be consumed by other applications or dashboards.
"""

import sqlite3
from abc import ABCMeta, abstractmethod


class ModelAnalyser:
	"""
	The ``ModelAnalyser`` class applies a configured set of data providers on a model 
	and creates snapshots with the extracted statistics in a given SQLite database.
	"""

	def __init__(self, database, providers):
		"""
		Init a ``ModelAnalyser`` instance.

		Args:
			database (string): The path to a configuration JSON file
			providers (list): A list of :class:`DataProviderBase` classes
		"""
		self.providers = providers
		self.database = ModelAnalyserDatabaseDriver(database)

	def snapshot(self):
		"""
		Create a snapshot in a given database
		"""
		import revitron
		logger = revitron.Log()
		snapshotId = self.database.addSnapshot()
		for provider in self.providers:
			module = __import__(__name__)
			providerClass = provider.get('class')
			providerName = provider.get('name')
			providerConfig = provider.get('config')
			cls = getattr(module, providerClass)
			try:
				providerInstance = cls(providerConfig)
				dataType = providerInstance.dataType
				value = providerInstance.run()
				self.database.addData(providerName, dataType, value, snapshotId)
			except:
				logger.error(
				    'Error instanciating {} for provider "{}"'.format(
				        providerClass,
				        providerName
				    )
				)


class ModelAnalyserDatabaseDriver:
	"""
	The database driver handles the connection to the SQLite database as well as the actual 
	creation of the snapshots.
	"""

	createSnapshotTable = """
		CREATE TABLE IF NOT EXISTS snapshots(
			id integer PRIMARY KEY AUTOINCREMENT,
			timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
		)
	"""

	insertSnapshot = """
		INSERT INTO snapshots(id) VALUES(null)
	"""

	createDataTable = """
		CREATE TABLE IF NOT EXISTS {}(
			id integer PRIMARY KEY AUTOINCREMENT,
			value {},
			snapshotId integer
		)
	"""

	insertData = """
		INSERT INTO {}(value, snapshotId) VALUES(:value, :snapshotId)
	"""

	def __init__(self, dbFile):
		"""
		Init a driver for a given SQLite file.

		Args:
			dbFile (string): The path to a SQLite file
		"""
		self.database = dbFile

	def addSnapshot(self):
		"""
		Add a row for a snapshot and return its row ID that can be used to refernce 
		other related data returned from the configured data providers.

		Returns:
			integer: The row ID of the snapshot
		"""
		conn = sqlite3.connect(self.database)
		cursor = conn.cursor()
		cursor.execute(self.createSnapshotTable)
		cursor.execute(self.insertSnapshot)
		rowId = cursor.lastrowid
		conn.commit()
		conn.close()
		return rowId

	def addData(self, table, dataType, value, snapshotId):
		"""
		Insert data that was returned by a given data provider in relation to a snapshot.

		Args:
			table (string): The table name
			dataType (string): The data type of the stored value
			value (mixed): The actual value
			snapshotId (integer): The related snapshot ID
		"""
		import revitron
		table = revitron.String.sanitize(table)
		conn = sqlite3.connect(self.database)
		cursor = conn.cursor()
		cursor.execute(self.createDataTable.format(table, dataType))
		cursor.execute(
		    self.insertData.format(table),
		    {
		        'value': value,
		        'snapshotId': snapshotId
		    }
		)
		conn.commit()
		conn.close()


class DataProviderBase(object):
	"""
	The abstract data provider. A data provider must implement a ``run()`` method
	that actually defines the extracted data.
	"""

	__metaclass__ = ABCMeta

	def __init__(self, config):
		"""
		Init a new data provider with a given configuration.

		Args:
			config (dict): The data provider configuration
		"""
		self.config = config

	def _filterElements(self):
		"""
		Filter elements in the target model by applying all filters that
		are defined in the configuration.

		Returns:
			list: The list of filtered elements
		"""
		import revitron
		filters = self.config.get('filters')
		fltr = revitron.Filter()
		for f in filters:
			evaluator = getattr(revitron.Filter, f.get('rule'))
			fltr = evaluator(fltr, *f.get('args'))
		return fltr.noTypes().getElements()

	@abstractmethod
	def run(self):
		"""
		The abstract method for data extraction. This method
		must be implemented by a data provider.
		"""
		pass

	@property
	def dataType(self):
		"""
		The data type property defines the data type of the provided data in the database.

		Returns:
			string: The data type that is used for provided values in the database
		"""
		return 'integer'


class ElementCountProvider(DataProviderBase):
	"""
	This data provider returns the count of filtered elements after applying all
	filters that are defined in the provider configuration.
	"""

	def run(self):
		"""
		Run the data provider and return the number of filtered elements.

		Returns:
			integer: The number of filtered elements
		"""
		return len(self._filterElements())


class ElementAreaProvider(DataProviderBase):
	"""
	This data provider returns the accumulated area of a set of elements after applying all
	filters that are defined in the provider configuration.
	"""

	def run(self):
		"""
		Apply filters and accumulate the area of the filtered elements.

		Returns:
			integer: The accumulated area
		"""
		from revitron import _
		area = 0.0
		for element in self._filterElements():
			area += _(element).get('Area')
		return area

	@property
	def dataType(self):
		"""
		The area data type is ``real``.

		Returns:
			string: The data type
		"""
		return 'real'


class WarningCountProvider(DataProviderBase):
	"""
	This data provider returns the number of warnings in a model.
	"""

	def run(self):
		"""
		Get the number of warnings.

		Returns:
			integer: The number of warnings
		"""
		import revitron
		return len(revitron.DOC.GetWarnings())
