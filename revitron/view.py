import revitron

class ViewSheetList:
    """
    The ViewSheetList class creates a list of custom view objects based on a list of sheets. 
    """    
    
    def __init__(self, sheets):
        """
        Inits an new ViewSheetList object. 

        Args:
            sheets (list): A list with sheets
        """      
        self.views = []  
        for sheet in sheets:
            if revitron.Element(sheet).getClassName() == 'ViewSheet':
                for viewId in sheet.GetAllPlacedViews():
                    item = revitron._helpers.AttrDict()
                    item.id = viewId
                    item.sheet = sheet
                    item.view = revitron.DOC.GetElement(viewId)
                    self.views.append(item)
    
    
    def get(self):
        """
        Returns the list of view objects. The view objects have the following properties:

        - `id`: The ID of the view
        - `sheet`: The sheet object where the view is placed on
        - `view`: The actual view object
        
        The returned list can be used as follows::
        
            sheets = revitron.Filter().byCategory('Sheets').getElements()
            for view in revitron.ViewSheetList(sheets).get():
                print(view.id, view.sheet, view.view)

        Returns:
            list: A list with view objects as described above
        """        
        return self.views