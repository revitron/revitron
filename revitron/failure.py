"""
This is a helper submodule for handling errors and warnings occuring in transactions. 
"""
from Autodesk.Revit.DB import IFailuresPreprocessor


class FailureHandler:
	"""
	A basic failure handler.
	"""

	errorMessage = ''

	@staticmethod
	def preprocess(failuresAccessor, suppressWarnings=False, rollbackOnError=False):
		"""
		Preprocess failures by optionally suppressing all warnings and rolling back transactions on error.

		Args:
			failuresAccessor (object): A Revit failure accessor object.
			suppressWarnings (bool, optional): Optionally suppress all warnings. Defaults to False.
			rollbackOnError (bool, optional): Optionally roll back on errors. Defaults to False.

		Returns:
			object: A Revit ``FailureProcessingResult``
		"""
		import revitron
		FailureHandler.errorMessage = ''
		for failure in failuresAccessor.GetFailureMessages():
			if rollbackOnError:
				if failure.GetSeverity() == revitron.DB.FailureSeverity.Error:
					FailureHandler.errorMessage = failure.GetDescriptionText()
					failuresAccessor.DeleteWarning(failure)
					return revitron.DB.FailureProcessingResult.ProceedWithRollBack
			if suppressWarnings:
				failuresAccessor.DeleteWarning(failure)
		return revitron.DB.FailureProcessingResult.Continue


class ErrorCatcher(IFailuresPreprocessor):
	"""
	This class implements the ``IFailurePreprocessor`` interface and can be used as a preprocessor 
	for rolling back on errors.

	Args:
		IFailuresPreprocessor (interface): The Revit API IFailuresPreprocessor interface.
	"""

	def PreprocessFailures(self, failuresAccessor):
		"""
		Preprocess all failures and returns a ProceedWithRollBack result on error.

		Args:
			failuresAccessor (object): The Revit API ``FailuresAccessor`` object.

		Returns:
			object: The ``FailureProcessingResult.ProceedWithRollBack`` result on error or ``FailureProcessingResult.Continue``.
		"""
		return FailureHandler.preprocess(
		    failuresAccessor,
		    suppressWarnings=False,
		    rollbackOnError=True
		)


class WarningCatcher(IFailuresPreprocessor):
	"""
	This class implements the ``IFailurePreprocessor`` interface and can be used as a preprocessor 
	for muting all warnings.

	Args:
		IFailuresPreprocessor (interface): The Revit API IFailuresPreprocessor interface.
	"""

	def PreprocessFailures(self, failuresAccessor):
		"""
		Preprocess all failures and deletes all warnings to suppress dialog boxes.

		Args:
			failuresAccessor (object): The Revit API ``FailuresAccessor`` object.

		Returns:
			object: The ``FailureProcessingResult.Continue`` result
		"""
		return FailureHandler.preprocess(
		    failuresAccessor,
		    suppressWarnings=True,
		    rollbackOnError=False
		)


class WarningAndErrorCatcher(IFailuresPreprocessor):
	"""
	This class implements the ``IFailurePreprocessor`` interface and can be used as a preprocessor 
	for rolling back on errors and muting all warnings.

	Args:
		IFailuresPreprocessor (interface): The Revit API IFailuresPreprocessor interface.
	"""

	def PreprocessFailures(self, failuresAccessor):
		"""
		Preprocess all failures and returns a ProceedWithRollBack result on error.

		Args:
			failuresAccessor (object): The Revit API ``FailuresAccessor`` object.

		Returns:
			object: The ``FailureProcessingResult.ProceedWithRollBack`` result on error or ``FailureProcessingResult.Continue``.
		"""
		return FailureHandler.preprocess(
		    failuresAccessor,
		    suppressWarnings=True,
		    rollbackOnError=True
		)