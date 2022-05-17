"""
The Geometry submodule and its ``Geometry`` class contain useful helpers for handling 
**Revit** element geometries. Note that it is possible to use the ``_()`` shorthand to get 
the geometry of an element as follows::

	geometry = _(element).getGeometry()

The full syntax without using the shorthand can also be used::

	geometry = revitron.Geometry(element)
"""
import math


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
			try:
				for face in solid.Faces:
					faces.append(face)
			except:
				pass
		return faces

	def getSolids(self):
		"""
		Get a list of all solids of a given element.

		Returns:
			list: A list of solid objects
		"""
		solids = []
		try:
			for geo in self._geometry:
				for item in geo.GetInstanceGeometry():
					try:
						if item.Volume:
							solids.append(item)
					except:
						pass
		except:
			pass
		return solids


class GeometryUtils:
	"""
	The GeometryUtils class contains a collection of static utility methods for dealing
	with geometry related tasks.
	"""

	@staticmethod
	def getAngle(center, p1, p2):
		"""
		Calculate the angle in degrees between two vectors that share a common center and 
		are defined two endpoints.

		Args:
			center (XYZ): A Revit XYZ object that defines the common start point
			p1 (XYZ): The endpoint of the first vector
			p2 (XYZ): The endpoint of the second vector

		Returns:
			float: The calculated angle in degrees
		"""
		vector1 = p1 - center
		vector2 = p2 - center
		dotProd = vector1.DotProduct(vector2)
		magnitude1 = p1.DistanceTo(center)
		magnitude2 = p2.DistanceTo(center)
		return math.degrees(math.acos(dotProd / (magnitude1 * magnitude2)))

	@staticmethod
	def getBoundaryPoints(boundary):
		"""
		Get a list of points from a given boundary that is usually returned by 
		methods such as ``GetBoundarySegments``.

		Args:
			boundary (list): A list of boundary segment lists

		Returns:
			list: The list of points that define a boundary polygon
		"""
		boundaryPoints = []
		for segmentsList in boundary:
			for segment in segmentsList:
				curve = segment.GetCurve()
				start = curve.GetEndPoint(0)
				boundaryPoints.append(start)
		return boundaryPoints

	@staticmethod
	def polygonContainsPoint2D(polygonPoints, point):
		"""
		Check whether a given polygon that is planar to a horizontal surface
		contains a given point. Note that both, the polygon as well as the point must share common Z values.

		Args:
			polygonPoints (list): A list of points
			point (XYZ): The point that is tested

		Returns:
			boolean: True, if the polygon contains the point
		"""
		for p in polygonPoints:
			if round(p.Z, 3) != round(point.Z, 3):
				return False
		prev = polygonPoints[len(polygonPoints) - 1]
		accumulated = 0
		for n in range(0, len(polygonPoints)):
			_p = polygonPoints[n]
			angle = GeometryUtils.getAngle(point, prev, _p)
			prev = _p
			accumulated = accumulated + angle
		return accumulated > 180