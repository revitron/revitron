#-*- coding: UTF-8 -*-
""" 
Besides the ``element`` and the ``filter`` submodules, 
this submodule is one of the most elementary submodules of the **Revitron** package.
It contains all classes related to parameters, built-in parameters and value providers.
"""
import re
import numbers


class Parameter:
	"""
	A wrapper class for interacting with element parameters. 
	
	Note:
	
		In most cases it is not required to actually create a **Parameter** class 
		instance in order to access paramter values of a given element. 
		The fastest way of getting or setting parameter values is using the ``_(element).get('parameter')``
		shortcut `function <revitron.html#function>`_ or an instance of the :doc:`revitron.element` class.
	"""

	def __init__(self, element, name):
		"""
		Init a new parameter instance.

		Getting a parameter by name visible to the user::

			value = revitron.Parameter(element, 'parameterName').get()

		Or the short version::

			value = _(element).get('parameterName')

		To be **language independent** it is possible to get a parameter value by its **built-in** parameter name
		like for example the view scale::

			scale = _(view).get('VIEW_SCALE')

		Args:
			element (object): Revit element
			name (string): The parameter name or the name of a built-Iin parameter
		"""
		self.element = element
		self.name = name
		self.parameter = element.LookupParameter(name)

		if not self.exists():
			try:
				import revitron
				self.parameter = element.get_Parameter(
				    getattr(revitron.DB.BuiltInParameter, name)
				)
			except:
				pass

	def exists(self):
		"""
		Checks if a parameter exists.

		Returns:
			boolean: True if existing
		"""
		return (self.parameter != None)

	def hasValue(self):
		"""
		Checks if parameter has a value.

		Returns:
			boolean: True if the parameter has a value
		"""
		if self.exists():
			return (self.parameter.HasValue)

	def get(self):
		"""
		Return the parameter value.

		Note:
		
			As mentioned above, the fastest way of getting a parameter value is to use the
			`get <revitron.element.html#revitron.element.Element.get>`_ method 
			of the ``revitron.Element`` class.

		Returns:
			mixed: The value
		"""
		if self.exists():
			storageType = str(self.parameter.StorageType)
		else:
			storageType = 'String'

		switcher = {
		    'String': self.getString,
		    'ValueString': self.getValueString,
		    'Integer': self.getInteger,
		    'Double': self.getDouble,
		    'ElementId': self.getElementId
		}

		value = switcher.get(storageType)
		return value()

	def getString(self):
		"""
		Return the parameter value as string.

		Returns:
			string: The value
		"""
		if self.hasValue():
			return self.parameter.AsString()
		return ''

	def getValueString(self):
		"""
		Return the parameter value as value string.

		Returns:
			string: The value
		"""
		if self.hasValue():
			return self.parameter.AsValueString()
		return ''

	def getInteger(self):
		"""
		Return the parameter value as integer.

		Returns:
			integer: The value
		"""
		if self.hasValue():
			return self.parameter.AsInteger()
		return 0

	def getDouble(self):
		"""
		Return the parameter value as double.

		Returns:
			double: The value
		"""
		if self.hasValue():
			return self.parameter.AsDouble()
		return 0.0

	def getElementId(self):
		"""
		Return the parameter value as ElementId.

		Returns:
			object: The value
		"""
		if self.hasValue():
			return self.parameter.AsElementId()
		return 0

	def set(self, value, paramType=False):
		"""
		Set a parameter value for an element. The parameter will be automatically created if not existing.
		The parameter type can be specified. If not type is given, it will be determined automatically in 
		case of text, integer or float values.

		Note:
		
			As mentioned above, the fastest way of setting a parameter value is to use the
			`set <revitron.element.html#revitron.element.Element.set>`_ method 
			of the ``revitron.Element`` class.
			
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
			value (string): The value
			paramType (string, optional): The `parameter type <https://www.revitapidocs.com/2019/f38d847e-207f-b59a-3bd6-ebea80d5be63.htm>`_
		"""
		if not self.name:
			return False
		if not paramType:
			paramType = 'Text'
			if isinstance(value, numbers.Integral):
				paramType = 'Integer'
			if isinstance(value, float):
				paramType = 'Number'
		if self.parameter == None:
			from revitron import _
			if ParameterUtils.bind(
			    self.element.Category.Name,
			    self.name,
			    paramType,
			    _(self.element).isType()
			):
				self.parameter = self.element.LookupParameter(self.name)
			else:
				print('Error setting value of parameter "{}"'.format(self.name))
				return False
		if not self.parameter.IsReadOnly:
			self.parameter.Set(value)

	@property
	def definitionType(self):
		"""
		The defenition parameter type.

		Returns:
			string: The definition parameter type name 
		"""
		return self.parameter.Definition.ParameterType

	@property
	def unit(self):
		"""
		The displayed unit type of a parameter. 

		Note that since Revit 2021 the preferred return value is of type ``ForgeTypeId``. 

		Returns:
			mixed: The displayed unit type (ForgeTypeId or DisplayUnitType)
		"""
		try:
			return self.parameter.GetUnitTypeId()
		except:
			return self.parameter.DisplayUnitType


