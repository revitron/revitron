import revitron
import os

class Parameter:
    
    
    def __init__(self, element, name):        
        """
        Init a new parameter instance.

        Args:
            element (object): Revit element
            name (string): The parameter name
        """
        self.parameter = element.LookupParameter(name)
    
    
    @staticmethod
    def isBoundToCategory(category, paramName):        
        """
        Test if a parameter is bound to a given category.

        Args:
            category (string): The category name
            paramName (string): The parameter name

        Returns:
            boolean: Returns True if parameter is bound already
        """
        definition = None
        
        for param in revitron.Filter().byClass(revitron.DB.SharedParameterElement).getElements():
            if param.GetDefinition().Name == paramName:
                definition = param.GetDefinition()
                break
            
        if definition:
            binding = revitron.DOC.ParameterBindings[definition]
            for cat in binding.Categories:
                if cat.Name == category:
                    return True
        
        
    @staticmethod
    def bind(category, paramName, paramType = 'Text'):
        """
        Bind a new parameter to a category.

        Args:
            category (string): The built-in category 
            paramName (string): The parameter name
            paramType (string): The parameter type (see here: https://www.revitapidocs.com/2019/f38d847e-207f-b59a-3bd6-ebea80d5be63.htm)
        """
        if Parameter.isBoundToCategory(category, paramName):
            return True

        paramFile = revitron.APP.OpenSharedParameterFile()    
        group = None
        definition = None
        
        for item in paramFile.Groups:
            if item.Name == '__API':
                group = item
                break
        
        if not group:
            group = paramFile.Groups.Create('__API')
            
        for item in group.Definitions:
            if item.Name == paramName:
                definition = item
                break
            
        if not definition:
            pt = getattr(revitron.DB.ParameterType, paramType)
            ExternalDefinitionCreationOptions = revitron.DB.ExternalDefinitionCreationOptions(paramName, pt)
            definition = group.Definitions.Create(ExternalDefinitionCreationOptions)
          
        cat = revitron.Category(category).get()
        categories = revitron.APP.Create.NewCategorySet();
        categories.Insert(cat)
        binding = revitron.APP.Create.NewInstanceBinding(categories)
        revitron.DOC.ParameterBindings.Insert(definition, binding)
    
    
    def exists(self):
        """
        Checks if a parameter exists.

        Returns:
            boolean: True if existing
        """
        return (self.parameter != None)
        
       
    def hasValue(self):
        """
        Checks if parameter has a value.

        Returns:
            boolean: True if the parameter has a value
        """
        if self.exists():
            return (self.parameter.HasValue)
    
    
    def get(self):
        """
        Return the parameter value.

        Returns:
            mixed: The value
        """
        if self.exists():
            storageType = str(self.parameter.StorageType)
        else:
            storageType = 'String'
        
        switcher = {
            'String': self.getString,
            'ValueString': self.getValueString,
            'Integer': self.getInteger,
            'Double': self.getDouble,
            'ElementId': self.getElementId
        }
        
        value = switcher.get(storageType)
        return value()
        
    
    def getString(self):
        """
        Return the parameter value as string.

        Returns:
            string: The value
        """
        if self.hasValue():
            return self.parameter.AsString()
        return ''
    
    
    def getValueString(self):
        """
        Return the parameter value as value string.

        Returns:
            string: The value
        """
        if self.hasValue():
            return self.parameter.AsValueString()
        return ''
    
    
    def getInteger(self):
        """
        Return the parameter value as integer.

        Returns:
            integer: The value
        """
        if self.hasValue():
            return self.parameter.AsInteger()
        return 0
    
    
    def getDouble(self):
        """
        Return the parameter value as double.

        Returns:
            double: The value
        """
        if self.hasValue():
            return self.parameter.AsDouble()
        return 0.0
    
    
    def getElementId(self):
        """
        Return the parameter value as ElementId.

        Returns:
            object: The value
        """
        if self.hasValue():
            return self.parameter.AsElementId()
        return 0
    
    
    def set(self, value):
        """
        Set a parameter value for an element.

        Args:
            value (string): The value
        """
        if self.parameter != None and not self.parameter.IsReadOnly:
            self.parameter.Set(value)
 

class ParameterDefinition:
    

    def __init__(self, name):
        """
        Inits a new ParameterDefinition instance by name.

        Args:
            name (string): Name
        """        
        it = revitron.DOC.ParameterBindings.ForwardIterator()
        while it.MoveNext():
            if it.Key.Name == name:
                self.definition = it.Key
                self.id = it.Key.Id
       
                 
    def getValueProvider(self):
        """
        Returns the value provider for the definition.

        Returns:
            object: The value provider
        """        
        return revitron.DB.ParameterValueProvider(self.id)