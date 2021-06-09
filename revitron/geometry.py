"""
The Geometry submodule and its ``Geometry`` class contain useful helpers for handling 
**Revit** element geometries. Note that it is possible to use the ``_()`` shorthand to get 
the geometry of an element as follows::

	geometry = _(element).getGeometry()

The full syntax without using the shorthand can also be used::

	geometry = revitron.Geometry(element)
"""


class Geometry:
	"""
	A collection of useful methods for handling Revit element geometries.
	"""

	def __init__(self, element):
		"""
		Inits a new Geometry instance.

		Args:
			element (object): A Revit element
		"""
		import revitron
		self._geometry = element.get_Geometry(revitron.DB.Options())


	def getFaces(self):
		"""
		Get a list of all faces of a given element.

		Returns:
			list: A list of face objects
		"""
		faces = []
		for solid in self.getSolids():
			for face in solid.Faces:
				faces.append(face)
		return faces


	def getSolids(self):
		"""
		Get a list of all solids of a given element.

		Returns:
			list: A list of solid objects
		"""
		solids = []
		for geo in self._geometry:
			for item in geo.GetInstanceGeometry():
				try:
					if item.Volume:
						solids.append(item)
				except:
					pass
		return solids