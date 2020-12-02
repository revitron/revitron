""" 
This submodule contains a wrapper classes for **Revit** room elements.
"""
import Autodesk
from revitron.element import Element


class Room(Element):
	"""
	A wrapper class for room elements.
	"""
	
	def getBboxCenter(self, inRoomOnly = False):
		"""
		Get the center point of a room's bounding box.

		Args:
			inRoomOnly (boolean): Optionally only return a point in case the bounding box center is actually in the room

		Returns:
			object: A Revit point object
		"""
		import revitron
		
		room = self.element
		bbox = self.getBbox()
		
		point = bbox.getCenterPoint()

		if room.IsPointInRoom(point) or not inRoomOnly:
			return point
	
	  
	def getBoundary(self):
		"""
		Get the boundary of a given room. 
		
		Returns:
			list: A list of boundary segment curves
		"""
		import revitron
		room = self.element
		options = revitron.DB.SpatialElementBoundaryOptions()
		boundaryLocation = revitron.DB.AreaVolumeSettings.\
						   GetAreaVolumeSettings(revitron.DOC).\
						   GetSpatialElementBoundaryLocation(revitron.DB.SpatialElementType.Room)   
		options.SpatialElementBoundaryLocation = boundaryLocation
		curveList = []
		for boundaryList in room.GetBoundarySegments(options):
			for boundary in boundaryList:
				curveList.append(boundary.GetCurve())
		return curveList


	def getBoundaryPoints(self):
		"""
		Get all points along a room boundary.

		Returns:
			list: A list of points
		"""
		import revitron
		room = self.element
		curveList = self.getBoundary()
		points = []
		for curve in curveList:
			# If the curve is an arc, first tessellate the curve 
			# and extend the points array with the polyline points.
			if 'Arc' in str(curve.GetType()):
				points.extend(curve.Tessellate())
			else:
				points.append(curve.GetEndPoint(0))
		return points


	def getBoundaryInsetPoints(self, inset = 0.1):
		"""
		Get all points along an inset of the room boundary. 
		
		The inset is useful in cases where a point has to be used as a location for a tag 
		and therefore should be located direktly on the boundary but a little bit more inside instead 
		to avoid issues and warnings.

		Args:
			inset (float, optional): The inset. Defaults to 0.1.

		Returns:
			list: The list of points
		"""
		import revitron
		room = self.element
		options = revitron.DB.SpatialElementBoundaryOptions()
		boundaryLocation = revitron.DB.AreaVolumeSettings.\
						   GetAreaVolumeSettings(revitron.DOC).\
						   GetSpatialElementBoundaryLocation(revitron.DB.SpatialElementType.Room)
		options.SpatialElementBoundaryLocation = boundaryLocation
		curves = dict()
		points = []

		try:            
			for boundaryList in room.GetBoundarySegments(options):
				cl = revitron.DB.CurveLoop()
				for x in boundaryList:
					cl.Append(x.GetCurve())
				curves[cl.GetExactLength()] = cl

			curveLengths = curves.keys()
			longest = curves[max(curveLengths)]

			tempInset = revitron.DB.CurveLoop.CreateViaOffset(longest, inset, revitron.DB.XYZ(0,0,1))
			if tempInset.GetExactLength() > max(curveLengths):
				tempInset = revitron.DB.CurveLoop.CreateViaOffset(longest, inset, revitron.DB.XYZ(0,0,-1))

			for c in tempInset:
				points.append(c.GetEndPoint(0))

		except:
			# If CurveLoop throws exception, get points from boundary.
			points = self.getPoints()
			pass

		return points
	 

	def getPointClosest(self, point, inset = 0.1):
		"""
		Get the point on a room boundary that is the closest to a given point.

		Args:
			point (object): A Revit XYZ object
			inset (float, optional): An optional room boundary inset. Defaults to 0.1.

		Returns:
			object: A Revit XYZ object
		"""
		closestDistance = False
		for p in self.getBoundaryInsetPoints(inset):
			d = p.DistanceTo(point)
			if not closestDistance:
				closestDistance = d
				closestPoint = p
			else:
				if d < closestDistance:
					closestDistance = d
					closestPoint = p
		return closestPoint
		
	
	def getPointTopLeft(self, inset = 0.1):
		"""
		Get the most top left point of a room boundary.

		Args:
			inset (float, optional): An optional room boundary inset. Defaults to 0.1.

		Returns:
			object: A Revit XYZ object
		"""
		import revitron
		bbox = self.getBbox()
		bboxTopLeft = revitron.DB.XYZ(bbox.Min.X, bbox.Max.Y, bbox.Min.Z)
		return self.getPointClosest(bboxTopLeft, inset)   
	 
	 
	def getPointTopRight(self, inset = 0.1):
		"""
		Get the most top right point of a room boundary.

		Args:
			inset (float, optional): An optional room boundary inset. Defaults to 0.1.

		Returns:
			object: A Revit XYZ object
		"""
		import revitron
		bbox = self.getBbox()
		bboxTopLeft = revitron.DB.XYZ(bbox.Max.X, bbox.Max.Y, bbox.Min.Z)
		return self.getPointClosest(bboxTopLeft, inset)   
	
	
	def getPointBottomLeft(self, inset = 0.1):
		"""
		Get the most bottom left point of a room boundary.

		Args:
			inset (float, optional): An optional room boundary inset. Defaults to 0.1.

		Returns:
			object: A Revit XYZ object
		"""
		import revitron
		bbox = self.getBbox()
		bboxTopLeft = revitron.DB.XYZ(bbox.Min.X, bbox.Min.Y, bbox.Min.Z)
		return self.getPointClosest(bboxTopLeft, inset)   
	
	
	def getPointBottomRight(self, inset = 0.1):
		"""
		Get the most bottom right point of a room boundary.

		Args:
			inset (float, optional): An optional room boundary inset. Defaults to 0.1.

		Returns:
			object: A Revit XYZ object
		"""
		import revitron
		bbox = self.getBbox()
		bboxTopLeft = revitron.DB.XYZ(bbox.Max.X, bbox.Min.Y, bbox.Min.Z)
		return self.getPointClosest(bboxTopLeft, inset)


	def getPointGrid(self, size = 5, inset = 0.05):
		"""
		Generates a point grid based on a given size within the room boundary. 

		Args:
			size (float, optional): The maximum grid field size. Defaults to 5.00.
			inset (float, optional): The inset of the room boundary. Defaults to 0.05.

		Returns:
			list: A list of Revit XYZ objects
		"""
		import revitron
		import math

		points = []
		bbox = self.getBbox()

		if isinstance(bbox, revitron.BoundingBox):
			
			tlp = revitron.DB.XYZ(bbox.Min.X, bbox.Max.Y, bbox.Min.Z)
			brp = revitron.DB.XYZ(bbox.Max.X, bbox.Min.Y, bbox.Min.Z)
			lengthX = bbox.Max.X - bbox.Min.X
			lengthY = bbox.Max.Y - bbox.Min.Y
			fieldSizeX = ((lengthX - (2 * inset)) / math.ceil(lengthX / size))
			fieldSizeY = ((lengthY - (2 * inset)) / math.ceil(lengthY / size))
			
			_x = tlp.X + inset
			while (_x < brp.X):
				_y = brp.Y + inset
				while (_y < tlp.Y):
					p = revitron.DB.XYZ(_x, _y, tlp.Z)
					if self.element.IsPointInRoom(p):
						points.append(p)
					_y = _y + fieldSizeY
				_x = _x + fieldSizeX
			
			return points


	def traceHeight(self, view3D, elementFilter = None, gridSize = 5, inset = 0.05):
		"""
		Traces the room heights and returns an object containing the min/max bottom and min/max top points.

		Args:
			view3D (object): A Revit 3D view.
			elementFilter (mixed, optional): Either a list of Revit elements or a Revit ElementClassFilter. Defaults to None.
			gridSize (float, optional): The maximum grid field size for the raytracing. Defaults to 5.00.
			inset (float, optional): The inset of the room boundary. Defaults to 0.05.

		Returns:
			object: An object containing a top and bottom property. 
					Both properties are nested objects containing an Min and a Max value.
		"""
		import revitron
		points = self.getPointGrid(gridSize, inset) + self.getBoundaryInsetPoints(inset)
		# Set z to the lower quarter.
		z = self.getBboxCenter().Z / 2

		intersectionsTop = []
		intersectionsBottom = []

		for point in points:
			point = revitron.DB.XYZ(point.X, point.Y, z)
			raytracer = revitron.Raytracer(point, view3D)
			intersectionsTop.append(raytracer.findIntersection(revitron.DB.XYZ(0,0,1), elementFilter).Z)
			intersectionsBottom.append(raytracer.findIntersection(revitron.DB.XYZ(0,0,-1), elementFilter).Z)

		top = revitron.AttrDict({
			'min': min(intersectionsTop),
			'max': max(intersectionsTop)
		})

		bottom = revitron.AttrDict({
			'min': min(intersectionsBottom),
			'max': max(intersectionsBottom)
		})

		return revitron.AttrDict({
			'top': top,
			'bottom': bottom
		})
		
