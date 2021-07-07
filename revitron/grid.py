class Grid(object):


	def __init__(self, typeFilterCsv=False):
		self._lines = self._getLines(typeFilterCsv)


	@property
	def lines(self):
		return self._lines


	def _getLines(self, typeFilterCsv=False):
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


	def _getLines(self, typeFilterCsv=False):
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


	def _intersection(self, xLine, yLine):
		import revitron
		obj = revitron.AttrDict
		if xLine and yLine:
			x = yLine.Curve.GetEndPoint(0).X
			y = xLine.Curve.GetEndPoint(0).Y
			return obj({
				'point': obj({
					'X': x,
					'Y': y
				}),
				'lines': obj({
					'X': obj({
						'line': xLine,
						'name': xLine.Name
					}),
					'Y': obj({
						'line': yLine,
						'name': yLine.Name
					})
				})
			})


	def closestIntersectionToPointTopLeft(self, point):
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
			return self._intersection(lines.X[top], lines.Y[left])
			

	def closestIntersectionToPointBottomRight(self, point):
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
			return self._intersection(lines.X[bottom], lines.Y[right])
