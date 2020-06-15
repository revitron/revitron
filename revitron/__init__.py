"""
Revitron
========
"""

from revitron._helpers import *
from revitron.element import Element
from revitron.category import Category
from revitron.document import Document
from revitron.externalreference import ExternalReference
from revitron.filter import Filter
from revitron.link import LinkRvt
from revitron.parameter import Parameter, ParameterDefinition
from revitron.selection import Selection
from revitron.transaction import Transaction
from revitron.transmissiondata import TransmissionData
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
    category = Parameter(element, 'Category').getValueString()
        
    switcher = {
        'RVT Links': LinkRvt(element)
    }
    
    return switcher.get(category, Element(element))