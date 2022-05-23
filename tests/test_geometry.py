import revitron
from revitron import _
import utils


class GeometryTests(utils.RevitronTestCase):

	def testPolygonContainsPointXY(self):
		xyz = revitron.DB.XYZ
		contains = revitron.GeometryUtils.polygonContainsPointXY
		polygon1 = [xyz(1, 1, 3), xyz(-1, 1, 3), xyz(-1, -1, 3), xyz(1, -1, 3)]
		self.assertTrue(contains(polygon1, xyz(0.5, -0.5, 3)))
		self.assertFalse(contains(polygon1, xyz(0, 0, 5)))
		self.assertFalse(contains(polygon1, xyz(2, 0, 3)))
		polygon2 = [
		    xyz(0, 0, 0),
		    xyz(0, 10, 0),
		    xyz(-20, 10, 0),
		    xyz(-20, -5, 0),
		    xyz(-15, -5, 0),
		    xyz(-15, 6, 0),
		    xyz(-5, 6, 0),
		    xyz(-5, 0, 0)
		]
		self.assertFalse(contains(polygon2, xyz(-10, 2, 0)))
		self.assertFalse(contains(polygon2, xyz(-11, 4, 0)))
		self.assertFalse(contains(polygon2, xyz(1, -4, 0)))
		self.assertTrue(contains(polygon2, xyz(-2, 5, 0)))
		self.assertTrue(contains(polygon2, xyz(-17, 7, 0)))

		self.assertFalse(contains(polygon2, xyz(-17, 7, 0)))


utils.run(GeometryTests)