from _element import *
from _filter import *
from _parameter import *
from _selection import *
import Autodesk.Revit.DB

DOC = __revit__.ActiveUIDocument.Document
UIDOC = __revit__.ActiveUIDocument
APP = DOC.Application
DB = Autodesk.Revit.DB

class _(Element):
    pass