class ParameterUtils:
	"""
	A collection of static parameter utilities.
	"""

	@staticmethod
	def bind(category, paramName, paramType='Text', typeBinding=False):
		"""
		Bind a new parameter to a category.

		Args:
			category (string): The built-in category 
			paramName (string): The parameter name
			paramType (string): The parameter type (see `here <https://www.revitapidocs.com/2019/f38d847e-207f-b59a-3bd6-ebea80d5be63.htm>`_)
								Defaults to "Text".
			typeBinding (bool): Bind parameter to type instead of instance. Defaults to False.

		Returns:
			boolean: Returns True on success and False on error.
		"""
		import revitron

		paramFile = revitron.APP.OpenSharedParameterFile()

		if paramFile is None:
			print('Please define a shared parameters file.')
			return False

		definition = None

		# Try to get an existing parameter definition with the given name.
		for group in paramFile.Groups:
			definition = group.Definitions.get_Item(paramName)
			if definition:
				break

		group = None

		# If the definition hasn't been created yet, create it in the REVITRON group.
		if not definition:
			group = paramFile.Groups.get_Item('REVITRON')
			if not group:
				group = paramFile.Groups.Create('REVITRON')
			pt = getattr(revitron.DB.ParameterType, paramType)
			ExternalDefinitionCreationOptions = revitron.DB.ExternalDefinitionCreationOptions(
			    paramName, pt
			)
			definition = group.Definitions.Create(ExternalDefinitionCreationOptions)

		# Try to get the parameter binding for the definition.
		binding = revitron.DOC.ParameterBindings[definition]

		# Add the given category to the categories list as the initial item
		# and try to access currently bound categories to add them as well.
		# In case the given category is already among the bound categories,
		# stop the further execution and return False.
		# In case the category is not bound yet, remove the binding from the parameter
		# binding map.
		categories = [revitron.Category(category).get()]
		try:
			for _cat in binding.Categories:
				categories.append(_cat)
				if _cat.Name == category:
					return False
			revitron.DOC.ParameterBindings.Remove(definition)
		except:
			pass

		# Create a new category set and add all categories, the given and the previously bound ones.
		categorySet = revitron.APP.Create.NewCategorySet()
		for _cat in categories:
			categorySet.Insert(_cat)

		# Create the binding.
		if typeBinding:
			binding = revitron.APP.Create.NewTypeBinding(categorySet)
		else:
			binding = revitron.APP.Create.NewInstanceBinding(categorySet)

		revitron.DOC.ParameterBindings.Insert(definition, binding)

		return True

	@staticmethod
	def getStorageType(name):
		"""
		Get the storage type of a parameter definition by name.

		Args:
			name (string): The parameter name

		Returns:
			string: The storage type
		"""
		from revitron import DOC
		# Try first project and shared parameters.
		definition = ParameterUtils._findProjectParameterDefinition(name)
		if not definition:
			definition = ParameterUtils._findSharedParameterDefinition(name)
		if definition:
			storageType = ParameterUtils._convertParameterTypeToStorageType(
			    definition.ParameterType.ToString()
			)
			if storageType:
				return storageType
		try:
			# Try built-in parameters.
			return str(DOC.TypeOfStorage[ParameterUtils._findBuiltInParameter(name)])
		except:
			# Fall back to very slow search in all elements.
			return ParameterUtils._findStorageTypeInElements(name)

	@staticmethod
	def _findProjectParameterDefinition(name):
		"""
		Find a custom parameter in a document.

		Args:
			name (string): The parameter name

		Returns:
			object: The parameter object
		"""
		from revitron import DOC
		it = DOC.ParameterBindings.ForwardIterator()
		while it.MoveNext():
			if it.Key.Name == name:
				return it.Key
		return None

	@staticmethod
	def _findBuiltInParameter(name):
		"""
		Find a built-in parameter by name.

		Args:
			name (string): The parameter name

		Returns:
			object: The built-in parameter
		"""
		from revitron import DB
		for item in dir(DB.BuiltInParameter):
			try:
				bip = getattr(DB.BuiltInParameter, item)
				if DB.LabelUtils.GetLabelFor(bip) == name:
					return bip
			except:
				pass
		return None

	@staticmethod
	def _findSharedParameterDefinition(name):
		"""
		Find a shared parameter definition by name.

		Args:
			name (string): The parameter name

		Returns:
			object: The shared parameter definition
		"""
		from revitron import Filter, DB
		sharedParameters = Filter().byClass(DB.SharedParameterElement).getElements()
		for parameter in sharedParameters:
			definition = parameter.GetDefinition()
			if name == definition.Name:
				return definition
		return None

	@staticmethod
	def _convertParameterTypeToStorageType(paramType):
		"""
		Convert parameter type to storage type in a map of known types. 
		Note that this map may be incomplete and therefore ``None`` may be returned.

		Args:
			paramType (string): The name of the parameter type to be converted

		Returns:
			string: The storage type
		"""
		typeMap = {
		    'Angle': 'Double',
		    'Area': 'Double',
		    'Currency': 'Double',
		    'ElectricalPotential': 'Double',
		    'ElectricalPowerDensity': 'Double',
		    'HVACAirflow': 'Double',
		    'HVACAirflowDensity': 'Double',
		    'HVACAreaDividedByCoolingLoad': 'Double',
		    'HVACAreaDividedByHeatingLoad': 'Double',
		    'HVACCoefficientOfHeatTransfer': 'Double',
		    'HVACCoolingLoad': 'Double',
		    'HVACCoolingLoadDividedByArea': 'Double',
		    'HVACFactor': 'Double',
		    'HVACHeatGain': 'Double',
		    'HVACHeatingLoad': 'Double',
		    'HVACHeatingLoadDividedByArea': 'Double',
		    'HVACRoughness': 'Double',
		    'HVACTemperature': 'Double',
		    'HVACThermalMass': 'Double',
		    'HVACThermalResistance': 'Double',
		    'Image': 'ElementId',
		    'Integer': 'Integer',
		    'Invalid': 'ElementId',
		    'Length': 'Double',
		    'Material': 'ElementId',
		    'MultilineText': 'String',
		    'Number': 'Double',
		    'PipingDensity': 'Double',
		    'PipingPressure': 'Double',
		    'PipingRoughness': 'Double',
		    'PipingTemperature': 'Double',
		    'PipingViscosity': 'Double',
		    'ReinforcementCover': 'Double',
		    'Text': 'String',
		    'URL': 'String',
		    'Volume': 'Double',
		    'YesNo': 'Integer'
		}
		if paramType in typeMap:
			return typeMap[paramType]

	@staticmethod
	def _findStorageTypeInElements(paramName):
		"""
		Find a storage type of a parameter by iterating a list of all elements in 
		a document and testing if an element contains a parameter with a given name.

		Note:

			This is a very slow way of finding the correct storage type and 
			should only be used in edge cases where there is no other way of finding out
			the storage type of a parameter!

		Args:
			paramName (string): The name of the parameter

		Returns:
			string: The storage type
		"""
		from revitron import Filter
		for element in Filter().getElements():
			parameter = element.LookupParameter(paramName)
			if parameter:
				return parameter.StorageType.ToString()


