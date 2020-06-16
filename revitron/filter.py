import revitron


class Filter:
    
    
    def __init__(self, viewId = None):
        """
        Inits a new Filter instance.

        Args:
            viewId (Element ID, optional): The optional view Id. Defaults to None.
        """                        
        if viewId:
            self.collector = revitron.DB.FilteredElementCollector(revitron.DOC, viewId) 
        else:   
            self.collector = revitron.DB.FilteredElementCollector(revitron.DOC)
    
    
    def applyParameterFilter(self, rule):
        """
        Filters the collection by a parameter value.

        Args:
            paramName (string): The parameter name
            value (mixed): the value
        """       
        parameterFilter = revitron.DB.ElementParameterFilter(rule)
        self.collector = self.collector.WherePasses(parameterFilter)


    def applyStringFilter(self, paramName, value, evaluator):
        """
        Apply a string filter.

        Args:
            paramName (string): The parameter name
            value (mixed): the value
            evaluator (object): The FilterStringRuleEvaluator
        """   
        valueProvider = revitron.ParameterValueProvider(paramName).get()
        rule = revitron.DB.FilterStringRule(valueProvider, evaluator, value, True)
        self.applyParameterFilter(rule)   
    
    
    def byCategory(self, name):
        """
        Filters the collection by a category name - not a built-in category.

        Args:
            name (string): The category name

        Returns:
            object: The Filter instance
        """        
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
    
    
    def byStringContains(self, paramName, value):
        """
        Filters the collection by a string contained in a parameter.

        Args:
            paramName (string): The parameter name
            value (string): The searched string

        Returns:
            object: The collector
        """
        self.applyStringFilter(paramName, value, revitron.DB.FilterStringContains())
        return self 
    
    
    def byStringEquals(self, paramName, value):
        """
        Filters the collection by a string that equals a parameter value.

        Args:
            paramName (string): The parameter name
            value (string): The searched string

        Returns:
            object: The collector
        """
        self.applyStringFilter(paramName, value, revitron.DB.FilterStringEquals())
        return self    
    
    
    def byStringBeginsWith(self, paramName, value):
        """
        Filters the collection by a string at the beginning of a parameter value.

        Args:
            paramName (string): The parameter name
            value (string): The searched string

        Returns:
            object: The collector
        """
        self.applyStringFilter(paramName, value, revitron.DB.FilterStringBeginsWith())
        return self 
    
    
    def byStringEndsWith(self, paramName, value):
        """
        Filters the collection by a string at the end of a parameter.

        Args:
            paramName (string): The parameter name
            value (string): The searched string

        Returns:
            object: The collector
        """
        self.applyStringFilter(paramName, value, revitron.DB.FilterStringEndsWith())
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
  