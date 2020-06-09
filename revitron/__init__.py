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

class _(Element):
    pass