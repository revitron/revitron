"""
This is a helper submodule for handling errors. 
"""
from Autodesk.Revit.DB import IFailuresPreprocessor


class WarningSwallower(IFailuresPreprocessor):
	"""
	This class implements the ``IFailurePreprocessor`` interface and can be used as a preprocessor 
	for failures to mute all warnings.

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
		import revitron
		for failure in failuresAccessor.GetFailureMessages():
			failuresAccessor.DeleteWarning(failure)
		return revitron.DB.FailureProcessingResult.Continue
