import revitron
from revitron import _
import utils


class DocumentTests(utils.RevitronTestCase):

	def testIsFamily(self):
		self.assertFalse(revitron.Document().isFamily())

	def testConfigStorage(self):
		config = revitron.DocumentConfigStorage()
		config.set('test.1', {'key': 'value'})
		config.set('test.2', 'string')
		raw = revitron._(revitron.DOC.ProjectInformation).get(config.storageName)
		self.assertEquals(raw, '{"test.1": {"key": "value"}, "test.2": "string"}')
		self.assertEquals(config.get('test.2'), 'string')

	def testGetDuplicateInstances(self):
		if revitron.REVIT_VERSION > '2018':
			family = self.fixture.createGenericModelFamily()
			p1 = revitron.DB.XYZ(0, 0, 0)
			p2 = revitron.DB.XYZ(0, 0, 0)
			p3 = revitron.DB.XYZ(10, 0, 0)
			instance1 = self.fixture.createGenericModelInstance(family, p1)
			instance2 = self.fixture.createGenericModelInstance(family, p2)
			instance3 = self.fixture.createGenericModelInstance(family, p3)
			duplicatesOld = revitron.Document().getDuplicateInstances(True)
			duplicatesYoung = revitron.Document().getDuplicateInstances()
			toStr = utils.idsToStr
			self.assertEquals(str(instance1.Id.IntegerValue), toStr(duplicatesOld))
			self.assertEquals(str(instance2.Id.IntegerValue), toStr(duplicatesYoung))
			self.assertFalse(
			    str(instance3.Id.IntegerValue) in toStr(duplicatesOld) +
			    toStr(duplicatesYoung)
			)
		else:
			revitron.Log().warning(
			    'Method revitron.Document().getDuplicateInstances() requires Revit 2018 or newer!'
			)


utils.run(DocumentTests)