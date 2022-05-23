"""
The ``transaction`` submodule contains a wrapper class to simplify the usage of transactions, 
transaction groups and subtransactions:: 

	t = revitron.Transaction() 
	... 
	t.close()

Or alternatively you can also use the following syntax::

	with revitron.Transaction():
	    ...

A transaction group can be started using::

	with revitron.TransactionGroup():
	    ...
	
"""
import __main__
import os
from pyrevit import script


class BaseTransaction:
	"""
	The base class for Revitron transaction classes. This class should not be used directly.
	"""

	def __init__(self):
		"""
		Init a basic transaction wrapper.
		"""
		import revitron
		self.transaction = revitron.DB.Transaction(revitron.DOC, self._getName())

	def __enter__(self):
		"""
		Enter transaction context.
		"""
		pass

	def __exit__(self, execType, execValue, traceback):
		"""
		Commit the transaction when leaving context.
		"""
		self.commit()

	def _getName(self):
		"""
		Build the transaction name.

		Returns:
			string: The generate transaction name.
		"""
		try:
			name = script.get_button().get_title()
		except:
			name = '{} - {}'.format(
			    os.path.basename(os.path.dirname(__main__.__file__)),
			    os.path.basename(__main__.__file__).replace('.py', '')
			)
		return name

	def commit(self):
		"""
		Commits the open transaction.
		"""
		if not self.transaction.HasEnded():
			self.transaction.Commit()

	def rollback(self):
		"""
		Rolls back the open transaction.
		"""
		if not self.transaction.HasEnded():
			self.transaction.RollBack()


class Transaction(BaseTransaction):
	"""
	A wrapper class for transactions and subtransactions. A subtransaction is started whenever 
	there is already another active transaction in use. In case the transaction is not a subtransaction, 
	it is possible to optionally suppress warnings and automatically roll back on errors.
	"""

	def __init__(self, doc=None, suppressWarnings=False, rollbackOnError=False):
		"""
		Inits a new transaction. 

		Args:
			doc (object, optional): An optional document to be used instead of the currently active one. Defaults to None.
			suppressWarnings (bool, optional): Optionally suppress any warning messages displayed during the transaction. Not available in subtransactions. Defaults to False.
			rollbackOnError: (bool, optional): Optionally roll back automatically on errors. Not available in subtransactions. Defaults to False.
		"""
		import revitron
		if not doc:
			doc = revitron.DOC
		if doc.IsModifiable:
			self.transaction = revitron.DB.SubTransaction(doc)
		else:
			name = self._getName()
			self.transaction = revitron.DB.Transaction(doc, name)
			if rollbackOnError and suppressWarnings:
				self._setFailureHandlingOptions(
				    revitron.WarningAndErrorCatcher(), clearAfterRollback=True
				)
			else:
				if suppressWarnings:
					self._setFailureHandlingOptions(revitron.WarningCatcher())
				if rollbackOnError:
					self._setFailureHandlingOptions(
					    revitron.ErrorCatcher(), clearAfterRollback=True
					)
		self.transaction.Start()

	def _setFailureHandlingOptions(self, failureProcessor, clearAfterRollback=False):
		"""
		Set up failure handling.

		Args:
			failureProcessor (object): A Revitron Failure object.
			clearAfterRollback (boolean, optional): Clears errors after rollback. Defaults to False.
		"""
		options = self.transaction.GetFailureHandlingOptions()
		options.SetFailuresPreprocessor(failureProcessor)
		options.SetClearAfterRollback(clearAfterRollback)
		self.transaction.SetFailureHandlingOptions(options)


class TransactionGroup(BaseTransaction):
	"""
	The transaction group wrapper. 
	"""

	def __init__(self, doc=False):
		"""
		Init a new transaction group.

		Args:
			doc (bool, optional): The document for the transaction. Defaults to False.
		"""
		import revitron
		if not doc:
			doc = revitron.DOC
		self.transaction = revitron.DB.TransactionGroup(doc, self._getName())
		self.transaction.Start()

	def __exit__(self, execType, execValue, traceback):
		"""
		Commit the transaction when leaving context.
		"""
		self.assimilate()

	def assimilate(self):
		"""
		Assimilates the open transaction group.
		"""
		if not self.transaction.HasEnded():
			self.transaction.Assimilate()
