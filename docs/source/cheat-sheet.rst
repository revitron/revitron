Cheat Sheet
===========

This is a collection of some useful little snippets and examples that can help you getting started quickly. 

Imports 
-------

To make use of Revitron and the _() function the following items have to be imported:

.. code-block:: python

    import revitron 
    from revitron import _

The ``revitron`` module also exposes some useful properties such as the active document and gives you access 
to the ``Autodesk.Revit.DB`` class as well as follows:

.. code-block:: python

    doc = revitron.DOC
    db = revitron.DB

Selection
---------

Getting all selected elements:

.. code-block:: python

    selection = revitron.Selection.get()

Getting the first element in the selection:

.. code-block:: python

    elements = revitron.Selection.first()

Elements
--------

Printing the category and class names for of all selected elements:

.. code-block:: python

    for el in revitron.Selection.get():
        name = _(el).getClassName()
        cat = _(el).getCategoryName()
        print(name, cat)

Dependent Elements
~~~~~~~~~~~~~~~~~~

You can get a list of all dependent elements of a given element as follows:

.. code-block:: python

    dependents = _(el).getDependent()

For example the following loop prints the ``ElementIds`` of all dependent elements of the selected elements:

.. code-block:: python

    for el in revitron.Selection.get():
        for d in _(el).getDependent():
            print(d.Id)

Parameters
----------

Getting a parameter value of all Revit elements in the selection:

.. code-block:: python

    for el in revitron.Selection.get():
        name = _(el).get('Name')
        print(name)

Getting the ``Family and Type`` parameter as ``id`` and ``string`` of elements in the selection. 
Note that here we want actually the value string instead of an ``ElementId``. 
So the first function will return the ``ElementId`` and the second one will give us the actual string.

.. code-block:: python

    for el in revitron.Selection.get():
        famTypeId = _(el).get('Family and Type')
        famType = _(el).getParameter('Family and Type').getValueString()
        print(famTypeId)
        print(famType)

Setting a parameter value. Note that a shared parameter will be created and bound to the element's 
category in case the parameter doesn't exist yet. The ``el`` variable contains a Revit element.

.. code-block:: python

    t = revitron.Transaction()
    _(el).set('Cool Parameter', 'Hello there!')
    t.commit()

By default the parameter type will be ``text``. 
It is possible to pass a third argument to the function to set a parameter type:

.. code-block:: python

    t = revitron.Transaction()
    _(el).set('Cool Integer Parameter', 10, 'Integer')
    t.commit()

Filters
-------

Getting all elements of a certain category, specified by a string, for example "Room":

.. code-block:: python

    rooms = revitron.Filter().byCategory('Rooms').getElements()
    for room in rooms:
        print(_(room).get('Name'))

Instead of the *natural* category name, it is also valid to use the string representation of 
a built-in category as filter argument:

.. code-block:: python

    rooms = revitron.Filter().byCategory('OST_Rooms').getElements()

.. note:: A full list of natural category names and their corresponding built-in categories can be found `here <https://docs.google.com/spreadsheets/d/1uNa77XYLjeN-1c63gsX6C5D5Pvn_3ZB4B0QMgPeloTw/edit#gid=1549586957>`_.

Filtering those rooms by filtering the ``Name`` *"beginning with the word Room"* can be done as follows. 
Note the flexible way of breaking down the filtering into multiple line for better readability:

.. code-block:: python

    fltr = revitron.Filter()
    fltr = fltr.byCategory('Rooms')
    fltr = fltr.byStringBeginsWith('Name', 'Room')

    for room in fltr.getElements():
        print(_(room).get('Name'))

The filter can be **inverted** to get only rooms with a ``Name`` value *"not beginning with Room"*:

.. code-block:: python

    fltr = revitron.Filter()
    fltr = fltr.byCategory('Rooms')
    fltr = fltr.byStringBeginsWith('Name', 'Room', True)

    for room in fltr.getElements():
        print(_(room).get('Name'))

Getting intersecting elements of one selected element and for example printing their category name:

.. code-block:: python

    el = revitron.Selection.first()
    for intEl in revitron.Filter().byIntersection(el).getElements():
        print(_(intEl).getCategoryName())

Room Geometry
-------------

Printing or getting the boundary points of one (first) selected room:

.. code-block:: python

    el = revitron.Selection.first()
    points = _(el).getBoundaryPoints()
    for p in points:
        print(p)

Or with an inset:

.. code-block:: python

    el = revitron.Selection.first()
    points = _(el).getBoundaryInsetPoints(0.2)
    for p in points:
        print(p)

Get list of all boundary segments of the first selected room:

.. code-block:: python

    el = revitron.Selection.first()
    boundary = _(el).getBoundary()
    for segment in boundary:
        print(segment)

Bounding Boxes
--------------

Getting the **Revitron** bounding box object of the first element in the selection:

.. code-block:: python

    el = revitron.Selection.first()
    bbox = _(el).getBbox()
    print(bbox)

Storing Configurations
----------------------

You can store any kind of easily serializable data such as ``string``, ``number``, ``list`` or ``dict`` 
in a config storage container as follows:

.. code-block:: python

    data = {'some': 'content'}
    revitron.DocumentConfigStorage().set('my.namespace', data)

To get data out of that storage simply do the following. 
Note that you can pass a **default** value as a second argument to be returned in case there is no 
data stored yet and you don't want to check for existence first:

.. code-block:: python

    config = revitron.DocumentConfigStorage().get('my.namespace', dict())
    print(config.get('some'))