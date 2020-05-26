import revitron


class Document:
    
    @staticmethod
    def isFamily():
        try:
            if revitron.DOC.FamilyManager is not None:
                return True
        except:
            pass
        return False