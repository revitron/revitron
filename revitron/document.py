import revitron

class Document:
    
    
    def __init__(self, doc = None):
        """
        Inits a new Document instance.

        Args:
            doc (object, optional): Any document instead of the active one. Defaults to None.
        """        
        if doc is not None:
            self.doc = doc
        else:
            self.doc = revitron.DOC
    
    
    def getPath(self):
        """
        Returns the path to the document.

        Returns:
            string: The path
        """
        return self.doc.PathName
    
    
    def isFamily(self):
        """
        Checks whether the document is a family.

        Returns:
            boolean: True in case the document is a family
        """
        try:
            if self.doc.FamilyManager is not None:
                return True
        except:
            pass
        return False
    
    
    @staticmethod
    def isOpen(path):
        """
        Checks whether a document is open by passing its path.

        Args:
            path (string): The path

        Returns:
            boolean: True in case the document is open
        """        
        try:
            for doc in revitron.APP.Documents:
                if path == doc.PathName:
                    return True
        except:
            pass
        return False