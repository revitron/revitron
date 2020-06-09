import revitron
import re
import shutil
import os
from _element import Element

class LinkRvt(Element):
    
    def moveOnDisk(self, search, replace):
        current = self.getPath()
        new = re.sub(search, replace, current, re.IGNORECASE)
        
        if current != new:
            linkType = self.getType()
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
        return revitron.Document(self.element.GetLinkDocument()).getPath()
    
    def getType(self):
        return revitron.DOC.GetElement(self.get('Type'))  
