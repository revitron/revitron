#-*- coding: UTF-8 -*-
import re


class Parameter:
    
    
    def __init__(self, element, name):        
        """
        Init a new parameter instance.

        Args:
            element (object): Revit element
            name (string): The parameter name
        """
        self.element = element
        self.name = name
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
        import revitron
        
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
            paramType (string): The parameter type (see `here <https://www.revitapidocs.com/2019/f38d847e-207f-b59a-3bd6-ebea80d5be63.htm>`_)
        
        Returns:
            boolean: Returns True on success and False on error
        """
        import revitron
        
        if Parameter.isBoundToCategory(category, paramName):
            return True

        paramFile = revitron.APP.OpenSharedParameterFile()    
        group = None
        definition = None
        
        if paramFile is None:
            print('Please define a shared parameters file.')
            return False
        
        for item in paramFile.Groups:
            if item.Name == 'REVITRON':
                group = item
                break
        
        if not group:
            group = paramFile.Groups.Create('REVITRON')
            
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
    
        return True
    
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
    
    
    def set(self, value, paramType = 'Text'):
        """
        Set a parameter value for an element.

        Attention:
        
            Possible parameter types are: 
            Text, Integer, Number, Length, Angle, Material, YesNo, MultilineText, FamilyType 
            and `more <https://www.revitapidocs.com/2019/f38d847e-207f-b59a-3bd6-ebea80d5be63.htm>`_.

        Args:
            value (string): The value
            paramType (string, optional): The `parameter type <https://www.revitapidocs.com/2019/f38d847e-207f-b59a-3bd6-ebea80d5be63.htm>`_. Defaults to "Text". 
        """
        if self.parameter == None:
            if Parameter.bind(self.element.Category.Name, self.name, paramType):
                self.parameter = self.element.LookupParameter(self.name)
            else:
                print('Error setting value of parameter "{}"'.format(self.name))
                return False
        if not self.parameter.IsReadOnly:
            self.parameter.Set(value)
 

class ParameterNameList:
    

    def __init__(self):
        """
        Inits a new ParameterNameList instance including all parameter names in the document.
        """            
        import revitron
            
        self.parameters = []
        
        for name in BuiltInParameterNameMap().map:
            self.parameters.append(name)
        
        for param in revitron.Filter().byClass(revitron.DB.SharedParameterElement).getElements():
            self.parameters.append(param.GetDefinition().Name)
            
        for param in revitron.Filter().byClass(revitron.DB.ParameterElement).getElements():
            self.parameters.append(param.GetDefinition().Name)    
            
        self.parameters = sorted(list(set(self.parameters)))
        
    def get(self):
        """
        Returns the parameter list.

        Returns:
            list: The list with all parameters in the document.
        """        
        return self.parameters


class ParameterValueProviders:
    

    def __init__(self, name):
        """
        Inits a new ParameterValueProviders instance by name. Such an instance consists of a list
        of value providers matching a parameters with a name visible to the user.
        Note that this list can have more than one value provider, since a parameter name possible matches 
        multiple built-in parameters.

        Args:
            name (string): Name
        """      
        import revitron
        
        self.providers = []
        paramIds = []
        it = revitron.DOC.ParameterBindings.ForwardIterator()
        while it.MoveNext():
            if it.Key.Name == name:
                paramIds.append(it.Key.Id)
        if not paramIds:
            try:
                paramIds = BuiltInParameterNameMap().get(name)  
            except: 
                pass   
        for paramId in paramIds:    
            self.providers.append(revitron.DB.ParameterValueProvider(paramId))

         
    def get(self):
        """
        Returns the list of value providers.

        Returns:
            list: The list of value providers
        """            
        return self.providers
    
    
class BuiltInParameterNameMap:
    
    
    def __init__(self):
        """
        Inits a new BuiltInParameterNameMap instance. The map is a dictionary where the key
        is a parameter name that is visible to the user and the value is a list of built-in parameters 
        represented by that name.
        """
        import revitron
        
        self.map = dict()
        for item in dir(revitron.DB.BuiltInParameter):
            try:
                bip = getattr(revitron.DB.BuiltInParameter, item)
                name = revitron.DB.LabelUtils.GetLabelFor(bip)
                if name not in self.map:
                    self.map[name] = []
                self.map[name].append(revitron.DB.ElementId(int(bip)))
            except:
                pass
            

    def get(self, name):
        """
        Return the list of matching built-in parameters for a given name.

        Args:
            name (string): The parameter name visible to the user

        Returns:
            list: The list of built-in parameters
        """        
        return self.map[name]
    
    
class ParameterTemplate:
    """
    Create a string based on a parameter template where parameter names are wrapped in :code:`{}` and get substituted with their value::
    
        This sheet has the number {Sheet Number} and the name {Sheet Name}
    """
    
    def __init__(self, element, template, sanitize = True):
        """
        Inits a new ParameterTemplate instance.

        Args:
            element (object): A Revit element
            template (string): A template string
            sanitize (bool, optional): Optionally sanitize the returned string. Defaults to True.
        """
        self.element = element
        self.template = template
        self.sanitize = sanitize
        
        
    def reCallback(self, match):
        """
        The callback function used by the :code:`get()` method.

        Args:
            match (object): The regex match object

        Returns:
            string: The processed string
        """
        import revitron
        
        parameter = match.group(1)
        string = str(revitron.Element(self.element).get(parameter))
        
        if self.sanitize:
            string = revitron.String.sanitize(string)
            
        return string
    
    
    def render(self):
        """
        Returns the rendered template string.

        Returns:
            string: The rendered string
        """
        return re.sub('\{(.+?)\}', self.reCallback, self.template)
        