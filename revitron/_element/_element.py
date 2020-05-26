import revitron

class Element:
    
    el = None
    
    def __init__(self, element):
        self.element = element
    
    def getClassName(self):
        return self.element.__class__.__name__
    
    def get(self, paramName):
        return revitron.Parameter(self.element, paramName).get()
    
    def set(self, paramName, value, paramType = 'Text'):
        revitron.Parameter.bind(self.element.Category.Name, paramName, paramType)
        revitron.Parameter(self.element, paramName).set(value)
        return self