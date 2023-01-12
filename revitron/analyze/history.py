""" 
This submodule provides an synchronizer class for mirroring hsitory data to Directus.
"""
import sqlite3
import re
from revitron.analyze.storage import DirectusAPI, parseToken


class DirectusHistorySynchronizer():
	"""
	This synchronizer class mirrors sync meta data that is tracked by the **Revitron History**
	into a Directus database.
	"""

	def __init__(self, config):
		"""
		Init the synchronizer.

		Args:
			config (dict): The configuration dictionary.
		"""
		try:
			collection = 'history__{}'.format(
			    re.sub(
			        r'[^a-z0-9]+', '_', config['storage']['config']['collection'].lower()
			    )
			)
			host = config['storage']['config']['host'].rstrip('/')
			token = parseToken(config['storage']['config']['token'])
			self.collection = collection
			self.directus = DirectusAPI(host, token, collection)
		except:
			self.collection = None
		self.db = self._getSqliteFile()

	def _getSqliteFile(self):
		import revitron
		config = revitron.DocumentConfigStorage().get('revitron.history', dict())
		return config.get('file', '')

	def sync(self):
		"""
		Fetch sync meta data from the history SQLite file and push it to the Directus database.
		"""
		import revitron
		if not self.collection or not self.db:
			return None

		directus = self.directus
		directus.clearCache()

		if not directus.collectionExists():
			directus.createCollection()

		remoteFields = directus.getFields()

		fields = {
		    'sync_id': 'integer',
		    'start_time': 'timestamp',
		    'user': 'string',
		    'unique_transactions': 'integer',
		    'sync_time': 'float',
		    'filesize': 'float'
		}

		for name in fields:
			if name not in remoteFields:
				directus.createField(name, fields[name])

		items = directus.get('items/{}?limit=-1'.format(self.collection), log=False)

		existingSyncIds = []

		for item in items:
			existingSyncIds.append(item['sync_id'])

		conn = sqlite3.connect(self.db)
		cursor = conn.cursor()

		cursor.execute(
		    """SELECT syncs.syncId, syncs.user, count(transactions.transactions), syncs.startTime, syncs.finishTime, syncs.size
			FROM syncs, transactions 
			WHERE syncs.syncId=transactions.syncId
			GROUP BY syncs.syncId"""
		)
		rows = cursor.fetchall()

		data = []

		for row in rows:
			syncId = row[0]
			if syncId in existingSyncIds:
				continue
			filesize = 0
			if row[5]:
				filesize = row[5]
			data.append({
			    'sync_id': row[0],
			    'start_time': row[3],
			    'user': row[1],
			    'unique_transactions': row[2],
			    'sync_time': revitron.Date.diffMin(row[3], row[4]),
			    'filesize': filesize
			})
			if len(data) > 100:
				directus.post('items/{}'.format(self.collection), data)
				data = []

		if len(data) > 0:
			directus.post('items/{}'.format(self.collection), data)

		directus.clearCache()
