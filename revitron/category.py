""" 
To simply the interaction with Revit categories, the ``category`` 
submodule provides the ``Category`` class to be able to access category objects by name.
"""

class Category:
    """
    A wrapper class for category objects which can be instantiated by a catergory name.
    """
    
    def __init__(self, name):
        """
        Init a new Category by name.

        Args:
            name (string): The category name
        """
        import revitron
        self.category = revitron.DOC.Settings.Categories.get_Item(name)
        
        
    def get(self):
        """
        Returns the category object.

        Returns:
            object: The category object
        """
        return self.category
    
    
    def getBic(self):
        """
        Returns the built-in category for a given category.

        Returns:
            object: The built-in category
        """    
        import revitron    
        for item in dir(revitron.DB.BuiltInCategory):
            try:
                bic = getattr(revitron.DB.BuiltInCategory, item)
                if int(bic) == self.category.Id.IntegerValue:
                    return bic
            except:
                pass  
