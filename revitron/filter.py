""" 
The ``filter`` submodule is one of the most essential one within the **Revitron** package. 
Its main purpose is taking over the heavy lifting of filtering elements in the **Revit** database and
complementing the standard **Revit API** ``FilteredElementCollector`` class with 
the ability to filter collections by parameter values::

	elements = (
	    revitron.Filter
	    .byStringEquals('param', 'value')
	    .noTypes()
	    .getElements()
	)
	
Note that you can **invert** a filter by providing a the third argument for a string filter as follows::

	elements = (
	    revitron.Filter
	    .byStringEquals('param', 'value', True)
	    .noTypes()
	    .getElements()
	)

.. note:: In order to filter elements in another model instead of the active one, it is possible to change 
	the document context using the ``with`` statement.

The document context can be changed as follows::

	with revitron.Document(anyOtherDoc):
	    fltr = revitron.Filter().noTypes()
	    elements = fltr.getElements()
"""
import re
from System.Collections.Generic import List


class Filter:
	""" 
	A filter class based on the ``FilteredElementCollector`` class.
	"""
	
	def __init__(self, scope = None):
		"""
		Inits a new Filter instance.

		Args:
			scope (Element ID or list of elements, optional): The optional scope. It can be either a view Id or a list of elements. Defaults to None.
		"""
		import revitron
		
		self.scope = scope
		if scope:
			if type(scope) == list:
				elementIds = []
				for element in scope:
					elementIds.append(element.Id)
				scope = List[revitron.DB.ElementId](elementIds) 
			self.collector = revitron.DB.FilteredElementCollector(revitron.DOC, scope) 
		else:   
			self.collector = revitron.DB.FilteredElementCollector(revitron.DOC)
	

	def all(self):
		"""
		This is just a helper filter that doesn't modify the collection at all to allow for 
		getting all elements of an instance without actually applying any filter before. 

		Returns:
			object: The Filter instance
		"""
		import revitron
		db = revitron.DB
		f = db.LogicalOrFilter(db.ElementIsElementTypeFilter(False), db.ElementIsElementTypeFilter(True))

		self.collector = self.collector.WherePasses(f)
		return self


	def applyFilter(self, filterRule, paramName, value, evaluator, invert = False):
		"""
		Applies a filter.

		Args:
			filterRule (class): A Revit filter rule class
			paramName (string): The parameter name
			value (number): the value
			evaluator (object): The evaluator object
			invert (boolean): Inverts the filter
		"""
		import revitron
		filters = []

		# Since a visible parameter name could match multiple built-in parameters,
		# we get a list of value providers. 
		# While iterating that list, the parameter filter is applied each time 
		# to a fresh element collector that will be later merged or intersected with the others. 
		for valueProvider in revitron.ParameterValueProviders(paramName).get():
			try:
				rule = filterRule(valueProvider, evaluator, value, True)
				_filter = Filter()
				_filter.collector = revitron.DB.FilteredElementCollector(revitron.DOC, self.getElementIds())
				_filter.parameterFilter(rule, invert) 
				filters.append(_filter)
			except:
				pass
		
		if len(filters):
			self.collector = filters[0].collector
			if len(filters) > 1:
				for i in range(1, len(filters)):
					if not invert:
						self.collector.UnionWith(filters[i].collector)
					else:
						self.collector.IntersectWith(filters[i].collector)


	def byIntersection(self, element):
		"""
		Reduces the set of elements to the ones that are intersecting a given element.

		Args:
			element (objetc): A Revit element

		Returns:
			object: The Filter instance
		"""
		import revitron
		self.collector = self.collector.WherePasses(revitron.DB.ElementIntersectsElementFilter(element))
		return self


	def byRegex(self, paramName, regex, invert = False):
		"""
		Filters a collection by a given regex. 

		Args:
			paramName (string): The name of the parameter to be matched. 
			regex (string): The regex. 
			invert (bool, optional): Inverts the filter. Defaults to False.

		Returns:
			object: The Filter instance
		"""
		import revitron
		
		passed = []
		failed = []

		for element in self.getElements():
			value = revitron.Parameter(element, paramName).getString()
			if not value:
				value = revitron.Parameter(element, paramName).getValueString()
			if value:
				if re.search(regex, value, re.IGNORECASE):
					passed.append(element)
				else:
					failed.append(element)

		if not invert:
			elements = passed
		else:
			elements = failed

		if elements:
			self.collector = Filter(elements).collector
		
		return self


	def byCategory(self, name):
		"""
		Filters the collection by a category name or a built-in category name.
		
		Note that there are basically three valid types that can be used as the filter argument. 
		The first two use the name of a built-in category (with or without the ``OST_`` prefix)::

			fltr = revitron.Filter().byCategory('Walls')
			fltr = revitron.Filter().byCategory('OST_Walls')

		The third type uses a `natural <https://docs.google.com/spreadsheets/d/1uNa77XYLjeN-1c63gsX6C5D5Pvn_3ZB4B0QMgPeloTw/edit#gid=1549586957>`_ 
		category name to find a corresponding built-in category to filter, here ``OST_BeamAnalyticalTags``::

			fltr = revitron.Filter().byCategory('Analytical Beam Tags')

		Args:
			name (string): A category or built-in category name

		Returns:
			object: The Filter instance
		"""
		import revitron
		try:
			self.collector = self.collector.OfCategory(revitron.BuiltInCategory(name).get())
		except:
			pass
		return self
	
	
	def byClass(self, cls):
		"""
		Filters the collection by class.

		Args:
			cls (class): A class to filter the elements

		Returns:
			object: The Filter instance
		"""
		self.collector = self.collector.OfClass(cls)
		return self
	
	
	def byNumberIsGreater(self, paramName, value, invert = False):
		"""
		Filters the collection by parameter values greater than a given number.

		Example::
			
			fltr = revitron.Filter()
			ids = fltr.byNumberIsGreater('Area', 5).noTypes().getElementIds()

		Args:
			paramName (string): The parameter name
			value (number): The numeric value to compare to
			invert (boolean): Inverts the filter

		Returns:
			object: The collector
		"""
		import revitron
		value = float(value)
		self.applyFilter(
			revitron.DB.FilterDoubleRule,
			paramName,
			value,
			revitron.DB.FilterNumericGreater(),
			invert)
		return self


	def byNumberIsGreaterOrEqual(self, paramName, value, invert = False):
		"""
		Filters the collection by parameter values greater than or equal to a given number.

		Example::
			
			fltr = revitron.Filter()
			fltr = fltr.byNumberIsGreaterOrEqual('Area', 5).noTypes()
			ids = fltr.getElementIds()

		Args:
			paramName (string): The parameter name
			value (number): The numeric value to compare to
			invert (boolean): Inverts the filter

		Returns:
			object: The collector
		"""
		import revitron
		value = float(value)
		self.applyFilter(
			revitron.DB.FilterDoubleRule,
			paramName,
			value,
			revitron.DB.FilterNumericGreaterOrEqual(),
			invert)
		return self


	def byNumberIsEqual(self, paramName, value, invert = False):
		"""
		Filters the collection by parameter values equal to a given number.

		Example::
			
			fltr = revitron.Filter()
			ids = fltr.byNumberIsEqual('Area', 5).noTypes().getElementIds()

		Args:
			paramName (string): The parameter name
			value (number): The numeric value to compare to
			invert (boolean): Inverts the filter

		Returns:
			object: The collector
		"""
		import revitron
		value = float(value)
		self.applyFilter(
			revitron.DB.FilterDoubleRule,
			paramName,
			value,
			revitron.DB.FilterNumericEquals(),
			invert)
		return self


	def byNumberIsLess(self, paramName, value, invert = False):
		"""
		Filters the collection by parameter values smaller than a given number.

		Example::
			
			fltr = revitron.Filter()
			ids = fltr.byNumberIsLess('Area', 5).noTypes().getElementIds()

		Args:
			paramName (string): The parameter name
			value (number): The numeric value to compare to
			invert (boolean): Inverts the filter

		Returns:
			object: The collector
		"""
		import revitron
		value = float(value)
		self.applyFilter(
			revitron.DB.FilterDoubleRule,
			paramName,
			value,
			revitron.DB.FilterNumericLess(),
			invert)
		return self


	def byNumberIsLessOrEqual(self, paramName, value, invert = False):
		"""
		Filters the collection by parameter values smaller than or equal to a given number.

		Example::
			
			fltr = revitron.Filter()
			ids = fltr.byNumberIsLessOrEqual('Area', 5).noTypes().getElementIds()

		Args:
			paramName (string): The parameter name
			value (number): The numeric value to compare to
			invert (boolean): Inverts the filter

		Returns:
			object: The collector
		"""
		import revitron
		value = float(value)
		self.applyFilter(
			revitron.DB.FilterDoubleRule,
			paramName,
			value,
			revitron.DB.FilterNumericLessOrEqual(),
			invert)
		return self


	def byOneInCsv(self, evaluatorName, paramName, csv, invert = False):
		"""
		Filters the collection by testing whether a string contains at lease one ot the items in a CSV list.

		This method is the base method for the ``byStringContainsOneInCsv`` and ``byStringEqualsOneInCsv``
		methods.

		.. note:: that by setting ``invert`` to ``True``, all elements that match one of the items will be 
			removed from the collection.

		Args:
			evaluatorName (method): The filter method to be used to filter
			paramName (string): The name of the parameter 
			csv (string): A comma separated list of items 
			invert (bool, optional): Inverts the filter. Defaults to False.

		Returns:
			object: The Filter instance
		"""
		import revitron

		evaluator = getattr(Filter, evaluatorName)

		filters = []
		for item in csv.split(','):
			_filter = Filter()
			try:
				_filter.collector = revitron.DB.FilteredElementCollector(revitron.DOC, self.getElementIds())
			except:
				_filter.collector = revitron.DB.FilteredElementCollector(revitron.DOC)
			_filter = evaluator(_filter, paramName, item.strip(), invert)
			filters.append(_filter)

		if len(filters):
			self.collector = filters[0].collector
			if len(filters) > 1:
				for i in range(1, len(filters)):
					if not invert:
						self.collector.UnionWith(filters[i].collector)
					else:
						self.collector.IntersectWith(filters[i].collector)
		return self


	def byStringContains(self, paramName, value, invert = False):
		"""
		Filters the collection by a string contained in a parameter.

		Example::
			
			fltr = revitron.Filter()
			fltr = fltr.byStringContains('param', 'value').noTypes()
			ids = fltr.getElementIds()

		Args:
			paramName (string): The parameter name
			value (string): The searched string
			invert (boolean): Inverts the filter

		Returns:
			object: The collector
		"""
		import revitron
		self.applyFilter(
			revitron.DB.FilterStringRule,
			paramName, 
			value, 
			revitron.DB.FilterStringContains(), 
			invert)
		return self 
	
	
	def byStringContainsOneInCsv(self, paramName, csv, invert = False):
		"""
		Filters the collection by testing whether a string contains at lease one ot the items in a CSV list.

		.. note:: that by setting ``invert`` to ``True``, all elements that match one of the items will be 
			removed from the collection.

		Example::

			fltr = revitron.Filter()
			fltr = fltr.byStringContainsOneInCsv('Family', 'some, words', False)
			fltr = fltr.noTypes()
			elements = fltr.getElements()

		Args:
			paramName (string): The name of the parameter 
			csv (string): A comma separated list of items 
			invert (bool, optional): Inverts the filter. Defaults to False.

		Returns:
			object: The Filter instance
		"""
		return self.byOneInCsv('byStringContains', paramName, csv, invert)

	
	def byStringEquals(self, paramName, value, invert = False):
		"""
		Filters the collection by a string that equals a parameter value.

		Example::
			
			fltr = revitron.Filter()
			ids = fltr.byStringEquals('param', 'value').noTypes().getElementIds()

		Args:
			paramName (string): The parameter name
			value (string): The searched string
			invert (boolean): Inverts the filter

		Returns:
			object: The collector
		"""
		import revitron
		self.applyFilter(
			revitron.DB.FilterStringRule,
			paramName, 
			value, 
			revitron.DB.FilterStringEquals(), 
			invert
		)
		return self
	

	def byStringEqualsOneInCsv(self, paramName, csv, invert = False):
		"""
		Filters the collection by testing whether a string equals at lease one ot the items in a CSV list.

		.. note:: that by setting ``invert`` to ``True``, all elements that match one of the items will be 
			removed from the collection.

		Example::

			fltr = revitron.Filter()
			fltr = fltr.byStringEqualsOneInCsv('Family', 'some, words', False)
			fltr = fltr.noTypes()
			elements = fltr.getElements()

		Args:
			paramName (string): The name of the parameter 
			csv (string): A comma separated list of items 
			invert (bool, optional): Inverts the filter. Defaults to False.

		Returns:
			object: The Filter instance
		"""
		return self.byOneInCsv('byStringEquals', paramName, csv, invert)

	
	def byStringBeginsWith(self, paramName, value, invert = False):
		"""
		Filters the collection by a string at the beginning of a parameter value.

		Example::
			
			fltr = revitron.Filter()
			fltr = fltr.byStringBeginsWith('param', 'value').noTypes()
			ids = fltr.getElementIds()

		Args:
			paramName (string): The parameter name
			value (string): The searched string
			invert (boolean): Inverts the filter

		Returns:
			object: The collector
		"""
		import revitron
		self.applyFilter(
			revitron.DB.FilterStringRule,
			paramName, 
			value, 
			revitron.DB.FilterStringBeginsWith(), 
			invert
		)
		return self 
	
	
	def byStringEndsWith(self, paramName, value, invert = False):
		"""
		Filters the collection by a string at the end of a parameter.

		Args:
			paramName (string): The parameter name
			value (string): The searched string
			invert (boolean): Inverts the filter

		Returns:
			object: The collector
		"""
		import revitron
		self.applyFilter(
			revitron.DB.FilterStringRule,
			paramName, 
			value, 
			revitron.DB.FilterStringEndsWith(), 
			invert
		)
		return self 
	
	
	def getElements(self):
		"""
		Get the collection as elements.

		Returns:
			list: The list of excluded elements
		"""
		try:
			return self.collector.ToElements()
		except:
			self.all()
			return self.collector.ToElements()
	
	
	def getElementIds(self):
		"""
		Get the collection as element IDs.

		Returns:
			list: The list of excluded element IDs
		"""
		try:
			return self.collector.ToElementIds()
		except:
			self.all()
			return self.collector.ToElementIds()


	def noTypes(self):
		"""
		Removes all types from collection.

		Returns:
			object: The Filter instance
		"""
		self.collector = self.collector.WhereElementIsNotElementType()
		return self


	def onlyTypes(self):
		"""
		Reduce to collection to types only.

		Returns:
			object: The Filter instance
		"""
		self.collector = self.collector.WhereElementIsElementType()
		return self


	def parameterFilter(self, rule, invert = False):
		"""
		Applies a parameter filter.

		Args:
			rule (object): The filter rule object
			invert (boolean): Inverts the filter
		"""  
		import revitron
		parameterFilter = revitron.DB.ElementParameterFilter(rule, invert)
		self.collector = self.collector.WherePasses(parameterFilter)
