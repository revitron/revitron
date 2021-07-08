from revitron import _
import utils


class BoundingBoxTests(utils.RevitronTestCase):
	
	def testContainsXY(self):
		wall1 = self.fixture.createWall([0, 0],[20, 20])
		wall2 = self.fixture.createWall([2, 5],[12, 15])
		self.assertTrue(_(wall1).getBbox().containsXY(_(wall2).getBbox()))
		self.assertTrue(_(wall1).getBbox().containsXY(_(wall1).getBbox()))
		self.assertFalse(_(wall2).getBbox().containsXY(_(wall1).getBbox()))

	def testGetCenterPoint(self):
		room = self.fixture.createRoom()
		center = _(room).getBbox().getCenterPoint()
		self.assertEquals(center.X, 5.0)
		self.assertEquals(center.Y, 5.0)

utils.run(BoundingBoxTests)