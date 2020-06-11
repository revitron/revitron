import revitron


class Selection:
    
    @staticmethod
    def get():
        return [revitron.DOC.GetElement(elId) for elId in revitron.UIDOC.Selection.GetElementIds()]
    
    @staticmethod
    def first():
        return Selection.get()[0]