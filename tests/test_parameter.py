import revitron
from revitron import _
import utils


class ParameterTests(utils.RevitronTestCase):

	def testParameterSet(self):

		wall = self.fixture.createWall()

		with revitron.Transaction():
			_(wall).set('text', 'some text')
			_(wall).set('integer', 5, 'Integer')
			_(wall).set('integerAuto', 5)
			_(wall).set('number', 10.5, 'Number')
			_(wall).set('numberAuto', 10.5)
			_(wall).set('length', 5, 'Length')
			_(wall).set('Comments', 'some comment')

		self.assertEquals(
		    str(revitron.Parameter(wall, 'integer').parameter.StorageType), 'Integer'
		)
		self.assertEquals(
		    str(revitron.Parameter(wall, 'integerAuto').parameter.StorageType), 'Integer'
		)
		self.assertEquals(
		    str(revitron.Parameter(wall, 'number').parameter.StorageType), 'Double'
		)
		self.assertEquals(
		    str(revitron.Parameter(wall, 'numberAuto').parameter.StorageType), 'Double'
		)
		self.assertEquals(
		    str(revitron.Parameter(wall, 'length').parameter.StorageType), 'Double'
		)

		self.assertEquals(
		    'Text',
		    revitron.ParameterUtils.getParameterTypeFromDefinition(
		        revitron.Parameter(wall, 'text').parameter.Definition
		    )
		)
		self.assertEquals(
		    'Integer',
		    revitron.ParameterUtils.getParameterTypeFromDefinition(
		        revitron.Parameter(wall, 'integer').parameter.Definition
		    )
		)
		self.assertEquals(
		    'Integer',
		    revitron.ParameterUtils.getParameterTypeFromDefinition(
		        revitron.Parameter(wall, 'integerAuto').parameter.Definition
		    )
		)
		self.assertEquals(
		    'Number',
		    revitron.ParameterUtils.getParameterTypeFromDefinition(
		        revitron.Parameter(wall, 'number').parameter.Definition
		    )
		)
		self.assertEquals(
		    'Number',
		    revitron.ParameterUtils.getParameterTypeFromDefinition(
		        revitron.Parameter(wall, 'numberAuto').parameter.Definition
		    )
		)
		self.assertEquals(
		    'Length',
		    revitron.ParameterUtils.getParameterTypeFromDefinition(
		        revitron.Parameter(wall, 'length').parameter.Definition
		    )
		)
		self.assertEquals(
		    'Area',
		    revitron.ParameterUtils.getParameterTypeFromDefinition(
		        revitron.Parameter(wall, 'Area').parameter.Definition
		    )
		)
		self.assertEquals(
		    'Length',
		    revitron.ParameterUtils.getParameterTypeFromDefinition(
		        revitron.Parameter(wall, 'Length').parameter.Definition
		    )
		)
		self.assertEquals(
		    'Length',
		    revitron.ParameterUtils.getParameterTypeFromDefinition(
		        revitron.Parameter(wall, 'WALL_TOP_OFFSET').parameter.Definition
		    )
		)
		self.assertEquals(
		    'YesNo',
		    revitron.ParameterUtils.getParameterTypeFromDefinition(
		        revitron.Parameter(wall, 'WALL_ATTR_ROOM_BOUNDING').parameter.Definition
		    )
		)

		self.assertEquals(_(wall).get('text'), 'some text')
		self.assertEquals(_(wall).get('integer'), 5)
		self.assertEquals(_(wall).get('integerAuto'), 5)
		self.assertEquals(_(wall).get('number'), 10.5)
		self.assertEquals(_(wall).get('numberAuto'), 10.5)
		self.assertEquals(_(wall).get('length'), 5)
		self.assertEquals(_(wall).get('Comments'), 'some comment')

	def testBuiltInParameterNameMap(self):

		ids = '-1010106,-1015083'
		toStr = utils.idsToStr
		self.assertEquals(toStr(revitron.BuiltInParameterNameMap().get('Comments')), ids)

	def testParameterTemplate(self):

		wall = _(self.fixture.createWall())
		info = _(revitron.DOC.ProjectInformation)

		with revitron.Transaction():
			wall.set('param1', 'Test & Text').set('param2', 10, 'Integer')
			info.set('projectParam', 'Project Name')

		self.assertEquals(
		    'Project_Name: Test_Text-10',
		    revitron.ParameterTemplate(
		        wall.element, '{%projectParam%}: {param1}-{param2}'
		    ).render()
		)
		self.assertEquals(
		    'Project Name: Test & Text-10',
		    revitron.ParameterTemplate(
		        wall.element, '{%projectParam%}: {param1}-{param2}', False
		    ).render()
		)

	def testParameterStorageTypes(self):

		wall = _(self.fixture.createWall())

		with revitron.Transaction():
			wall.set('param1', 'Test & Text').set('param2', 10, 'Integer')

		self.assertEquals(str(revitron.ParameterUtils.getStorageType('param1')), 'String')
		self.assertEquals(
		    str(revitron.ParameterUtils.getStorageType('param2')), 'Integer'
		)
		self.assertEquals(
		    str(revitron.ParameterUtils.getStorageType('Comments')), 'String'
		)
		self.assertEquals(str(revitron.ParameterUtils.getStorageType('Area')), 'Double')
		self.assertEquals(
		    str(revitron.ParameterUtils.getStorageType('Number')), 'Integer'
		)


utils.run(ParameterTests)