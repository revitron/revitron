import revitron
from revitron import _
import utils


class FilterTests(utils.RevitronTestCase):

	def testStringFilters(self):

		w1 = self.fixture.createWall([0, 10], [10, 10])
		w2 = self.fixture.createWall([0, 20], [10, 20])
		w3 = self.fixture.createWall([0, 30], [10, 30])
		w4 = self.fixture.createWall([0, 40], [10, 40])
		w5 = self.fixture.createWall([0, 50], [10, 50])

		with revitron.Transaction():
			_(w1).set('test', 'an awesome test wall')
			_(w2).set('test', 'another awesome test wall')
			_(w3).set('test', 'and one more wall')
			_(w4).set('Comments', 'test comment')

		f = revitron.Filter
		toStr = utils.idsToStr

		self.assertEquals(
		    toStr([w1.Id,
		           w2.Id]),
		    toStr(f().byStringContains('test',
		                               'awesome').noTypes().getElementIds())
		)

		self.assertEquals(
		    toStr([w4.Id,
		           w5.Id]),
		    toStr(
		        f().byCategory('Walls').byStringContains('test',
		                                                 'wall',
		                                                 True).noTypes().getElementIds()
		    )
		)

		self.assertEquals(
		    toStr([w4.Id,
		           w5.Id]),
		    toStr(
		        f().byCategory('OST_Walls').byStringContains('test',
		                                                     'wall',
		                                                     True
		                                                     ).noTypes().getElementIds()
		    )
		)

		self.assertEquals(
		    toStr([w3.Id]),
		    toStr(f().byStringBeginsWith('test',
		                                 'and one').noTypes().getElementIds())
		)

		self.assertEquals(
		    toStr([w1.Id,
		           w2.Id,
		           w3.Id]),
		    toStr(f().byStringEndsWith('test',
		                               'wall').noTypes().getElementIds())
		)

		self.assertEquals(
		    toStr([w3.Id]),
		    toStr(
		        f().byStringEquals('test',
		                           'and one more wall').noTypes().getElementIds()
		    )
		)

		self.assertEquals(
		    toStr([w4.Id]),
		    toStr(
		        f().byStringEquals('Comments',
		                           'test comment').noTypes().getElementIds()
		    )
		)

		self.assertEquals(
		    toStr([w2.Id,
		           w3.Id]),
		    toStr(
		        f().byStringContainsOneInCsv('test',
		                                     'one, another').noTypes().getElementIds()
		    )
		)

		self.assertEquals(
		    toStr([w1.Id,
		           w4.Id,
		           w5.Id]),
		    toStr(
		        f().byCategory('Walls'
		                       ).byStringContainsOneInCsv('test',
		                                                  'one, another',
		                                                  True).noTypes().getElementIds()
		    )
		)

		self.assertEquals(
		    toStr([w1.Id,
		           w3.Id]),
		    toStr(
		        f().byStringEqualsOneInCsv(
		            'test',
		            'an awesome test wall, and one more wall'
		        ).noTypes().getElementIds()
		    )
		)

	def testRegexFilter(self):
		family = self.fixture.createGenericModelFamily()
		genModel = self.fixture.createGenericModelInstance(
		    family,
		    revitron.DB.XYZ(0,
		                    0,
		                    0)
		)
		f = revitron.Filter
		toStr = utils.idsToStr
		self.assertEquals(
		    toStr([genModel.Id]),
		    toStr(
		        f().noTypes().byRegex('Family and Type',
		                              '\-genericModel\-Revit').getElementIds()
		    )
		)

	def testNumericFilters(self):
		w1 = self.fixture.createWall([0, 10], [10, 10])
		w2 = self.fixture.createWall([0, 20], [10, 20])

		with revitron.Transaction():
			_(w1).set('num', 1, 'Number').set('int', 1, 'Integer')
			_(w2).set('num', 5, 'Number').set('int', 5, 'Integer')

		f = revitron.Filter
		toStr = utils.idsToStr
		self.assertEquals(
		    toStr([w1.Id]),
		    toStr(
		        f().byCategory('Walls').byNumberIsEqual('num',
		                                                1).noTypes().getElementIds()
		    )
		)
		self.assertEquals(
		    toStr([w1.Id]),
		    toStr(
		        f().byCategory('Walls').byNumberIsEqual('int',
		                                                1).noTypes().getElementIds()
		    )
		)
		self.assertEquals(
		    toStr([w2.Id]),
		    toStr(
		        f().byCategory('Walls').byNumberIsEqual('num',
		                                                '5').noTypes().getElementIds()
		    )
		)
		self.assertEquals(
		    toStr([w2.Id]),
		    toStr(
		        f().byCategory('Walls').byNumberIsEqual('int',
		                                                '5').noTypes().getElementIds()
		    )
		)
		self.assertEquals(
		    toStr([w2.Id]),
		    toStr(
		        f().byCategory('Walls').byNumberIsGreater('num',
		                                                  1).noTypes().getElementIds()
		    )
		)
		self.assertEquals(
		    toStr([w2.Id]),
		    toStr(
		        f().byCategory('Walls').byNumberIsGreater('int',
		                                                  1).noTypes().getElementIds()
		    )
		)
		self.assertEquals(
		    toStr([w1.Id,
		           w2.Id]),
		    toStr(
		        f().byCategory('Walls'
		                       ).byNumberIsGreaterOrEqual('num',
		                                                  1).noTypes().getElementIds()
		    )
		)
		self.assertEquals(
		    toStr([w1.Id,
		           w2.Id]),
		    toStr(
		        f().byCategory('Walls'
		                       ).byNumberIsGreaterOrEqual('int',
		                                                  1).noTypes().getElementIds()
		    )
		)
		self.assertEquals(
		    toStr([w1.Id]),
		    toStr(
		        f().byCategory('Walls').byNumberIsLess('num',
		                                               5).noTypes().getElementIds()
		    )
		)
		self.assertEquals(
		    toStr([w1.Id]),
		    toStr(
		        f().byCategory('Walls').byNumberIsLess('int',
		                                               5).noTypes().getElementIds()
		    )
		)
		self.assertEquals(
		    toStr([w1.Id,
		           w2.Id]),
		    toStr(
		        f().byCategory('Walls').byNumberIsLessOrEqual('num',
		                                                      5).noTypes().getElementIds()
		    )
		)
		self.assertEquals(
		    toStr([w1.Id,
		           w2.Id]),
		    toStr(
		        f().byCategory('Walls').byNumberIsLessOrEqual('int',
		                                                      5).noTypes().getElementIds()
		    )
		)


utils.run(FilterTests)