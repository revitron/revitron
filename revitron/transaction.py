"""
The ``transaction`` submodule contains a wrapper class to simplify the usage of transactions and subtransactions:: 

	t = revitron.Transaction() 
	... 
	t.close()
	
"""
from pyrevit import script


class Transaction:
	"""
	A transaction helper class. 
	"""
	
	def __init__(self):
		"""
		Inits a new transaction. 

		In case there is already an open transaction, a subtransaction will be initialized instead.
		"""  
		import revitron
		if revitron.DOC.IsModifiable:
			self.transaction = revitron.DB.SubTransaction(revitron.DOC)
		else:
			self.transaction = revitron.DB.Transaction(revitron.DOC, script.get_button().get_title())
		self.transaction.Start()
		
		
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
	