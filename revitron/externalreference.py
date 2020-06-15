import revitron

class ExternalReference:
    
    
    def __init__(self, ref):
        """
        Inits a new ExternalReference instance.

        Args:
            ref (object): A Revit external reference instance.
        """        
        self.ref = ref
        self.type = ref.ExternalFileReferenceType
        self.path = revitron.DB.ModelPathUtils.ConvertModelPathToUserVisiblePath(ref.GetAbsolutePath())