import revitron


class Document:
    
    def __init__(self, doc = None):
        if doc is not None:
            self.doc = doc
        else:
            self.doc = revitron.DOC
    
    def isFamily(self):
        try:
            if self.doc.FamilyManager is not None:
                return True
        except:
            pass
        return False