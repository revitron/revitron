import revitron
import os

class Parameter:
    
    @staticmethod
    def isBoundToCategory(category, paramName):
        """
        Test if a parameter is bound to a given category

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
        Bind a new parameter to a category

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
        
    @staticmethod
    def set(element, paramName, value):
        """
        Set a parameter value for an element.

        Arguments:
            element {object} -- The element
            paraName {string} -- The parameter name
            value {string} -- The value
        """
        param = element.LookupParameter(paramName)
        if param != None and not param.IsReadOnly:
            param.Set(value)
 
        