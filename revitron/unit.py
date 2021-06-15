"""
The unit module and its **Unit** class provide little helper for handling units in Revit. 
"""


class Unit:
	"""
	The Unit class contains helpers for handling units.
	"""

	
	@staticmethod
	def convertToInternalUnit(value, unit):
		"""
		Convert a given value from a given unit into Revit's internal unit.

		Args:
			value (mixed): A number or string value. Strings are converted to floats automatically.
			unit (object): A Revit ``DisplayUnitType`` or ``ForgeTypeId`` object

		Returns:
			number: The converted number
		"""
		import revitron
		value = float(value)
		return revitron.DB.UnitUtils.ConvertToInternalUnits(value, unit)