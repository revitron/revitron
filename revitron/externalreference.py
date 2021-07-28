""" 
This submodule contains a wrapper class for external references within a **Revit** document.
"""


class ExternalReference:
	""" 
	An external reference wrapper class.
	"""

	def __init__(self, ref):
		"""
		Inits a new ExternalReference instance.

		Args:
			ref (object): A Revit external reference instance.
		"""
		import revitron

		self.ref = ref
		self.type = ref.ExternalFileReferenceType
		self.path = revitron.DB.ModelPathUtils.ConvertModelPathToUserVisiblePath(
		    ref.GetAbsolutePath()
		)
