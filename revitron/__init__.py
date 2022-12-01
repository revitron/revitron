"""
The Revitron package is a `Revit API <https://www.revitapidocs.com/>`_ wrapper written in Python 
to help you developing clean and powerful **Revit** plugins in `pyRevit <https://github.com/eirannejad/pyRevit>`_.
The package consists of a minimal main `module`_ and collection of specific `submodules`_ covering certain topics 
of the **Revit API**.

Concept
=======

Basically this package is designed to be a generic **Revit API** toolbox. It doesn't focus on a single topic, but tries to
combine multiple wrapper classes instead to enable you to create plugins using just one single base library.
However, there are two topics that are in the main focus of many **pyRevit** plugins --- working with elements and filtering. 

.. note::

	Check out the `cheat sheet <cheat-sheet.html>`_ to get you started quickly with the most common tools.

Working with Elements
---------------------

Revitron elements wrap standard Revit elements and expose additional `convenience methods <revitron.element.html>`_
in order to make working with the API a bit less cumbersome::

	import revitron
	_element = revitron.Element(element)

Alternatively to the default constructor it is also possible to create element instances by using the 
following shorthand function::

	from revitron import _
	_element = _(element)

In both cases ``_element`` is a proper Revitron element. This comes in handy in many situations where a quick access to an 
element is needed. The following example demonstrates how it is possible to set a parameter value, even though 
the parameter itself doesn't exist yet::

	from revitron import _
	_(element).set('ParameterName', value)

In that one line we just set a parameter value and also created the parameter if neccessary.
In order to get a parameter value of a given element we can use::

	from revitron import _
	comment = _(element).get('Comments')
	
You can find the documentation of more available element methods in the `revitron.element <revitron.element.html>`_ reference.
	
Using Filters
-------------
	
Besides element properties, filtering is another core functionality of this package. Working with ``FiteredElementCollector`` 
instances can be quite complex and difficult to debug. Revitron provides a `Filter <revitron.filter.html>`_ that implements
a powerful tool to also filter the database by parameter values using human readable one-liner::

	import revitron
	filter = revitron.Filter
	ids = filter().byStringEquals('param', 'value').noTypes().getElementIds()

.. _module:

Revitron Module
===============

The main Revitron module contains only some global module properties as well as the magic ``_()`` function. 
Specific classes are located in the `submodules`_ listed below.

.. data:: DOC

	The currently active document. 
		
.. data:: UIDOC

	The active UI document.

.. data:: APP

	A shortcut for accessing the application object of the active document.

.. data:: ACTIVE_VIEW

	The active view element.

.. data:: DB

	A shortcut for ``Autodesk.Revit.DB``.
	
.. data:: LIB_DIR

	The path to the **Revitron** library extension directory.

.. data:: REVIT_VERSION

	The version number string of the running Revit application.
"""
import Autodesk.Revit.DB
import pyrevit
import os

from revitron._utils import *
from revitron.analyze import *
from revitron.boundingbox import *
from revitron.element import *
from revitron.excel import *
from revitron.export import *
from revitron.category import *
from revitron.create import *
from revitron.document import *
from revitron.externalreference import *
from revitron.failure import *
from revitron.filter import *
from revitron.geometry import *
from revitron.grid import *
from revitron.link import *
from revitron.parameter import *
from revitron.raytrace import *
from revitron.room import *
from revitron.roomtag import *
from revitron.selection import *
from revitron.transaction import *
from revitron.transmissiondata import *
from revitron.unit import *
from revitron.view import *

parent = os.path.dirname

try:
	DOC = __revit__.ActiveUIDocument.Document
	UIDOC = __revit__.ActiveUIDocument
	APP = DOC.Application
	ACTIVE_VIEW = DOC.ActiveView
except:
	pass

DB = Autodesk.Revit.DB
LIB_DIR = parent(parent(__file__))
REVIT_VERSION = pyrevit.HOST_APP.uiapp.Application.VersionNumber
REVITRON_VERSION = '0.4.1'


def _(element):
	"""
	Shorthand function to init a Revitron element instance based on a Revit element category.

	Args:
		element (object): The Revit element

	Returns:
		mixed: A Revitron element instance
	"""
	try:
		category = Element(element).getParameter('Category').getValueString()
		switcher = {'RVT Links': LinkRvt, 'Rooms': Room}
		wrapper = switcher.get(category, Element)
		return wrapper(element)
	except:
		return Element(element)