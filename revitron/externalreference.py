
class ExternalReference:
    
    
    def __init__(self, ref):
        """
        Inits a new ExternalReference instance.

        Args:
            ref (object): A Revit external reference instance.
        """        
        import revitron
        
        self.ref = ref
        self.type = ref.ExternalFileReferenceType
        self.path = revitron.DB.ModelPathUtils.ConvertModelPathToUserVisiblePath(ref.GetAbsolutePath())