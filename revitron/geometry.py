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
	def getAbsoluteAngleXY(base, endpoint):
		"""
		Get the absolute angle between 0 and 360 degrees of a vector counter clockwise relative to the X-axis.

		Args:
			base (XYZ): The base point that represents 0,0 of the coordinate system
			endpoint (XYZ): The endpoint of the line starting from the basepoint that represents the vector in question

		Returns:
			float: The absolute angle between 0 and 360 degrees
		"""
		from revitron import DB
		vector = endpoint - base
		angle = math.degrees(vector.AngleTo(DB.XYZ(1, 0, vector.Z)))
		if vector.Y < 0:
			angle = 360 - angle
		return angle

	@staticmethod
	def getAngleXY(base, reference, endpoint):
		"""
		Get the angle from a vector to a reference. Note that the result returns positiv as well as negative angles
		depending on the relative location of the reference vector.

		Args:
			base (XYZ): The base point that represents 0,0 of the coordinate system
			reference (XYZ): The endpoint of the reference line starting from the basepoint
			endpoint (XYZ): The endpoint of the line starting from the basepoint that represents the vector in question

		Returns:
			float: The angle
		"""
		alpha = GeometryUtils.getAbsoluteAngleXY(base, endpoint)
		beta = GeometryUtils.getAbsoluteAngleXY(base, reference)
		angle = beta - alpha
		if angle > 180:
			angle = angle - 360
		if angle < -180:
			angle = angle + 360
		return angle

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
	def polygonContainsPointXY(polygonPoints, point):
		"""
		Check whether a given polygon that is planar to a horizontal surface
		contains a given point. Note that both, the polygon as well as the point must share common Z values.

		The algorithm accumulates all angles (positive and negative) between neighboring lines that span from a given point to
		all vertices of the polygon. In case the accumulated absolute value equals 360, the point is located inside the polygon.

		Args:
			polygonPoints (list): A list of points
			point (XYZ): The point that is tested

		Returns:
			boolean: True, if the polygon contains the point
		"""
		for p in polygonPoints:
			if round(p.Z, 3) != round(point.Z, 3):
				return False
		accumulated = 0
		prev = -1
		for n in range(0, len(polygonPoints)):
			delta = GeometryUtils.getAngleXY(point, polygonPoints[prev], polygonPoints[n])
			accumulated += delta
			prev = n
		accumulated = round(abs(accumulated))
		return accumulated == 360
