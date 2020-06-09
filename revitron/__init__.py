from _element import *
from _category import *
from _document import *
from _filter import *
from _parameter import *
from _selection import *
from _transaction import *
import Autodesk.Revit.DB

try:
    DOC = __revit__.ActiveUIDocument.Document
    UIDOC = __revit__.ActiveUIDocument
    APP = DOC.Application
except:
    pass

DB = Autodesk.Revit.DB

def _(element):
    """
    Shorthand function to init a Revitron element instance based on a Revit element category.

    Args:
        element (object): The Revit element

    Returns:
        mixed: A Revitron element instance
    """    
    category = revitron.Parameter(element, 'Category').getValueString()
        
    switcher = {
        'RVT Links': LinkRvt(element)
    }
    
    return switcher.get(category, Element(element))