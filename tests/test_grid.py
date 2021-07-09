from revitron import _
import revitron
import utils


class GridTests(utils.RevitronTestCase):

	def testOrthoGridIntersections(self):
		ortho = revitron.OrthoGrid
		xyz = revitron.DB.XYZ
		with revitron.Transaction():
			x1 = ortho.newLineX(10, 'x1')
			x2 = ortho.newLineX(20, 'x2')
			x3 = ortho.newLineX(30, 'x3')
			x4 = ortho.newLineX(40, 'x4')
			y1 = ortho.newLineY(40, 'y1')
			y2 = ortho.newLineY(30, 'y2')
			y3 = ortho.newLineY(20, 'y3')
			y4 = ortho.newLineY(10, 'y4')
		point = xyz(22, 33, 0)
		grid = ortho()
		intersectionTopLeft = grid.closestIntersectionToPointTopLeft(point)
		intersectionBottomRight = grid.closestIntersectionToPointBottomRight(point)
		self.assertEquals(intersectionTopLeft.nameX, 'x2')
		self.assertEquals(intersectionTopLeft.X, 20)
		self.assertEquals(intersectionTopLeft.nameY, 'y1')
		self.assertEquals(intersectionTopLeft.Y, 40)
		self.assertEquals(intersectionBottomRight.nameX, x3.Name)
		self.assertNotEquals(intersectionBottomRight.nameX, x2.Name)
		self.assertEquals(intersectionBottomRight.X, 30)
		self.assertEquals(intersectionBottomRight.nameY, y2.Name)
		self.assertEquals(intersectionBottomRight.Y, 30)

	def testGridLines(self):
		newLine = revitron.Create.GridLineLinear
		xyz = revitron.DB.XYZ
		with revitron.Transaction():
			l1 = newLine(xyz(0, 0, 0), xyz(20, 10, 0), 'A')
			l2 = newLine(xyz(0, 0, 0), xyz(0, 20, 0), 'B')
			l3 = newLine(xyz(10, 0, 0), xyz(10, 100, 0), 'C')
			l4 = newLine(xyz(10, 5, 0), xyz(0, 5, 0), 'D')
		grid = revitron.Grid()
		ortho = revitron.OrthoGrid()
		gridNames = sorted(grid.lines.keys())
		orthoXNames = sorted(ortho.lines.X.keys())
		orthoYNames = sorted(ortho.lines.Y.keys())
		self.assertEqual(''.join(gridNames), 'ABCD')
		self.assertEqual(''.join(orthoXNames), 'BC')
		self.assertEqual(''.join(orthoYNames), 'D')
		self.assertNotEquals(''.join(orthoXNames), 'BCD')

utils.run(GridTests)