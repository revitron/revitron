import revitron
from revitron.element import Element

class LinkRvt(Element):
    
    def getPath(self):
        """
        Gets the path of the linked document.

        Returns:
            string: The path on disk
        """        
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
        try:
            return revitron.DOC.GetElement(self.get('Type'))  
        except:
            pass
