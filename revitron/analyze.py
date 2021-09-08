import sqlite3
from abc import ABCMeta, abstractmethod


class ModelAnalyser:

	def __init__(self, database, providers):
		self.providers = providers
		self.database = ModelAnalyserDatabaseDriver(database)

	def snapshot(self):
		import revitron
		logger = revitron.Log()
		snapshotId = self.database.addSnapshot()
		print(snapshotId)
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
				print(providerName, dataType, value)
			except:
				logger.error(
				    'Error instanciating {} for provider "{}"'.format(
				        providerClass,
				        providerName
				    )
				)


class ModelAnalyserDatabaseDriver:

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
		self.database = dbFile

	def addSnapshot(self):
		conn = sqlite3.connect(self.database)
		cursor = conn.cursor()
		cursor.execute(self.createSnapshotTable)
		cursor.execute(self.insertSnapshot)
		rowId = cursor.lastrowid
		conn.commit()
		conn.close()
		return rowId

	def addData(self, table, dataType, value, snapshotId):
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

	__metaclass__ = ABCMeta

	def __init__(self, config):
		self.config = config

	def _filterElements(self):
		import revitron
		filters = self.config.get('filters')
		fltr = revitron.Filter()
		for f in filters:
			evaluator = getattr(revitron.Filter, f.get('rule'))
			fltr = evaluator(fltr, *f.get('args'))
		return fltr.noTypes().getElements()

	@abstractmethod
	def run(self):
		pass

	@property
	def dataType(self):
		return 'integer'


class ElementCountProvider(DataProviderBase):

	def run(self):
		return len(self._filterElements())


class ElementAreaProvider(DataProviderBase):

	def run(self):
		from revitron import _
		area = 0.0
		for element in self._filterElements():
			area += _(element).get('Area')
		return area

	@property
	def dataType(self):
		return 'real'


class WarningCountProvider(DataProviderBase):

	def run(self):
		import revitron
		return len(revitron.DOC.GetWarnings())
