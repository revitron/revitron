"""
The ``create`` submodule and its ``Create`` class contain helpful shorthand methods to create 
**Revit** elements and families programatically. For example a centered room tag can be created as follows::

	tag = revitron.Create.roomTag(self.element, self.getBboxCenter())
	
Note that some methods are also directly accessible in element classes such as ``Room``::

	tag = _(room).tagCenter()
"""	
import os


class Create:
	"""
	A collection of shorthand methods to create **Revit** elements.
	"""
	
	@staticmethod
	def familyDoc(template, savePath):
		"""
		Creates a new familiy document from a given template and saves it.add()

		Args:
			template (string): The template name without the ``.rft`` extension. 
			savePath (string): The full path of the family file to be saved as.

		Returns:
			object: A reference to the newly created family document.
		"""
		import revitron
		try:
			if os.path.isfile(savePath):
				os.remove(savePath)
		except:
			pass
		templatesDir = revitron.APP.FamilyTemplatePath
		templatePath = os.path.join(templatesDir, template + '.rft')
		famDoc = revitron.APP.NewFamilyDocument(templatePath)
		opt = revitron.DB.SaveAsOptions()
		opt.OverwriteExistingFile = True
		famDoc.SaveAs(savePath, opt)
		return famDoc


	@staticmethod
	def familyExtrusion(familyDoc, curveArrayArray, sketchPlane, height = 10.0, location = False, isSolid = True):
		"""
		Creates an extrusion within a given family document.

		Args:
			familyDoc (object): A reference to a family document.
			curveArrayArray (object): A Revit API ``CurveArrArray``.
			sketchPlane (object): A Revit API ``SketchPlane``.
			height (float, optional): The extrusion height. Defaults to 10.0.
			location (object, optional): A Revit API ``XYZ`` point object. Defaults to False.
			isSolid (bool, optional): Soild (True) or void (False). Defaults to True.

		Returns:
			object: The extrusion element.
		"""
		import revitron
		if not location:
			location = revitron.DB.XYZ(0, 0, 0)
		if revitron.Document(familyDoc).isFamily():
			extrusion = familyDoc.FamilyCreate.NewExtrusion(isSolid, curveArrayArray, sketchPlane, height)
			revitron.DB.ElementTransformUtils.MoveElement(familyDoc, extrusion.Id, location)
			return extrusion


	@staticmethod
	def familyInstance(familySymbolId, location, structuralType = False):
		"""
		Creates a new family instance.

		Example::

			transaction = revitron.Transaction()
			instance = revitron.Create.familyInstance(familySymbolId, location)
			transaction.commit()

		Args:
			familySymbolId (object): A Revit API family symbol ID.
			location (object): A Revit API ``XYZ`` point.
			structuralType (object, optional): A Revit API structural type of False for ``NonStructural``. Defaults to False.

		Returns:
			object: The family instance.
		"""
		import revitron
		from revitron import _ 
		if not structuralType:
			structuralType = revitron.DB.Structure.StructuralType.NonStructural
		familySymbol = _(familySymbolId).element
		if not familySymbol.IsActive:
			familySymbol.Activate()
		return revitron.DOC.Create.NewFamilyInstance(location, familySymbol, structuralType)


	@staticmethod
	def GridLineLinear(start, end, name):
		"""
		Create a new linear grid line.

		Args:
			start (object): A Revit ``XYZ`` element
			end (object): A Revit ``XYZ`` element
			name (string): The grid name

		Returns:
			object: A Revit grid element
		"""
		import revitron
		line = revitron.DB.Line.CreateBound(start, end)
		try:
			grid = revitron.DB.Grid.Create(revitron.DOC, line)
			grid.Name = name
			return grid
		except:
			revitron.Log().error('Can\'t create grid line "{}"'.format(name))
			return None


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
			viewId = revitron.ACTIVE_VIEW.Id

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


	@staticmethod
	def view3D():
		"""
		Create a new 3D view.

		Returns:
			object: A Revit 3D view element
		"""
		import revitron 
		view3DType = None

		for viewFamilyType in revitron.Filter().byClass(revitron.DB.ViewFamilyType).onlyTypes().getElements():
			if viewFamilyType.FamilyName == '3D View':
				view3DType = viewFamilyType
				break
		
		return revitron.DB.View3D.CreateIsometric(revitron.DOC, view3DType.Id)	

