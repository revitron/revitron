import revitron
from revitron import _
import utils


class RoomTests(utils.RevitronTestCase):

	def testRoomCenter(self):
		room = self.fixture.createRoom()
		center = _(room).getBboxCenter()
		self.assertEquals(center.X, 5.0)
		self.assertEquals(center.Y, 5.0)

	def testRoomPoints(self):
		xyz = revitron.DB.XYZ
		room = self.fixture.createRoom()
		boundaryPoints = _(room).getBoundaryPoints()
		testPoints = [xyz(0, 10, 0), xyz(0, 0, 0), xyz(10, 0, 0), xyz(10, 10, 0)]
		for i in range(0, 4):
			self.assertTrue(boundaryPoints[i].IsAlmostEqualTo(testPoints[i]))

	def testRoomInsetPoints(self):
		xyz = revitron.DB.XYZ
		room = self.fixture.createRoom()
		boundaryPoints = _(room).getBoundaryInsetPoints(1.0)
		testPoints = [xyz(1, 9, 0), xyz(1, 1, 0), xyz(9, 1, 0), xyz(9, 9, 0)]
		for i in range(0, 4):
			self.assertTrue(boundaryPoints[i].IsAlmostEqualTo(testPoints[i]))

	def testRoomPointTopLeft(self):
		room = self.fixture.createRoomComplex()
		point = _(room).getPointTopLeft(0.5)
		self.assertTrue(point.IsAlmostEqualTo(revitron.DB.XYZ(2.5, 11.5, 0)))

	def testRoomPointTopRight(self):
		room = self.fixture.createRoomComplex()
		point = _(room).getPointTopRight(0.5)
		self.assertTrue(point.IsAlmostEqualTo(revitron.DB.XYZ(11.5, 11.5, 0)))

	def testRoomPointBottomLeft(self):
		room = self.fixture.createRoomComplex()
		point = _(room).getPointBottomLeft(0.5)
		self.assertTrue(point.IsAlmostEqualTo(revitron.DB.XYZ(0.5, 2.5, 0)))

	def testRoomPointBottomRight(self):
		room = self.fixture.createRoomComplex()
		point = _(room).getPointBottomRight(0.5)
		self.assertTrue(point.IsAlmostEqualTo(revitron.DB.XYZ(13.5, 4.5, 0)))


utils.run(RoomTests)