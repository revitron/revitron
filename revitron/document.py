""" 
The ``document`` submodule contains classes to interact with the currently 
active **Revit** document or store individual project configurations within a model. 
"""
import json


class Document:
	"""
	A basic wrapper class for Revit documents.
	
	Basic examples are::
	
		path = revitron.Document().getPath()
		if revitron.Document().isFamily():
		    pass

	In case you want to work with any other model than the active one, it is possible to change the context
	to that model using the ``with`` statement. Changing the context to another model will internally redefine 
	the ``revitron.DOC`` property within the scope of that ``with`` statement.
	Therefore it is also possible to use a ``revitron.Filter`` instance on any model by just using a filter within a 
	``with`` statement::

		with revitron.Document(doc):
		    fltr = revitron.Filter().noTypes()
		    elements = fltr.getElements()
	"""
	
	def __init__(self, doc = None):
		"""
		Inits a new Document instance.

		Args:
			doc (object, optional): Any document instead of the active one. Defaults to None.
		"""
		import revitron
		if doc is not None:
			self.doc = doc
		else:
			self.doc = revitron.DOC
	

	def __enter__(self):
		"""
		Set ``revitron.DOC`` to the document of the current ``Document`` class instance. 

		By default that will just be the active document and therefore ``revitron.DOC`` stays unchanged.
		"""
		import revitron
		self.cache = revitron.DOC
		revitron.DOC = self.doc


	def __exit__(self, execType, execValue, traceback):
		"""
		Restore the original context.

		Args:
			execType (string): The execution type
			execValue (string): The execution value
			traceback (mixed): The traceback
		"""
		import revitron
		revitron.DOC = self.cache


	def getDuplicateInstances(self, preferOlderElement = False):
		"""
		Returns a list of duplicate family instances. 
		By default, the list contains always the younger more recently created duplicate instance.

		Note:
			This method requires **Revit 2018** or newer!

		Args:
			preferOlderElement (bool, optional): Optionally return the list with the older instances. Defaults to False.

		Returns:
			list: A list with duplicate instances, either the younger or the older ones.
		"""
		import revitron
		if revitron.REVIT_VERSION < '2018':
			revitron.Log().error('Method revitron.Document.getDuplicateInstances() is not supported by this Revit version!')
			return []
		index = 1
		if preferOlderElement:
			index = 0
		of = revitron.DB.BuiltInFailures.OverlapFailures
		duplicates = []
		for warning in self.doc.GetWarnings():
			if warning.GetFailureDefinitionId().Guid == of.DuplicateInstances.Guid:
				ids = warning.GetFailingElements()		
				duplicates.append(ids[index])
				duplicates = list(set(duplicates))
		return duplicates


	def getLinkedDocuments(self, scope = None):
		"""
		Returns a dictionary of all linked documents.
		The key is the ID of the link and the value is the actual document object.

		Args:
			scope (mixed, optional): List or view ID. Defaults to None.

		Returns:
			dict: A dictionary of all linked documents.
		"""
		import revitron
		linkedDocuments = dict()
		extension = '.rvt'
		for link in revitron.Filter(scope).byCategory('RVT Links').noTypes().getElements():
			linkType = revitron.Parameter(link, 'Type').getValueString()
			if linkType.endswith(extension):
				linkType = linkType[:-len(extension)]
			for openDoc in revitron.APP.Documents:
				if openDoc.IsLinked:
					if openDoc.Title == linkType:
						linkedDocuments[link.Id] = openDoc
		return linkedDocuments


	def getPath(self):
		"""
		Returns the path to the document.

		Returns:
			string: The path
		"""
		return self.doc.PathName
	
	
	def isFamily(self):
		"""
		Checks whether the document is a family.

		Returns:
			boolean: True in case the document is a family
		"""
		try:
			if self.doc.FamilyManager is not None:
				return True
		except:
			pass
		return False
	
	
	@staticmethod
	def isOpen(path):
		"""
		Checks whether a document is open by passing its path.

		Args:
			path (string): The path

		Returns:
			boolean: True in case the document is open
		"""   
		import revitron     
		try:
			for doc in revitron.APP.Documents:
				if path == doc.PathName:
					return True
		except:
			pass
		return False
	
	
class DocumentConfigStorage:
	"""
	The ``DocumentConfigStorage`` allows for easily storing project configuration items.
	
	Getting configuration items::
	   
	   config = revitron.DocumentConfigStorage().get('namespace.item')
	   
	The returned ``config`` item can be a **string**, a **number**, a **list** or a **dictionary**. 
	It is also possible to define a default value in case the item is not defined in the storage::

		from collections import defaultdict
		config = revitron.DocumentConfigStorage().get('namespace.item', defaultdict())
		
	Setting configuration items works as follows::
	
		revitron.DocumentConfigStorage().set('namespace.item', value)
	
	"""
	
	def __init__(self):
		"""
		Inits a new ``DocumentConfigStorage`` object.
		"""
		import revitron
		
		self.storageName = 'REVITRON_CONFIG'
		self.info = revitron.DOC.ProjectInformation
		raw = revitron._(self.info).get(self.storageName)
		self.storage = dict()
		
		if raw:
			self.storage = json.loads(raw)
		
			
	def get(self, key, default=None):
		"""
		Returns storage entry for a given key.

		Example::

			config = revitron.DocumentConfigStorage()
			item = config.get('name')
			
		Args:
			key (string): The key of the storage entry
			default (mixed, optional): An optional default value. Defaults to None.

		Returns:
			mixed: The stored value 
		"""
		return self.storage.get(key, default)
	
	
	def set(self, key, data):
		"""
		Updates or creates a config storage entry.

		Example::
		
			config = revitron.DocumentConfigStorage()
			config.set('name', value)
			
		Args:
			key (string): The storage entry key
			data (mixed): The value of the entry
		"""
		import revitron
		
		self.storage[key] = data
		# Remove empty items.
		self.storage = dict((k, v) for k, v in self.storage.iteritems() if v)
		raw = json.dumps(self.storage, sort_keys=True, ensure_ascii=False)
		t = revitron.Transaction()
		revitron._(self.info).set(self.storageName, raw)
		t.commit()
