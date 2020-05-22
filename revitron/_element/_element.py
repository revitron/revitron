import revitron

class Element:
    
    el = None
    
    def __init__(self, el):
        self.el = el
    
    def getClassName(self):
        return self.el.__class__.__name__
    
    def set(self, paramName, value, paramType = 'Text'):
        revitron.Parameter.bind(self.el.Category.Name, paramName, paramType)
        revitron.Parameter.set(self.el, paramName, value)
        return self