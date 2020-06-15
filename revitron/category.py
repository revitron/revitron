import revitron

class Category:
    
    
    def __init__(self, name):
        """
        Init a new Category by name.

        Args:
            name (string): The category name
        """
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
        for item in dir(revitron.DB.BuiltInCategory):
            try:
                bic = getattr(revitron.DB.BuiltInCategory, item)
                if int(bic) == self.category.Id.IntegerValue:
                    return bic
            except:
                pass  
