import revitron

class Element:
    
     
    def __init__(self, element):
        """
        Inits a new element instance.

        Args:
            element (object): The Revit element or an element ID
        """   
        if isinstance(element, revitron.DB.ElementId):
            self.element = revitron.DOC.GetElement(element)   
        else:
            self.element = element
    
    
    def getClassName(self):
        """
        Returns the class name of the element.

        Returns:
            string: The class name
        """        
        return self.element.__class__.__name__
    
    
    def get(self, paramName):
        """
        Returns a parameter value.

        Args:
            paramName (string): The name of the parameter

        Returns:
            mixed: The parameter value
        """        
        return revitron.Parameter(self.element, paramName).get()
    
    
    def getParameter(self, paramName):
        """
        Returns a parameter object.

        Args:
            paramName (string): The name of the parameter

        Returns:
            object: The parameter object
        """
        return revitron.Parameter(self.element, paramName)
      
    
    def set(self, paramName, value, paramType = 'Text'):
        """
        Sets a parameter value.

        Args:
            paramName (string): The parameter name
            value (mixed): The value
            paramType (string, optional): The parameter type. Defaults to 'Text'.

        Returns:
            object: The element instance
        """        
        revitron.Parameter.bind(self.element.Category.Name, paramName, paramType)
        revitron.Parameter(self.element, paramName).set(value)
        return self