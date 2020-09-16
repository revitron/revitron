"""
The purpose of this submodule is to provide convenient wrappers for the interaction with elements.
Getting parameter values or other information can be quite complicated using the plain Revit API. 
Using a method like ``revitron.Element(element).get(parameter)`` simplifies that process. 
Note that there is also the ``_()`` shortcut function available to be even more efficient 
in getting properties::

    form revitron import _
    value = _(element).get('parameter')
    boundingBox = _(element).getBbox()
    
Or setting parameter values::

    _(element).set('parameter', value)
    
"""

class Element:
    """
    A wrapper class for Revit elements. 
    """
     
    def __init__(self, element):
        """
        Inits a new element instance.

        Args:
            element (object): The Revit element or an element ID
        """   
        import revitron
        if isinstance(element, revitron.DB.ElementId):
            self.element = revitron.DOC.GetElement(element)   
        else:
            self.element = element
    

    def getBbox(self):
        """
        Returns a bounding box for the element.

        Returns:
            object: The bounding box or false on error
        """
        import revitron
        try:
            return revitron.BoundingBox(self.element)
        except:
            return False
    
    
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
        
        Example::
        
            value = _(element).get('name')
            
        Args:
            paramName (string): The name of the parameter

        Returns:
            mixed: The parameter value
        """        
        import revitron
        return revitron.Parameter(self.element, paramName).get()
    
    
    def getParameter(self, paramName):
        """
        Returns a parameter object.

        Args:
            paramName (string): The name of the parameter

        Returns:
            object: The parameter object
        """
        import revitron
        return revitron.Parameter(self.element, paramName)
      
    
    def set(self, paramName, value, paramType = 'Text'):
        """
        Sets a parameter value.

        Example::
        
            _(element).set('name', 'value')
            
        Args:
            paramName (string): The parameter name
            value (mixed): The value
            paramType (string, optional): The parameter type. Defaults to 'Text'.

        Returns:
            object: The element instance
        """        
        import revitron
        revitron.Parameter(self.element, paramName).set(value, paramType)
        return self