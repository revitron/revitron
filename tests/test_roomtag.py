import revitron
from revitron import _
import utils


class RoomTagTests(utils.RevitronTestCase):

	def testCreate(self):

		room = self.fixture.createRoom()

		t = revitron.Transaction()
		tag = revitron.RoomTag.center(room)
		t.commit()
		self.assertEquals(tag.Id.IntegerValue, _(room).getTags()[0].Id.IntegerValue)

		t = revitron.Transaction()
		tag = revitron.RoomTag.topLeft(room)
		t.commit()
		self.assertEquals(tag.Id.IntegerValue, _(room).getTags()[0].Id.IntegerValue)

		t = revitron.Transaction()
		tag = revitron.RoomTag.topRight(room)
		t.commit()
		self.assertEquals(tag.Id.IntegerValue, _(room).getTags()[0].Id.IntegerValue)

		t = revitron.Transaction()
		tag = revitron.RoomTag.bottomLeft(room)
		t.commit()
		self.assertEquals(tag.Id.IntegerValue, _(room).getTags()[0].Id.IntegerValue)

		t = revitron.Transaction()
		tag = revitron.RoomTag.bottomRight(room)
		t.commit()
		self.assertEquals(tag.Id.IntegerValue, _(room).getTags()[0].Id.IntegerValue)


utils.run(RoomTagTests)