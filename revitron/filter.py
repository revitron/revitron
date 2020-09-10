
from System.Collections.Generic import List


class Filter:
    
    
    def __init__(self, scope = None):
        """
        Inits a new Filter instance.

        Args:
            scope (Element ID or list of elements, optional): The optional scope. It can be either a view Id or a list of elements Defaults to None.
        """   
        import revitron
        
        self.scope = scope         
        if scope:
            if type(scope) == list:
                elementIds = []
                for element in scope:
                    elementIds.append(element.Id)
                scope = List[revitron.DB.ElementId](elementIds) 
            self.collector = revitron.DB.FilteredElementCollector(revitron.DOC, scope) 
        else:   
            self.collector = revitron.DB.FilteredElementCollector(revitron.DOC)
    
    
    def applyParameterFilter(self, rule, invert = False):
        """
        Applies a parameter filter.

        Args:
            rule (object): The filter rule object
            invert (boolean): Inverts the filter
        """  
        import revitron
             
        parameterFilter = revitron.DB.ElementParameterFilter(rule, invert)
        self.collector = self.collector.WherePasses(parameterFilter)


    def applyStringFilter(self, paramName, value, evaluator, invert = False):
        """
        Applies a string filter.

        Args:
            paramName (string): The parameter name
            value (mixed): the value
            evaluator (object): The FilterStringRuleEvaluator
            invert (boolean): Inverts the filter
        """   
        import revitron
        
        filters = []
    
        # Since a visible parameter name could match multiple built-in parameters,
        # we get a list of value providers. 
        # While iterating that list, the parameter filter is applied each time 
        # to a fresh element collector that will be later merged or intersected with the others. 
        for valueProvider in revitron.ParameterValueProviders(paramName).get():
            rule = revitron.DB.FilterStringRule(valueProvider, evaluator, value, True)
            _filter = Filter()
            # Try to get elements from the collector as base for the fresh collector.
            # In case there was never a filter applied before, getting elements will raise an exception
            # and new Filter() instance is created with the same scope.
            try:
                _filter.collector = revitron.DB.FilteredElementCollector(revitron.DOC, self.collector.ToElementIds())
            except:
                _filter.collector = revitron.Filter(self.scope).collector
            _filter.applyParameterFilter(rule, invert) 
            filters.append(_filter)
        
        self.collector = filters[0].collector
        
        if len(filters) > 1:
            for i in range(1, len(filters)):
                if not invert:
                    self.collector.UnionWith(filters[i].collector)
                else:
                    self.collector.IntersectWith(filters[i].collector)
                
           
    def byCategory(self, name):
        """
        Filters the collection by a category name - not a built-in category.

        Args:
            name (string): The category name

        Returns:
            object: The Filter instance
        """   
        import revitron
             
        self.collector = self.collector.OfCategory(revitron.Category(name).getBic())
        return self
    
    
    def byClass(self, cls):
        """
        Filters the collection by class.

        Returns:
            object: The Filter instance
        """        
        self.collector = self.collector.OfClass(cls)
        return self
    
    
    def byStringContains(self, paramName, value, invert = False):
        """
        Filters the collection by a string contained in a parameter.

        Args:
            paramName (string): The parameter name
            value (string): The searched string
            invert (boolean): Inverts the filter

        Returns:
            object: The collector
        """
        import revitron
        
        self.applyStringFilter(paramName, value, revitron.DB.FilterStringContains(), invert)
        return self 
    
    
    def byStringEquals(self, paramName, value, invert = False):
        """
        Filters the collection by a string that equals a parameter value.

        Args:
            paramName (string): The parameter name
            value (string): The searched string
            invert (boolean): Inverts the filter

        Returns:
            object: The collector
        """
        import revitron
        
        self.applyStringFilter(paramName, value, revitron.DB.FilterStringEquals(), invert)
        return self    
    
    
    def byStringBeginsWith(self, paramName, value, invert = False):
        """
        Filters the collection by a string at the beginning of a parameter value.

        Args:
            paramName (string): The parameter name
            value (string): The searched string
            invert (boolean): Inverts the filter

        Returns:
            object: The collector
        """
        import revitron
        
        self.applyStringFilter(paramName, value, revitron.DB.FilterStringBeginsWith(), invert)
        return self 
    
    
    def byStringEndsWith(self, paramName, value, invert = False):
        """
        Filters the collection by a string at the end of a parameter.

        Args:
            paramName (string): The parameter name
            value (string): The searched string
            invert (boolean): Inverts the filter

        Returns:
            object: The collector
        """
        import revitron
        
        self.applyStringFilter(paramName, value, revitron.DB.FilterStringEndsWith(), invert)
        return self 
    
    
    def onlyTypes(self):
        """
        Reduce to collection to types only.

        Returns:
            object: The Filter instance
        """
        self.collector = self.collector.WhereElementIsElementType()
        return self
    
    
    def noTypes(self):
        """
        Removes all types from collection.

        Returns:
            object: The Filter instance
        """
        self.collector = self.collector.WhereElementIsNotElementType()
        return self
    
    
    def getElements(self):
        """
        Get the collection as elements.

        Returns:
            list: The list of filtered elements
        """        
        return self.collector.ToElements()
    
    
    def getElementIds(self):
        """
        Get the collection as element IDs.

        Returns:
            list: The list of filtered element IDs
        """        
        return self.collector.ToElementIds()
  