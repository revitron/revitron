"""
This submodule provides convenient wrappers for the interaction with elements.
Getting parameter values or other information can be quite complicated using the plain **Revit API**. 
Methods like ``revitron.Element(element).get(parameter)`` simplify that process. 

Note:

	Note that there is also the ``_()`` shortcut function available to be even more efficient 
	in getting properties of Revit elements. `More here <revitron.html#function>`_ ...

For example getting a parameter value or even a bounding box object works as follows::

	form revitron import _
	value = _(element).get('parameter')
	boundingBox = _(element).getBbox()
	
Or setting parameter values::

	_(element).set('parameter', value)
	
"""
import numbers


class Element:
	"""
	A wrapper class for Revit elements. 
	
	Example::
	
		value = revitron.Element(element).get('parameter')
		
	Or in short::
	
		from revitron import _
		value = _(element).get('parameter')
	"""

	def __init__(self, element):
		"""
		Inits a new element instance.

		Args:
			element (object): The Revit element or an element ID
		"""
		import revitron
		if isinstance(element, revitron.DB.ElementId):
			self._element = revitron.DOC.GetElement(element)
		elif isinstance(element, numbers.Integral):
			self._element = revitron.DOC.GetElement(revitron.DB.ElementId(element))
		else:
			self._element = element

	def __getattr__(self, name):
		"""
		Define default method to be returned on attribute errors.
		
		Since this is a generic element class that is extended by other more specialized classes such 
		as the ``Room`` class, a default method along with an error message is returned when accidently 
		calling a special methods that only exists in one of the derived classes on an element of another class.

		Args:
			name (string): The name of the called method

		Returns:
			method: An empty method
		"""
		from revitron import Log

		def method(*args):
			Log().warning(
			    'Failed to call unkown method "{}" for element of class "{}"'.format(
			        name, self.getClassName()
			    )
			)

		return method

	@property
	def element(self):
		"""
		The actual Revit element. 

		Returns:
			object: The Revit element object
		"""
		return self._element

	def delete(self):
		"""
		Delete an element.
		
		Example::
		
			_(element).delete()
		"""
		import revitron
		revitron.DOC.Delete(self._element.Id)

	def getBbox(self):
		"""
		Returns a bounding box for the element.

		Returns:
			object: The bounding box or false on error
		"""
		import revitron
		try:
			return revitron.BoundingBox(self._element)
		except:
			return False

	def getCategoryName(self):
		"""
		Returns the category name of the element.

		Returns:
			string: The category name
		"""
		try:
			return self._element.Category.Name
		except:
			return ''

	def getClassName(self):
		"""
		Returns the class name of the element.

		Returns:
			string: The class name
		"""
		return self._element.__class__.__name__

	def getFamilyName(self):
		"""
		Returns the family name of the element.

		Returns:
			string: The family name
		"""
		return self.getParameter('Family').getValueString()

	def getFamilyAndTypeName(self):
		"""
		Returns the family name of the element.

		Returns:
			string: The family name
		"""
		return self.getParameter('Family and Type').getValueString()

	def get(self, paramName):
		"""
		Returns a parameter value.
		
		Example::
		
			value = _(element).get('name')
			
		Args:
			paramName (string): The name of the parameter

		Returns:
			mixed: The parameter value
		"""
		import revitron
		return revitron.Parameter(self._element, paramName).get()

	def getDependent(self, filterClass=None):
		"""
		Returns a list of dependent elements.

		Args:
			filterClass (class, optional): An optional class to filter the list of dependent elements by. Defaults to None.

		Returns:
			list: The list with the dependent Revit elements.
		"""
		import revitron
		from revitron import _
		# The GetDependentElements() method doesn't exist in older Revit API versions.
		# Therefore it is required to fallback to a more compatible way of getting those dependent elements
		# in case an execption is raised.
		# The fallback solution basically tries to get the list of affected IDs when trying to delete
		# the actual parent element within a transaction that will be cancelled.
		try:
			fltr = None
			if filterClass:
				fltr = revitron.DB.ElementClassFilter(filterClass)
			dependentIds = self._element.GetDependentElements(fltr)
		except:
			sub = revitron.Transaction()
			ids = revitron.DOC.Delete(self._element.Id)
			sub.rollback()
			if filterClass:
				dependentIds = revitron.Filter(ids).byClass(filterClass
				                                            ).noTypes().getElementIds()
			else:
				dependentIds = revitron.Filter(ids).noTypes().getElementIds()
		dependent = []
		for eId in dependentIds:
			dependent.append(_(eId).element)
		return dependent

	def getFromType(self, paramName):
		"""
		Returns a parameter value of the element type.
		
		Example::
		
			value = _(element).getFromType('name')
			
		Args:
			paramName (string): The name of the parameter

		Returns:
			mixed: The parameter value
		"""
		from revitron import _
		try:
			return _(self._element.GetTypeId()).get(paramName)
		except:
			return ''

	def getGeometry(self):
		"""
		Return the Revitron Geometry instance for this element.

		Returns:
			object: A Revitron Geometry object
		"""
		import revitron
		return revitron.Geometry(self._element)

	def getParameter(self, paramName):
		"""
		Returns a parameter object.

		Args:
			paramName (string): The name of the parameter

		Returns:
			object: The parameter object
		"""
		import revitron
		return revitron.Parameter(self._element, paramName)

	def getTags(self):
		"""
		Get possibly existing tags of an element.

		Returns:
			list: A list of Revit tag objects depending on the element class
		"""
		import revitron

		category = self.getParameter('Category').getValueString()

		switcher = {'Rooms': revitron.DB.SpatialElementTag}

		return self.getDependent(switcher.get(category))

	def isNotOwned(self):
		"""
		Checks whether an element is owned by another user.

		Returns:
			boolean: True if the element is not owned by another user.
		"""
		import revitron
		return str(
		    revitron.DB.WorksharingUtils.
		    GetCheckoutStatus(revitron.DOC, self._element.Id)
		) != 'OwnedByOtherUser'

	def isType(self):
		"""
		Checks whether an element is a type or not. 

		Returns:
			bool: True if element is a type.
		"""
		className = self.getClassName()
		return (
		    className.endswith('Type') or className.endswith('Symbol')
		    or className == 'MEPBuildingConstruction' or className == 'SiteLocation'
		    or className == 'BrowserOrganization' or className == 'TilePattern'
		)

	def set(self, paramName, value, paramType='Text'):
		"""
		Sets a parameter value.

		Example::
		
			_(element).set('name', 'value', 'type')
		
		Some possible parameter types are: 
			
		- ``Text``
		- ``Integer`` 
		- ``Number``
		- ``Length``
		- ``Angle`` 
		- ``Material``
		- ``YesNo``
		- ``MultilineText``
		- ``FamilyType``
			 
		You can find a list of all types `here <https://www.revitapidocs.com/2019/f38d847e-207f-b59a-3bd6-ebea80d5be63.htm>`_.

		Args:
			paramName (string): The parameter name
			value (mixed): The value
			paramType (string, optional): The parameter type. Defaults to 'Text'.

		Returns:
			object: The element instance
		"""
		import revitron
		revitron.Parameter(self._element, paramName).set(value, paramType)
		return self