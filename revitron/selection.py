import revitron


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