""" 
To simplify the interaction with **Revit** categories, the ``category`` 
submodule provides the ``Category`` and ``BuiltInCategory`` classes in order
to access **Revit** category objects as well as builtin categories by name.
"""


class Category:
	"""
	A wrapper class for category objects which can be instantiated by a category name.
	
	You can get the Revit Category class object by providing a name as follows::
	
		category = revitron.Category('name').get()
	"""

	def __init__(self, name):
		"""
		Init a new Category by name.

		Args:
			name (string): The category name
		"""
		import revitron
		for cat in revitron.DOC.Settings.Categories:
			if cat.Name == name:
				self.category = cat
				break

	def get(self):
		"""
		Returns the category object.

		Returns:
			object: The category object
		"""
		return self.category

	def getBic(self):
		"""
		Returns the built-in category for a given category.

		Returns:
			object: The built-in category
		"""
		import revitron
		for item in dir(revitron.DB.BuiltInCategory):
			try:
				bic = getattr(revitron.DB.BuiltInCategory, item)
				if int(bic) == self.category.Id.IntegerValue:
					return bic
			except:
				pass


class BuiltInCategory:
	"""
	A wrapper class for builtin category objects which can be instantiated by name.
	
	You can get the Revit BuitlInCategory class object by providing a name as follows::
	
		bic = revitron.BuiltInCategory('OST_Walls').get()

	For convenience reasons, it is also valid to skip the ``OST_`` prefix and simply do::

		bic = revitron.BuiltInCategory('Walls').get()

	In case you only know the *natural* category name and want to get the BuiltInCategory instead,
	you can also use that one. For example to get the ``OST_BeamAnalyticalTags`` BuiltInCategory, you
	can do simply::

		bic = revitron.BuiltInCategory('Analytical Beam Tags').get()

	A full list of category names can be found `here <https://docs.google.com/spreadsheets/d/1uNa77XYLjeN-1c63gsX6C5D5Pvn_3ZB4B0QMgPeloTw/edit#gid=1549586957>`_.
	"""

	def __init__(self, name):
		"""
		Get the BuiltInCategory by its name, its name without the ``OST_`` prefix 
		or even its natural category name. A full list of category names can be found `here <https://docs.google.com/spreadsheets/d/1uNa77XYLjeN-1c63gsX6C5D5Pvn_3ZB4B0QMgPeloTw/edit#gid=1549586957>`_.

		Example::

			bic = revitron.BuiltInCategory('OST_Walls').get()
			bic = revitron.BuiltInCategory('Walls').get()

		Use the natural name to get for example ``OST_BeamAnalyticalTags``::

			bic = revitron.BuiltInCategory('Analytical Beam Tags').get()

		Args:
			name (name): The name, the name without the ``OST_`` prefix or even the 
				`natural <https://docs.google.com/spreadsheets/d/1uNa77XYLjeN-1c63gsX6C5D5Pvn_3ZB4B0QMgPeloTw/edit#gid=1549586957>`_ category name
		"""
		import revitron
		cat = Category(name)
		self.bic = cat.getBic()
		if not self.bic:
			try:
				name = 'OST_{}'.format(name.replace('OST_', ''))
				self.bic = getattr(revitron.DB.BuiltInCategory, name)
			except:
				pass

	def get(self):
		"""
		Return the BuiltInCategory class.

		Returns:
			class: The BuiltInCategory class
		"""
		return self.bic