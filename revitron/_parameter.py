import revitron
import os

class Parameter:
    
    
    def __init__(self, element, name):
        """
        Init a new parameter instance.

        Arguments:
            element {object} -- Revit element
            name {string} -- The parameter name
        """
        self.parameter = element.LookupParameter(name)
    
    
    @staticmethod
    def isBoundToCategory(category, paramName):
        """
        Test if a parameter is bound to a given category.

        Arguments:
            category {string} -- The category name
            paramName {sting} -- The parameter name

        Returns:
            boolean -- Returns True if parameter is bound already
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

        Arguments:
            category {string} -- The built-in category 
            paramName {string} -- The parameter name
            paramType {string} -- The parameter type (see here: https://www.revitapidocs.com/2019/f38d847e-207f-b59a-3bd6-ebea80d5be63.htm)
            
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
          
        cat = revitron.DOC.Settings.Categories.get_Item(category)
        categories = revitron.APP.Create.NewCategorySet();
        categories.Insert(cat)
        binding = revitron.APP.Create.NewInstanceBinding(categories)
        revitron.DOC.ParameterBindings.Insert(definition, binding)
    
    
    def exists(self):
        """
        Checks if a parameter exists.add()

        Returns:
            boolean -- True if existing
        """
        return (self.parameter != None)
        
       
    def hasValue(self):
        """
        Checks if parameter has a value.add()

        Returns:
            boolean -- True if the parameter has a value
        """
        if self.exists():
            return (self.parameter.HasValue)
    
    
    def get(self):
        """
        Get a parameter value.
        """
        switcher = {
            'String': self.getString,
            'ValueString': self.getValueString,
            'Integer': self.getInteger,
            'Double': self.getDouble
        }
        value = switcher.get(str(self.parameter.StorageType))
        return value()
        
    
    def getString(self):
        """
        Return the parameter value as string.

        Returns:
            string -- The value
        """
        if self.hasValue():
            return self.parameter.AsString()
        return ''
    
    
    def getValueString(self):
        """
        Return the parameter value as value string.

        Returns:
            string -- The value
        """
        if self.hasValue():
            return self.parameter.AsValueString()
        return ''
    
    
    def getInteger(self):
        """
        Return the parameter value as integer.

        Returns:
            integer -- The value
        """
        if self.hasValue():
            return self.parameter.AsInteger()
        return 0
    
    
    def getDouble(self):
        """
        Return the parameter value as double.

        Returns:
            double -- The value
        """
        if self.hasValue():
            return self.parameter.AsDouble()
        return 0.0
    
    
    def set(value):
        """
        Set a parameter value for an element.

        Arguments:
            value {string} -- The value
        """
        if self.parameter != None and not self.parameter.IsReadOnly:
            self.parameter.Set(value)
 