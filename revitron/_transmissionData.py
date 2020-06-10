import revitron
import re
import shutil
import os

class TransmissionData:
    
    refs = dict()
    
    def __init__(self, hostPath):
        """
        Inits a new TransmissionData instance

        Args:
            hostPath (string): The path of the host model
        """        
        self.hostPath = revitron.DB.FilePath(hostPath)
        self.data = revitron.DB.TransmissionData.ReadTransmissionData(self.hostPath)
        
        for refId in self.data.GetAllExternalFileReferenceIds():
            self.refs[refId.IntegerValue] = revitron.ExternalReference(self.data.GetLastSavedReferenceData(refId))
        
    def moveLinksOnDisk(self, source, target):
        """
        Moves all external CAD and RVT links on disk and relinks them.

        Args:
            source (string): The source directory 
            target (string): The target directory
        """
        source = '^' + re.escape(source)
        
        for _id in self.refs:
            
            refId = revitron.DB.ElementId(_id)
            ref = self.refs[_id]
            
            if str(ref.type) in ['RevitLink', 'CADLink']:
                
                if re.search(source, ref.path, re.IGNORECASE):
                    newPath = re.sub(source, target, ref.path, re.IGNORECASE)
                else:
                    newPath = re.sub(r'\\\\$', '', target) + '\\' + os.path.basename(ref.path)
                    
                print(newPath)
                
                if newPath != ref.path:
                    try:
                        os.makedirs(os.path.dirname(newPath))
                    except:
                        pass
                    try:
                        shutil.copyfile(ref.path, newPath)
                    except:
                        pass
                    
                    self.data.SetDesiredReferenceData(refId, revitron.DB.FilePath(newPath), revitron.DB.PathType.Absolute, True)
                
        self.write()
        
    def write(self):
        """
        Writes the TransmissionData back to the model.
        """        
        self.data.IsTransmitted = True
        revitron.DB.TransmissionData.WriteTransmissionData(self.hostPath, self.data)
        
    
    