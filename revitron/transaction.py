"""
The ``transaction`` submodule contains a wrapper class to simplify the usage of transactions and subtransactions:: 

	t = revitron.Transaction() 
	... 
	t.close()
	
"""
import __main__
import os
from pyrevit import script


class Transaction:
	"""
	A transaction helper class. 
	"""
	
	def __init__(self, doc = None, suppressWarnings = False):
		"""
		Inits a new transaction. 

		In case there is already an open transaction, a subtransaction will be initialized instead.

		Args:
			doc (bool, optional): On optional document to be used instead of the currently active one. Defaults to None.
			suppressWarnings (bool, options): Optionally suppress any warning messages displayed during the transaction: Defaults to False.
		"""
		import revitron
		if not doc:
			doc = revitron.DOC
		if doc.IsModifiable:
			self.transaction = revitron.DB.SubTransaction(doc)
		else:
			try:
				name = script.get_button().get_title()
			except:
				name = '{} - {}'.format(
					os.path.basename(os.path.dirname(__main__.__file__)),
					os.path.basename(__main__.__file__).replace('.py', '')
				)
			self.transaction = revitron.DB.Transaction(doc, name)
		self.transaction.Start()
		if suppressWarnings:
			options = self.transaction.GetFailureHandlingOptions()
			options.SetFailuresPreprocessor(revitron.WarningSwallower())
			self.transaction.SetFailureHandlingOptions(options)
		
		
	def commit(self):
		"""
		Commits the open transaction.
		"""        
		self.transaction.Commit()
		
	
	def rollback(self):
		"""
		Rolls back the open transaction.
		"""
		self.transaction.RollBack()
	