import revitron

class Filter:
    
    def __init__(self):
        self.collector = revitron.DB.FilteredElementCollector(revitron.DOC)
    
    def byClass(self, _class):
        self.collector = self.collector.OfClass(_class)
        return self
    
    def getElements(self):
        return self.collector.ToElements()