class ParameterNameList:
	"""
	A helper class for listing all parameter names in the active document. 
	"""

	def __init__(self):
		"""
		Inits a new ParameterNameList instance including all parameter names in the document.
		"""
		import revitron

		self.parameters = []

		for name in BuiltInParameterNameMap().map:
			self.parameters.append(name)

		for param in revitron.Filter().byClass(revitron.DB.SharedParameterElement
		                                       ).getElements():
			self.parameters.append(param.GetDefinition().Name)

		for param in revitron.Filter().byClass(revitron.DB.ParameterElement
		                                       ).getElements():
			self.parameters.append(param.GetDefinition().Name)

		self.parameters = sorted(list(set(self.parameters)))

	def get(self):
		"""
		Returns the parameter list.

		Returns:
			list: The list with all parameters in the document.
		"""
		return self.parameters


class ParameterValueProviders:
	""" 
	A wrapper for parameter value providers used for filtering elements.
	"""

	def __init__(self, name):
		"""
		Inits a new ParameterValueProviders instance by name. Such an instance consists of a list
		of value providers matching a parameters with a name visible to the user.
		Note that this list can have more than one value provider, since a parameter name possible matches 
		multiple built-in parameters.

		Args:
			name (string): Name
		"""
		import revitron
		self.providers = []
		paramIds = []
		it = revitron.DOC.ParameterBindings.ForwardIterator()
		while it.MoveNext():
			if it.Key.Name == name:
				paramIds.append(it.Key.Id)
		if not paramIds:
			try:
				paramIds = BuiltInParameterNameMap().get(name)
			except:
				pass
		for paramId in paramIds:
			self.providers.append(revitron.DB.ParameterValueProvider(paramId))

	def get(self):
		"""
		Returns the list of value providers.

		Returns:
			list: The list of value providers
		"""
		return self.providers


