""" 
This submodule contains wrapper classes for links used in Revit models.
"""
from revitron.element import Element


class LinkRvt(Element):
    """
    A wrapper class for Revit links.
    """
    
    def getPath(self):
        """
        Gets the path of the linked document.

        Returns:
            string: The path on disk
        """   
        import revitron
             
        try:
            return revitron.Document(self.element.GetLinkDocument()).getPath()
        except:
            pass
    
    
    def getType(self):
        """
        Gets the type object of the link.

        Returns:
            object: The Link type
        """
        import revitron
        
        try:
            return revitron.DOC.GetElement(self.get('Type'))  
        except:
            pass
