import revitron
import re
import shutil
import os
from _element import Element

class LinkRvt(Element):
    
    def moveOnDisk(self, search, replace):
        """
        Move a link on disk and reload it from its new location.

        Args:
            search (string): Search pattern to be replaced 
            replace (string): Replacement in path

        Returns:
            string: The new path on success
        """        
        linkType = self.getType()
        transaction = revitron.Transaction()
        linkType.PathType = revitron.DB.PathType.Absolute
        transaction.commit()
        current = self.getPath()
        new = re.sub(search, replace, current, re.IGNORECASE)
        
        if current != new:
            
            worksetConfig = revitron.DB.WorksetConfiguration()
            try:
                os.makedirs(os.path.dirname(new))
            except:
                pass
            try:
                shutil.copyfile(current, new)
            except:
                pass
            linkType.LoadFrom(revitron.DB.FilePath(new), worksetConfig)
            
            return new
    
    def getPath(self):
        """
        Gets the path of the linked document.

        Returns:
            string: The path on disk
        """        
        return revitron.Document(self.element.GetLinkDocument()).getPath()
    
    def getType(self):
        """
        Gets the type object of the link.

        Returns:
            object: The Link type
        """
        return revitron.DOC.GetElement(self.get('Type'))  
