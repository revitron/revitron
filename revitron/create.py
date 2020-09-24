"""
The ``create`` submodule and its ``Create`` class contain helpful shorthand methods to create 
**Revit** elements. For example a centered room tag can be created as follows::

	tag = revitron.Create.roomTag(self.element, self.getBboxCenter())
	
Note that some methods are also directly accessible in element classes such as ``Room``::

	tag = _(room).tagCenter()
"""	

class Create:
	"""
	A collection of shorthand methods to create **Revit** elements.
	"""
	
	@staticmethod
	def roomTag(room, location, typeId = False, viewId = False):
		"""
		Creates a room tag for a given room element.

		Args:
			room (object): A Revit room element
			location (object): A Revit point object
			typeId (ElementId, optional): An optional Id of a tag type. Defaults to False.
			viewId (ElementId, optional): An optional Id of a view. Defaults to the currently active view.

		Returns:
			object: The Revit ``RoomTag`` element
		"""
		import revitron
		from revitron import _ 

		if not viewId:
			viewId = revitron.ACTIVEVIEW.Id

		clsName = _(room).getClassName()

		if clsName != 'Room':
			revitron.Log().error('Can\'t tag an element of class "{}" with a room tag.'.format(clsName))
			return False
		
		location = revitron.DB.UV(location.X, location.Y)
		tag = revitron.DOC.Create.NewRoomTag(revitron.DB.LinkElementId(room.Id), location, viewId)

		if typeId:
			if tag.IsValidType(typeId):
				tag.ChangeTypeId(typeId)
		
		return tag        
