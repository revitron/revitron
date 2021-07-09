"""
The Grid submodule contains all classes that are related to **Revit** grids. It helps you
to quickly get filtered lists of grid lines or find closests intersections to given points in
orthogonal grids.
"""


class Grid(object):
	"""
	The ``Grid`` class is the base class for other grid classes such as the ``OrthoGrid`` class. A grid object contains 
	a collection of grid lines. That collection can be filtered when creating a grid instance.

	The following example will create a grid object based on all grid lines with a type name
	that either contains "main" or "sub"::

		grid = revitron.Grid('main, sub')
	
	Alternatively you can create a grid object only including orthogonal grid lines::

		ortho = revitron.OrthoGrid('main, sub')
	"""


	def __init__(self, typeFilterCsv=False):
		"""
		Creates a new ``Grid`` instance. A comma separated string can be passed as an argument to filter 
		the grid elements by their type name.

		Args:
			typeFilterCsv (string, optional): A CSV filter. Defaults to False.
		"""
		self._lines = self._getLines(typeFilterCsv)


	@property
	def lines(self):
		"""
		The dict of grid lines contained in the ``Grid`` object where the grid line name serves as key.

		Returns:
			dict: A dict of Revit grid line elements where the grid name serves as key
		"""
		return self._lines


	def _getLines(self, typeFilterCsv=False):
		"""
		Create the filtered dict of grid lines.

		Args:
			typeFilterCsv (string, optional): A CSV filter. Defaults to False.

		Returns:
			dict: A dict of Revit grid line elements where the grid name serves as key
		"""
		if hasattr(self, '_lines'):
			return self._lines
		import revitron
		fltr = revitron.Filter().byCategory('Grids').noTypes()
		if typeFilterCsv:
			fltr = fltr.byStringContainsOneInCsv('Type', typeFilterCsv)
		lines = dict()
		for line in fltr.getElements():
			try:
				lines[line.Name] = line
			except:
				pass
		return lines


