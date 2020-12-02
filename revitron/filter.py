""" 
The ``filter`` submodule is one of the most essential one within the **Revitron** package. 
Its main purpose is taking over the heavy lifting of filtering elements in the **Revit** database and
complementing the standard **Revit API** ``FilteredElementCollector`` class with 
the ability to filter collections by parameter values::

	filter = revitron.Filter
	ids = filter().byStringEquals('param', 'value').noTypes().getElementIds()
	
Note that you can **invert** a filter by providing a the third argument for a string filter as follows::

	filter = revitron.Filter
	ids = filter().byStringEquals('param', 'value', True).noTypes().getElementIds()
	
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


	def applyParameterFilter(self, rule, invert = False):
		"""
		Applies a parameter filter.

		Args:
			rule (object): The filter rule object
			invert (boolean): Inverts the filter
		"""  
		import revitron
			 
		parameterFilter = revitron.DB.ElementParameterFilter(rule, invert)
		self.collector = self.collector.WherePasses(parameterFilter)


	def applyStringFilter(self, paramName, value, evaluator, invert = False):
		"""
		Applies a string filter.

		Args:
			paramName (string): The parameter name
			value (mixed): the value
			evaluator (object): The FilterStringRuleEvaluator
			invert (boolean): Inverts the filter
		"""   
		import revitron
		
		filters = []
	
		# Since a visible parameter name could match multiple built-in parameters,
		# we get a list of value providers. 
		# While iterating that list, the parameter filter is applied each time 
		# to a fresh element collector that will be later merged or intersected with the others. 
		for valueProvider in revitron.ParameterValueProviders(paramName).get():
			rule = revitron.DB.FilterStringRule(valueProvider, evaluator, value, True)
			_filter = Filter()
			# Try to get elements from the collector as base for the fresh collector.
			# In case there was never a filter applied before, getting elements will raise an exception
			# and new Filter() instance is created with the same scope.
			try:
				_filter.collector = revitron.DB.FilteredElementCollector(revitron.DOC, self.collector.ToElementIds())
			except:
				_filter.collector = Filter(self.scope).collector
			_filter.applyParameterFilter(rule, invert) 
			filters.append(_filter)
		
		self.collector = filters[0].collector
		
		if len(filters) > 1:
			for i in range(1, len(filters)):
				if not invert:
					self.collector.UnionWith(filters[i].collector)
				else:
					self.collector.IntersectWith(filters[i].collector)
				

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
		Filters the collection by a category name - not a built-in category.

		Args:
			name (string): The category name

		Returns:
			object: The Filter instance
		"""   
		import revitron
			 
		self.collector = self.collector.OfCategory(revitron.Category(name).getBic())
		return self
	
	
	def byClass(self, cls):
		"""
		Filters the collection by class.

		Returns:
			object: The Filter instance
		"""        
		self.collector = self.collector.OfClass(cls)
		return self
	
	
	def byStringContains(self, paramName, value, invert = False):
		"""
		Filters the collection by a string contained in a parameter.

		Example::
			
			filter = revitron.Filter
			ids = filter().byStringContains('param', 'value').noTypes().getElementIds()

		Args:
			paramName (string): The parameter name
			value (string): The searched string
			invert (boolean): Inverts the filter

		Returns:
			object: The collector
		"""
		import revitron
		
		self.applyStringFilter(paramName, value, revitron.DB.FilterStringContains(), invert)
		return self 
	
	
	def byStringEquals(self, paramName, value, invert = False):
		"""
		Filters the collection by a string that equals a parameter value.

		Example::
			
			filter = revitron.Filter
			ids = filter().byStringEquals('param', 'value').noTypes().getElementIds()

		Args:
			paramName (string): The parameter name
			value (string): The searched string
			invert (boolean): Inverts the filter

		Returns:
			object: The collector
		"""
		import revitron
		
		self.applyStringFilter(paramName, value, revitron.DB.FilterStringEquals(), invert)
		return self    
	
	
	def byStringBeginsWith(self, paramName, value, invert = False):
		"""
		Filters the collection by a string at the beginning of a parameter value.

		Args:
			paramName (string): The parameter name
			value (string): The searched string
			invert (boolean): Inverts the filter

		Returns:
			object: The collector
		"""
		import revitron
		
		self.applyStringFilter(paramName, value, revitron.DB.FilterStringBeginsWith(), invert)
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
		
		self.applyStringFilter(paramName, value, revitron.DB.FilterStringEndsWith(), invert)
		return self 
	
	
	def onlyTypes(self):
		"""
		Reduce to collection to types only.

		Returns:
			object: The Filter instance
		"""
		self.collector = self.collector.WhereElementIsElementType()
		return self
	
	
	def noTypes(self):
		"""
		Removes all types from collection.

		Returns:
			object: The Filter instance
		"""
		self.collector = self.collector.WhereElementIsNotElementType()
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
