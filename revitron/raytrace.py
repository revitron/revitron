"""
The raytrace submodule contains helper methods for easily raytracing intersections or similar. 
"""
from System.Collections.Generic import List


class Raytracer:
	"""
	The Raytracer class. 
	"""

	def __init__(self, point, view3D):
		"""
		Inits a raytracer instance.

		Args:
			point (object): A Revit XYZ object used as the base point for the raytracing. 
			view3D (object): A Revit 3D view. 
		"""
		self.point = point
		self.view3D = view3D


	def findIntersection(self, direction, elementFilter = None):
		"""
		Finds and returns an intersection point of a ray in a given direction based on an optional element filter. 

		Args:
			direction (object): A Revit XYZ vector.
			elementFilter (mixed, optional): Either a list of Revit elements or a Revit ElementClassFilter. Defaults to None.

		Returns:
			object: A Revit XYZ object or False on errors.
		"""
		import revitron 
		DB = revitron.DB

		if isinstance(elementFilter, List):
			intersector = DB.ReferenceIntersector(elementFilter, 
												  DB.FindReferenceTarget.Face, 
												  self.view3D)
		elif isinstance(elementFilter, DB.ElementClassFilter):
			intersector = DB.ReferenceIntersector(DB.ElementClassFilter(DB.CeilingAndFloor), 
												  DB.FindReferenceTarget.Face, 
												  self.view3D)
		else:
			intersector = DB.ReferenceIntersector(self.view3D)

		try:
			context = intersector.FindNearest(self.point, direction)
			return context.GetReference().GlobalPoint
		except:
			return False