class OrthoGrid(Grid):
	"""
	In contrast to the ``Grid`` class, the ``OrthoGrid`` object only contains grid lines that are orthogonal.

	The following example will create a orthogonal grid object based on all grid lines with a type name
	that either contains "main" or "sub"::

		grid = revitron.OrthoGrid('main, sub')
	"""


	@property
	def lines(self):
		"""
		An object that contains one ``X`` and one ``Y`` property, both dicts containing
		grid line elements where the grid name serves as key. 
		The ``X`` property contains all grid lines that are parallel to the X axis while 
		the ``Y`` one contains all line parallel to the Y axis. 

		Returns:
			object: An object containing orthogonal grid elements split into X and Y direction
		"""
		return self._lines


	def _getLines(self, typeFilterCsv=False):
		"""
		Create an object that contains one ``X`` and one ``Y`` property, both dicts containing
		grid line elements where the grid name serves as key. 
		The ``X`` property contains all grid lines that are parallel to the X axis while 
		the ``Y`` one contains all line parallel to the Y axis. 

		Args:
			typeFilterCsv (string, optional): A CSV filter. Defaults to False.

		Returns:
			object: An object containing orthogonal grid elements split into X and Y direction
		"""
		if hasattr(self, '_lines'):
			return self._lines
		import revitron
		x = dict()
		y = dict()
		lines = super(OrthoGrid, self)._getLines(typeFilterCsv).values()
		for line in lines:
			try:
				p0 = line.Curve.GetEndPoint(0)
				p1 = line.Curve.GetEndPoint(1)
				if round(p0.X, 3) == round(p1.X, 3):
					y[line.Name] = line
				if round(p0.Y, 3) == round(p1.Y, 3):
					x[line.Name] = line
			except:
				pass
		return revitron.AttrDict({'X': x, 'Y': y})


	def _getLinesByPosition(self):
		"""
		Create an object that contains one ``X`` and one ``Y`` property, both dicts containing
		grid line elements where the **position** of the grid line in orthogonal direction serves as key. 
		The ``X`` property contains all grid lines that are parallel to the X axis while 
		the ``Y`` one contains all line parallel to the Y axis. 
		In case of a grid line parallel to the X axis, its Y position serves as key and vice versa.

		Returns:
			object: An object containing orthogonal grid elements split into X and Y direction
		"""
		if not hasattr(self, '_linesByPosition'):
			import revitron
			x = dict()
			y = dict()
			for line in self._lines.X.values():
				p0 = line.Curve.GetEndPoint(0)
				x[round(p0.Y, 3)] = line
			for line in self._lines.Y.values():
				p0 = line.Curve.GetEndPoint(0)
				y[round(p0.X, 3)] = line
			self._linesByPosition = revitron.AttrDict({'X': x, 'Y': y})
		return self._linesByPosition


	def closestIntersectionToPointTopLeft(self, point):
		"""
		Find the grid intersection that is closest to a given point on the top left side.

		Args:
			point (object): A Revit ``XYZ`` object

		Returns:
			object: A :class:`OrthoGridIntersection` object
		"""
		top = None
		left = None
		lines = self._getLinesByPosition()
		xLinePosY = sorted(lines.X.keys(), reverse=True)
		yLinePosX = sorted(lines.Y.keys())
		for y in xLinePosY:
			if y < point.Y:
				break
			top = y
		for x in yLinePosX:
			if x > point.X:
				break
			left = x
		if top and left:
			return OrthoGridIntersection(lines.X[top], lines.Y[left])


	def closestIntersectionToPointBottomRight(self, point):
		"""
		Find the grid intersection that is closest to a given point on the bottom right side.

		Args:
			point (object): A Revit ``XYZ`` object

		Returns:
			object: A :class:`OrthoGridIntersection` object
		"""
		bottom = None
		right = None
		lines = self._getLinesByPosition()
		xLinePosY = sorted(lines.X.keys(), reverse=True)
		yLinePosX = sorted(lines.Y.keys())
		for y in xLinePosY:
			bottom = y
			if y < point.Y:
				break
		for x in yLinePosX:
			right = x
			if x > point.X:
				break
		if bottom and right:
			return OrthoGridIntersection(lines.X[bottom], lines.Y[right])


class OrthoGridIntersection:
	"""
	An ``OrthoGridIntersction`` object contains all relevant information about an intersection 
	of two orthogonal grid lines.
	"""

	def __init__(self, gridX, gridY):
		"""
		Create a new intersection object based on two orthogonal grid lines.

		Args:
			gridX (object): A Revit grid element
			gridY (object): A Revit grid element
		"""
		self._gridX = gridX
		self._gridY = gridY
		self._nameX = ''
		self._nameY = ''
		self._X = None
		self._Y = None
		if gridX:
			self._Y = gridX.Curve.GetEndPoint(0).Y
			self._nameX = gridX.Name
		if gridY:
			self._X = gridY.Curve.GetEndPoint(0).X
			self._nameY = gridY.Name


	@property
	def gridX(self):
		"""
		The Revit grid element that is parallel to the **X** axis.

		Returns:
			object: A Revit grid element
		"""
		return self._gridX


	@property
	def gridY(self):
		"""
		The Revit grid element that is parallel to the **Y** axis.

		Returns:
			object: A Revit grid element
		"""
		return self._gridY


	@property
	def nameX(self):
		"""
		The name of the grid element that is parallel to the **X** axis.

		Returns:
			string: The name of the grid
		"""
		return self._nameX


	@property
	def nameY(self):
		"""
		The name of the grid element that is parallel to the **Y** axis.

		Returns:
			string: The name of the grid
		"""
		return self._nameY


	@property
	def X(self):
		"""
		The **X** coordinate of the intersection on plan.

		Returns:
			float: The X coordinate
		"""
		return self._X


	@property
	def Y(self):
		"""
		The **Y** coordinate of the intersection on plan.

		Returns:
			float: The Y coordinate
		"""
		return self._Y