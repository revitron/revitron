import revitron
from revitron import _
import utils


class ParameterTests(utils.RevitronTestCase):
	
	def testParameterSet(self):

		wall = self.fixture.createWall()

		t = revitron.Transaction()
		_(wall).set('text', 'some text')
		_(wall).set('integer', 5, 'Integer')
		_(wall).set('number', 10.5, 'Number')
		_(wall).set('length', 5, 'Length')
		_(wall).set('Comments', 'some comment')
		t.commit()

		self.assertEquals(str(revitron.Parameter(wall, 'integer').parameter.StorageType), 'Integer')
		self.assertEquals(str(revitron.Parameter(wall, 'number').parameter.StorageType), 'Double')
		self.assertEquals(str(revitron.Parameter(wall, 'length').parameter.StorageType), 'Double')

		self.assertEquals('Text',
			str(revitron.Parameter(wall, 'text').parameter.Definition.ParameterType))
		self.assertEquals('Integer',
			str(revitron.Parameter(wall, 'integer').parameter.Definition.ParameterType))
		self.assertEquals('Number',
			str(revitron.Parameter(wall, 'number').parameter.Definition.ParameterType))
		self.assertEquals('Length',
			str(revitron.Parameter(wall, 'length').parameter.Definition.ParameterType))

		self.assertEquals(_(wall).get('text'), 'some text')
		self.assertEquals(_(wall).get('integer'), 5)
		self.assertEquals(_(wall).get('number'), 10.5)
		self.assertEquals(_(wall).get('length'), 5)
		self.assertEquals(_(wall).get('Comments'), 'some comment')

	def testBuiltInParameterNameMap(self):
	
		ids = '-1010106,-1015083'
		toStr = utils.idsToStr
		self.assertEquals(toStr(revitron.BuiltInParameterNameMap().get('Comments')), ids)

	def testParameterTemplate(self):

		wall = _(self.fixture.createWall())
		info = _(revitron.DOC.ProjectInformation)

		t = revitron.Transaction()
		wall.set('param1', 'Test & Text').set('param2', 10, 'Integer')
		info.set('projectParam', 'Project Name')
		t.commit()

		self.assertEquals('Project_Name: Test_Text-10',
			revitron.ParameterTemplate(wall.element, '{%projectParam%}: {param1}-{param2}').render())
		self.assertEquals('Project Name: Test & Text-10',
			revitron.ParameterTemplate(wall.element, '{%projectParam%}: {param1}-{param2}', False).render())
		
utils.run(ParameterTests)