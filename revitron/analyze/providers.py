"""
This submodule is a collection of data providers that are used to extract information from a given Revit model.
"""

from abc import ABCMeta, abstractmethod, abstractproperty


class AbstractDataProvider(object):
	"""
	The abstract data provider. A data provider must implement a ``run()`` method
	that actually defines the extracted data.
	"""

	__metaclass__ = ABCMeta

	def __init__(self, config):
		"""
		Init a new data provider with a given configuration.

		Args:
			config (dict): The data provider configuration
		"""
		self.config = config

	def _filterElements(self):
		"""
		Filter elements in the target model by applying all filters that
		are defined in the configuration.

		Returns:
			list: The list of filtered elements
		"""
		import revitron
		filters = self.config.get('filters')
		fltr = revitron.Filter()
		for f in filters:
			evaluator = getattr(revitron.Filter, f.get('rule'))
			fltr = evaluator(fltr, *f.get('args'))
		return fltr.noTypes().getElements()

	@abstractmethod
	def run(self):
		"""
		The abstract method for data extraction. This method
		must be implemented by a data provider.
		"""
		pass

	@property
	def dataType(self):
		"""
		The data type property defines the data type of the provided data in the database.

		Returns:
			string: The data type that is used for provided values in the database
		"""
		return 'integer'

	@abstractproperty
	def valueType(self):
		"""
		The value type property defines the type of the provided data in the database, such as
		length, area, volume or count.

		Returns:
			string: The value type
		"""
		pass


class ElementCountProvider(AbstractDataProvider):
	"""
	This data provider returns the count of filtered elements after applying all
	filters that are defined in the provider configuration.
	"""

	def run(self):
		"""
		Run the data provider and return the number of filtered elements.

		Returns:
			integer: The number of filtered elements
		"""
		return len(self._filterElements())

	@property
	def valueType(self):
		"""
		The value type for the counter is ``count``.

		Returns:
			string: The value type
		"""
		return 'num'


class ElementAreaProvider(AbstractDataProvider):
	"""
	This data provider returns the accumulated area of a set of elements after applying all
	filters that are defined in the provider configuration.
	"""

	def run(self):
		"""
		Apply filters and accumulate the area of the filtered elements.

		Returns:
			integer: The accumulated area
		"""
		from revitron import _
		area = 0.0
		for element in self._filterElements():
			area += _(element).get('Area')
		return round(area, 3)

	@property
	def dataType(self):
		"""
		The area data type is ``real``.

		Returns:
			string: The data type
		"""
		return 'real'

	@property
	def valueType(self):
		"""
		The value type is ``area``.

		Returns:
			string: The value type
		"""
		return 'are'


class ElementVolumeProvider(AbstractDataProvider):
	"""
	This data provider returns the accumulated area of a set of elements after applying all
	filters that are defined in the provider configuration.
	"""

	def run(self):
		"""
		Apply filters and accumulate the volume of the filtered elements.

		Returns:
			integer: The accumulated area
		"""
		from revitron import _
		volume = 0.0
		for element in self._filterElements():
			volume += _(element).get('Volume')
		return round(volume, 3)

	@property
	def dataType(self):
		"""
		The volume data type is ``real``.

		Returns:
			string: The data type
		"""
		return 'real'

	@property
	def valueType(self):
		"""
		The value type is ``volume``.

		Returns:
			string: The value type
		"""
		return 'vol'


class ElementLengthProvider(AbstractDataProvider):
	"""
	This data provider returns the accumulated length of a set of elements after applying all
	filters that are defined in the provider configuration.
	"""

	def run(self):
		"""
		Apply filters and accumulate the length of the filtered elements.

		Returns:
			integer: The accumulated length
		"""
		from revitron import _
		length = 0.0
		for element in self._filterElements():
			length += _(element).get('Length')
		return round(length, 3)

	@property
	def dataType(self):
		"""
		The length data type is ``real``.

		Returns:
			string: The data type
		"""
		return 'real'

	@property
	def valueType(self):
		"""
		The value type is ``length``.

		Returns:
			string: The value type
		"""
		return 'len'


class WarningCountProvider(AbstractDataProvider):
	"""
	This data provider returns the number of warnings in a model.
	"""

	def run(self):
		"""
		Get the number of warnings.

		Returns:
			integer: The number of warnings
		"""
		import revitron
		return len(revitron.DOC.GetWarnings())

	@property
	def valueType(self):
		"""
		The value type is ``count``.

		Returns:
			string: The value type
		"""
		return 'num'