class BuiltInParameterNameMap:
	""" 
	A helper class for mapping lists of built-in parameter names to their representation visible to the user.
	"""

	def __init__(self):
		"""
		Inits a new BuiltInParameterNameMap instance. The map is a dictionary where the key
		is a parameter name that is visible to the user and the value is a list of built-in parameters 
		represented by that name.
		"""
		import revitron

		self.map = dict()
		for item in dir(revitron.DB.BuiltInParameter):
			try:
				bip = getattr(revitron.DB.BuiltInParameter, item)
				name = revitron.DB.LabelUtils.GetLabelFor(bip)
				if name not in self.map:
					self.map[name] = []
				self.map[name].append(revitron.DB.ElementId(int(bip)))
			except:
				pass

	def get(self, name):
		"""
		Return the list of matching built-in parameters for a given name.

		Args:
			name (string): The parameter name visible to the user

		Returns:
			list: The list of built-in parameter ids
		"""
		return self.map[name]


class ParameterTemplate:
	"""
	Create a string based on a parameter template where parameter names are wrapped in :code:`{...}` and get substituted with their value::
	
		This sheet has the number {Sheet Number}

	It is also possible to get parameter values from the project information instead by wrapping the parameter names 
	in :code:`{%...%}` instead::

		This sheet of the project {%Project Name%} has the number {Sheet Number}

	"""

	def __init__(self, element, template, sanitize=True):
		"""
		Inits a new ParameterTemplate instance.

		Args:
			element (object): A Revit element
			template (string): A template string
			sanitize (bool, optional): Optionally sanitize the returned string. Defaults to True.
		"""
		import revitron

		self.projectInfo = revitron.DOC.ProjectInformation
		self.element = element
		self.template = template
		self.sanitize = sanitize

	def reCallback(self, match):
		"""
		The callback function used by the ``get()`` method.

		Args:
			match (object): The regex match object

		Returns:
			string: The processed string
		"""
		import revitron

		parameter = match.group(1)

		try:
			match = re.match('^%(.+?)%$', parameter)
			parameter = match.group(1)
			string = str(revitron.Element(self.projectInfo).get(parameter))
		except:
			string = str(revitron.Element(self.element).get(parameter))

		if self.sanitize:
			string = revitron.String.sanitize(string)

		return string

	def render(self):
		"""
		Returns the rendered template string.

		Returns:
			string: The rendered string
		"""
		return re.sub('\{(.+?)\}', self.reCallback, self.template)
