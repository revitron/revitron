"""
This submodule is a collection of storage drivers that can be used to store extracted model information 
in different types of formats such as SQLite, JSON or API based databases.
"""
import sqlite3
import sys
from revitron import Log
from pyrevit import script
from time import time
from datetime import datetime
from abc import ABCMeta, abstractmethod


class AbstractStorageDriver:
	"""
	The abstract storage driver is the base class for all storage driver classes.
	"""
	__metaclass__ = ABCMeta

	def __init__(self, config):
		"""
		Inits a new storage driver instance with a givenm configuration.

		Args:
			config (dict): The driver configuration
		"""
		self.config = config
		self.timestamp = datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')

	@abstractmethod
	def add(self, dataProviderResults, modelSize):
		"""
		Add a new snapshot.

		Args:
			dataProviderResults (list): The list of 
				:class:`revitron.analyze.DataProviderResult` objects
			modelSize (float): The local file's size in bytes
		"""
		pass


class JSONStorageDriver(AbstractStorageDriver):
	"""
	This storage driver handles appending snapshots to JSON files.
	"""

	def add(self, dataProviderResults, modelSize):
		"""
		Add a new item to JSON file.

		Args:
			dataProviderResults (list): The list of 
				:class:`revitron.analyze.DataProviderResult` objects
			modelSize (float): The local file's size in bytes
		"""
		try:
			file = self.config['file']
		except:
			Log().error('No JSON file defined')
			sys.exit(1)
		try:
			snapshots = script.load_json(file)
		except:
			snapshots = []
		data = dict()
		data['timestamp'] = self.timestamp
		data['model_size'] = modelSize
		for item in dataProviderResults:
			data[item.name] = item.value
		snapshots.append(data)
		script.dump_json(snapshots, file)


class SQLiteStorageDriver(AbstractStorageDriver):
	"""
	This storage driver handles the connection to the SQLite database as well as the actual 
	creation of the snapshots.
	"""

	def add(self, dataProviderResults, modelSize):
		"""
		Add a new row to the snapshots table.

		Args:
			dataProviderResults (list): The list of 
				:class:`revitron.analyze.DataProviderResult` objects
			modelSize (float): The local file's size in bytes
		"""
		try:
			file = self.config['file']
		except:
			Log().error('No SQLite database file defined')
			sys.exit(1)
		create = ''
		insertColumns = ', model_size'
		insertParams = ', :model_size'
		data = dict()
		data['model_size'] = modelSize
		for item in dataProviderResults:
			create = '{} {} {},'.format(create, item.name, item.dataType)
			insertColumns = '{}, {}'.format(insertColumns, item.name)
			insertParams = '{}, :{}'.format(insertParams, item.name)
			data[item.name] = item.value
		conn = sqlite3.connect(file)
		cursor = conn.cursor()
		cursor.execute(self._createTable.format(create))
		cursor.execute(self._insertRow.format(insertColumns, insertParams), data)
		conn.commit()
		conn.close()

	@property
	def _createTable(self):
		return """
			CREATE TABLE IF NOT EXISTS snapshots(
				id integer PRIMARY KEY AUTOINCREMENT,
				timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,{}
				model_size real
			)
		"""

	@property
	def _insertRow(self):
		return """
			INSERT INTO snapshots(id{}) VALUES(null{})
		"""
