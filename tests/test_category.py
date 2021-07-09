import revitron
import utils


class CatergoryTests(utils.RevitronTestCase):
	
	def testGet(self):
		self.assertEqual(revitron.Category('Walls').get().Name, 'Walls')
	
	def testGetBic(self):
		self.assertEqual(revitron.Category('Walls').getBic(), revitron.DB.BuiltInCategory.OST_Walls)

	def testBicGet(self):
		self.assertEqual(
			revitron.BuiltInCategory('AreaSchemeLines').get(), 
			revitron.DB.BuiltInCategory.OST_AreaSchemeLines
		)
		self.assertEqual(
			revitron.BuiltInCategory('OST_AreaSchemeLines').get(), 
			revitron.DB.BuiltInCategory.OST_AreaSchemeLines
		)
		self.assertEqual(
			revitron.BuiltInCategory('Walls').get(), 
			revitron.DB.BuiltInCategory.OST_Walls
		)
		self.assertEqual(
			revitron.BuiltInCategory('OST_Walls').get(), 
			revitron.DB.BuiltInCategory.OST_Walls
		)
		self.assertEqual(
			revitron.BuiltInCategory('DSR_ArrowHeadStyleId').get(), 
			revitron.DB.BuiltInCategory.OST_DSR_ArrowHeadStyleId
		)
		self.assertEqual(
			revitron.BuiltInCategory('Analytical Beam Tags').get(), 
			revitron.DB.BuiltInCategory.OST_BeamAnalyticalTags
		)
	
utils.run(CatergoryTests)