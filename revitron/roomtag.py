""" 
A simple helper module for creating room tags.
"""


class RoomTag:
	"""
	This class contains methods to create room tags in given locations.
	"""
	
	@staticmethod
	def create(room, location, tagTypeId = False, viewId = False):
		"""
		Create a room tag in a given location.

		All existing room tags will be removed before automatically.

		Args:
			location (object): A Revit location point object.
			tagTypeId (ElementId, optional): A Revit element Id of a custom tag type. Defaults to False.
			viewId (ElementId, optional): A Revit element Id a view. Defaults to False.

		Returns:
			object: A Revit ``RoomTag`` element 
		"""
		import revitron
		from revitron import _
		
		if not viewId:
			viewId = revitron.ACTIVE_VIEW.Id
			
		for tagId in _(room).getTags():
			_(tagId).delete()
			
		return revitron.Create.roomTag(room, location, tagTypeId, viewId)


	@staticmethod
	def center(room, tagTypeId = False, viewId = False):
		"""
		Create a room tag in the bounding box center.
   
		All existing room tags will be removed before automatically.

		Args:
			room (object): A Revit room element.
			tagTypeId (ElementId, optional): A Revit element Id of a custom tag type. Defaults to False.
			viewId (ElementId, optional): A Revit element Id a view. Defaults to False.

		Returns:
			object: A Revit ``RoomTag`` element 
		"""
		from revitron import _
		return RoomTag.create(room, _(room).getBboxCenter(), tagTypeId, viewId)


	@staticmethod
	def topLeft(room, tagTypeId = False, viewId = False):
		"""
		Create a room tag in the top left corner. 
  
		All existing room tags will be removed before automatically.

		Args:
			room (object): A Revit room element.
			tagTypeId (ElementId, optional): A Revit element Id of a custom tag type. Defaults to False.
			viewId (ElementId, optional): A Revit element Id a view. Defaults to False.

		Returns:
			object: A Revit ``RoomTag`` element 
		"""
		from revitron import _
		return RoomTag.create(room, _(room).getPointTopLeft(), tagTypeId, viewId)


	@staticmethod
	def topRight(room, tagTypeId = False, viewId = False):
		"""
		Create a room tag in the top right corner. 
  
		All existing room tags will be removed before automatically.

		Args:
			room (object): A Revit room element.
			tagTypeId (ElementId, optional): A Revit element Id of a custom tag type. Defaults to False.
			viewId (ElementId, optional): A Revit element Id a view. Defaults to False.

		Returns:
			object: A Revit ``RoomTag`` element 
		"""
		from revitron import _
		return RoomTag.create(room, _(room).getPointTopRight(), tagTypeId, viewId)


	@staticmethod
	def bottomLeft(room, tagTypeId = False, viewId = False):
		"""
		Create a room tag in the bottom left corner. 
  
		All existing room tags will be removed before automatically.

		Args:
			room (object): A Revit room element.
			tagTypeId (ElementId, optional): A Revit element Id of a custom tag type. Defaults to False.
			viewId (ElementId, optional): A Revit element Id a view. Defaults to False.

		Returns:
			object: A Revit ``RoomTag`` element 
		"""
		from revitron import _
		return RoomTag.create(room, _(room).getPointBottomLeft(), tagTypeId, viewId)


	@staticmethod
	def bottomRight(room, tagTypeId = False, viewId = False):
		"""
		Create a room tag in the bottom right corner. 
  
		All existing room tags will be removed before automatically.

		Args:
			room (object): A Revit room element.
			tagTypeId (ElementId, optional): A Revit element Id of a custom tag type. Defaults to False.
			viewId (ElementId, optional): A Revit element Id a view. Defaults to False.

		Returns:
			object: A Revit ``RoomTag`` element 
		"""
		from revitron import _
		return RoomTag.create(room, _(room).getPointBottomRight(), tagTypeId, viewId)