import revitron
from System.Collections.Generic import List


class Selection:
    
    
    @staticmethod
    def get():
        """
        Get the currently selected elements.

        Returns:
            list: The list of selected elements
        """        
        return [revitron.DOC.GetElement(elId) for elId in revitron.UIDOC.Selection.GetElementIds()]
    
    
    @staticmethod
    def first():
        """
        Get the first elements of the list of selected elements.

        Returns:
            object: The first element in a list of selected elements
        """
        return Selection.get()[0]
    
    
    @staticmethod
    def set(ids):
        """
        Set the selection to a list of element ids.

        Args:
            ids (list): A list of element ids
        """        
        revitron.UIDOC.Selection.SetElementIds(List[revitron.DB.ElementId](ids))
        revitron.UIDOC.RefreshActiveView()