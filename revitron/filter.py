import revitron

class Filter:
    
    def __init__(self, viewId = None):
        """
        Inits a new Filter instance.

        Args:
            viewId (Element ID, optional): The optional view Id. Defaults to None.
        """                        
        if viewId:
            self.collector = revitron.DB.FilteredElementCollector(revitron.DOC, viewId) 
        else:   
            self.collector = revitron.DB.FilteredElementCollector(revitron.DOC)
    
    def byCategory(self, name):
        """
        Filters the collection by a category name - not a built-in category.

        Args:
            name (string): The category name

        Returns:
            object: The Filter instance
        """        
        self.collector = self.collector.OfCategory(revitron.Category(name).getBic())
        return self
    
    def onlyTypes(self):
        """
        Reduce to collection to types only.

        Returns:
            object: The Filter instance
        """
        self.collector = self.collector.WhereElementIsElementType()
        return self
    
    def noTypes(self):
        """
        Removes all types from collection.

        Returns:
            object: The Filter instance
        """
        self.collector = self.collector.WhereElementIsNotElementType()
        return self
    
    def byClass(self, cls):
        """
        Filters the collection by class.

        Returns:
            object: The Filter instance
        """        
        self.collector = self.collector.OfClass(cls)
        return self
    
    def getElements(self):
        """
        Get the collection as elements.

        Returns:
            list: The list of filtered elements
        """        
        return self.collector.ToElements()