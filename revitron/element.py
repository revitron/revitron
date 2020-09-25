"""
This submodule provides convenient wrappers for the interaction with elements.
Getting parameter values or other information can be quite complicated using the plain **Revit API**. 
Methods like ``revitron.Element(element).get(parameter)`` simplify that process. 

Attention:

    Note that there is also the ``_()`` shortcut function available to be even more efficient 
    in getting properties of Revit elements. `More here <revitron.html#function>`_ ...

For example getting a parameter value or even a bounding box object works as follows::

    form revitron import _
    value = _(element).get('parameter')
    boundingBox = _(element).getBbox()
    
Or setting parameter values::

    _(element).set('parameter', value)
    
"""

class Element:
    """
    A wrapper class for Revit elements. 
    
    Example::
    
        value = revitron.Element(element).get('parameter')
        
    Or in short::
    
        from revitron import _
        value = _(element).get('parameter')
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
    

    def __getattr__(self, name):
        """
        Define default method to be returned on attribute errors.
        
        Since this is a generic element class that is extended by other more specialized classes such 
        as the ``Room`` class, a default method along with an error message is returned when accidently 
        calling a special methods that only exists in one of the derived classes on an element of another class.

        Args:
            name (string): The name of the called method

        Returns:
            method: An empty method
        """
        from revitron import Log
        def method(*args):
            Log().error('Failed to call unkown method "{}" for element of class "{}"'.format(name, self.getClassName()))
        return method


    def delete(self):
        """
        Delete an element.
        
        Example::
        
            _(element).delete()
        """
        import revitron
        revitron.DOC.Delete(self.element.Id)
        
        
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
    
    
    def getFromType(self, paramName):
        """
        Returns a parameter value of the element type.
        
        Example::
        
            value = _(element).getFromType('name')
            
        Args:
            paramName (string): The name of the parameter

        Returns:
            mixed: The parameter value
        """  
        from revitron import _
        try:
            return _(self.element.GetTypeId()).get(paramName)
        except:
            return ''
    
    
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
      
      
    def getTags(self):
        """
        Get possibly existing tags of an element.

        Returns:
            list: A list of Revit tag objects depending on the element class
        """
        import revitron
        
        category = self.getParameter('Category').getValueString()
    
        switcher = {
            'Rooms': revitron.DB.SpatialElementTag
        }
        
        tags = []
        
        try:
            fltr = revitron.DB.ElementClassFilter(switcher.get(category))
            for item in self.element.GetDependentElements(fltr):
                _element = Element(item)
                if _element.getClassName() in ['RoomTag']:
                    tags.append(_element.element)
        except:
            pass
        return tags
        
    
    def set(self, paramName, value, paramType = 'Text'):
        """
        Sets a parameter value.

        Example::
        
            _(element).set('name', 'value', 'type')
        
        Some possible parameter types are: 
            
        - ``Text``
        - ``Integer`` 
        - ``Number``
        - ``Length``
        - ``Angle`` 
        - ``Material``
        - ``YesNo``
        - ``MultilineText``
        - ``FamilyType``
             
        You can find a list of all types `here <https://www.revitapidocs.com/2019/f38d847e-207f-b59a-3bd6-ebea80d5be63.htm>`_.

            
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