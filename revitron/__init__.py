"""
Revitron
========
"""

import Autodesk.Revit.DB
import os

from revitron._helpers import *
from revitron.boundingbox import *
from revitron.element import *
from revitron.excel import *
from revitron.export import *
from revitron.category import *
from revitron.document import *
from revitron.externalreference import *
from revitron.filter import *
from revitron.link import *
from revitron.parameter import *
from revitron.selection import *
from revitron.transaction import *
from revitron.transmissiondata import *
from revitron.view import *

parent = os.path.dirname 

try:
    DOC = __revit__.ActiveUIDocument.Document
    UIDOC = __revit__.ActiveUIDocument
    APP = DOC.Application
    ACTIVEVIEW = DOC.ActiveView
except:
    pass


DB = Autodesk.Revit.DB
LIB_DIR = parent(parent(__file__))


def _(element):
    """
    Shorthand function to init a Revitron element instance based on a Revit element category.

    Args:
        element (object): The Revit element

    Returns:
        mixed: A Revitron element instance
    """    
    category = Element(element).getParameter('Category').getValueString()
    
    switcher = {
        'RVT Links': LinkRvt(element)
    }
    
    return switcher.get(category, Element(element))