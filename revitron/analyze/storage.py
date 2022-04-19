"""
This submodule is a collection of storage drivers that can be used to store extracted model information 
in different types of formats such as SQLite, JSON or API based databases.
"""
import json
import sqlite3
import sys
import requests
from revitron import Log
from time import time
from datetime import datetime
from abc import ABCMeta, abstractmethod
from collections import OrderedDict


class AbstractStorageDriver:
	"""
	The abstract storage driver is the base class for all storage driver classes.
	"""
	__metaclass__ = ABCMeta

	def __init__(self, config):
		"""
		Init a new storage driver instance with a givenm configuration.

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


class DirectusStorageDriver(AbstractStorageDriver):
	"""
	This storage driver handles storing snapshots to in Directus using the Directus API.
	"""

	def __init__(self, config):
		"""
		Init a new Directus storage driver instance with a givenm configuration.

		Args:
			config (dict): The driver configuration
		"""
		try:
			self.collection = config['collection']
			self.host = config['host'].rstrip('/')
			self.token = config['token']
		except:
			Log().error('Invalid Directus configuration')
			sys.exit(1)
		self.timestamp = datetime.fromtimestamp(time()).strftime('%Y-%m-%dT%H:%M:%S')

	@property
	def _headers(self):
		return {
		    'Accept': 'application/json',
		    'Authorization': 'Bearer {}'.format(self.token),
		    'Content-Type': 'application/json'
		}

	def _get(self, endpoint):
		response = requests.get(
		    '{}/{}'.format(self.host,
		                   endpoint),
		    headers=self._headers
		)
		try:
			responseJson = response.json()
			return responseJson['data']
		except:
			Log().error('Request has failed')
			print(response.json())
			return None

	def _post(self, endpoint, data):
		response = requests.post(
		    '{}/{}'.format(self.host,
		                   endpoint),
		    headers=self._headers,
		    data=json.dumps(data)
		)
		try:
			responseJson = response.json()
			return responseJson['data']
		except:
			Log().error('Request has failed')
			print(response.json())
			return None

	def _getRemoteCollection(self):
		return self._get('collections/{}'.format(self.collection))

	def _createMissingCollection(self):
		return self._post(
		    'collections',
		    {
		        'collection': self.collection,
		        'schema': {},
		        'meta': {
		            'icon': 'pie_chart'
		        }
		    }
		)

	def _getRemoteFields(self):
		fields = []
		data = self._get('fields/{}'.format(self.collection))
		if data:
			for item in data:
				fields.append(item['field'])
		return fields

	def _createField(self, name, dataType):
		data = {
		    'field': name,
		    'type': dataType.replace('real',
		                             'float'),
		    'schema': {},
		    'meta': {
		        'icon': 'data_usage'
		    }
		}
		return self._post('fields/{}'.format(self.collection), data)

	def _createMissingFields(self, dataProviderResults):
		remoteFields = self._getRemoteFields()
		if 'model_size' not in remoteFields:
			self._createField('model_size', 'float')
		if 'timestamp' not in remoteFields:
			self._createField('timestamp', 'timestamp')
		for item in dataProviderResults:
			if item.name not in remoteFields:
				self._createField(item.name, item.dataType)

	def add(self, dataProviderResults, modelSize):
		"""
		Send a POST request to the Directus API in order store a snapshot

		Args:
			dataProviderResults (list): The list of 
				:class:`revitron.analyze.DataProviderResult` objects
			modelSize (float): The model size in bytes
		"""
		if self._getRemoteCollection() is None:
			self._createMissingCollection()
		self._createMissingFields(dataProviderResults)
		data = {}
		data['model_size'] = modelSize
		data['timestamp'] = self.timestamp
		for item in dataProviderResults:
			data[item.name] = item.value
		self._post('items/{}'.format(self.collection), data)


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
			with open(file) as handle:
				snapshots = json.load(handle, object_pairs_hook=OrderedDict)
		except:
			snapshots = []
		data = OrderedDict()
		data['timestamp'] = self.timestamp
		data['model_size'] = modelSize
		for item in dataProviderResults:
			data[item.name] = item.value
		snapshots.append(data)
		with open(file, 'w') as handle:
			json.dump(snapshots, handle, indent=2)


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
