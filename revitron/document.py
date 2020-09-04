""" 
The ``document`` submodule contains classes to interact with the currently active Revit document. 
"""
import json


class Document:
    
    
    def __init__(self, doc = None):
        """
        Inits a new Document instance.

        Args:
            doc (object, optional): Any document instead of the active one. Defaults to None.
        """        
        import revitron
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
        import revitron     
        try:
            for doc in revitron.APP.Documents:
                if path == doc.PathName:
                    return True
        except:
            pass
        return False
    
    
class DocumentConfigStorage:
    """
    The ``DocumentConfigStorage`` allows for easily store project configuration items.
    """
    
    def __init__(self):
        """
        Inits a new ``DocumentConfigStorage`` object.
        """
        import revitron
        
        self.storageName = 'REVITRON_CONFIG'
        self.info = revitron.DOC.ProjectInformation
        raw = revitron._(self.info).get(self.storageName)
        self.storage = dict()
        
        if raw:
            self.storage = json.loads(raw)
        
            
    def get(self, key):
        """
        Returns storage entry for a given key.

        Args:
            key (string): The key of the storage entry

        Returns:
            mixed: The stored value 
        """    
        return self.storage.get(key)
    
    
    def set(self, key, data):
        """
        Updates or creates a config storage entry.

        Args:
            key (string): The storage entry key
            data (mixed): The value of the entry
        """
        import revitron
        
        self.storage[key] = data
        # Remove empty items.
        self.storage = dict((k, v) for k, v in self.storage.iteritems() if v)
        raw = json.dumps(self.storage, sort_keys=True)
        t = revitron.Transaction()
        revitron._(self.info).set(self.storageName, raw)
        t.commit()
