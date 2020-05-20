import revitron

class Element:
    
    el = None
    
    def __init__(self, el):
        self.el = el
    
    def getClassName(self):
        return self.el.__class__.__name__