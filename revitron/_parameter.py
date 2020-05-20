import revitron
import os

class Param:
    
    @staticmethod
    def isBoundToCategory(category, paramName):
        
        try:
            for param in revitron.Filter().byClass(revitron.DB.SharedParameterElement).getElements():
                
                if param.GetDefinition().Name == paramName:
                    definition = param.GetDefinition()
                    break
            
            if definition:
                binding = revitron.DOC.ParameterBindings[definition]
                
                for cat in binding.Categories:
                    if cat.Name == category:
                        return True
        except:
            return False
            
    @staticmethod
    def bind(category, paramName, paramType):
    
        if Param.isBoundToCategory(category, paramName):
            return True
    
        paramFile = revitron.APP.OpenSharedParameterFile()    
        group = None
        
        for item in paramFile.Groups:
            if item.Name == '__API':
                group = item
                break
        
        if not group:
            group = paramFile.Groups.Create('__API')
            
        ExternalDefinitionCreationOptions = revitron.DB.ExternalDefinitionCreationOptions(paramName, paramType)
        definition = group.Definitions.Create(ExternalDefinitionCreationOptions)
        cat = revitron.DOC.Settings.Categories.get_Item(category)
        categories = revitron.APP.Create.NewCategorySet();
        categories.Insert(cat)
        binding = revitron.APP.Create.NewInstanceBinding(categories)
        revitron.DOC.ParameterBindings.Insert(definition, binding)
        