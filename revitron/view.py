import revitron

class ViewList:
    
    views = []
    
    def __init__(self):
        pass
    
    def fromSheets(self, sheets):
        
        for sheet in sheets:
            if revitron.Element(sheet).getClassName() == 'ViewSheet':
                for viewId in sheet.GetAllPlacedViews():
                    item = revitron._helpers.AttrDict()
                    item.id = viewId
                    item.sheet = sheet
                    item.view = revitron.DOC.GetElement(viewId)
                    self.views.append(item)
                    
        return self
                    
    def get(self):
        return self.views